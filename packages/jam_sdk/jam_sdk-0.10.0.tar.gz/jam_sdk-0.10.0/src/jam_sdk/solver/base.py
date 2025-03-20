from __future__ import annotations

import asyncio
import logging
import time
from abc import abstractmethod
from typing import Any

import msgspec
from aiocache import Cache
from eth_typing import HexStr
from eth_utils.address import to_checksum_address
from msgspec.json import decode, encode
from web3 import AsyncHTTPProvider, AsyncWeb3, Web3
from web3.middleware.geth_poa import async_geth_poa_middleware
from web3.types import TxParams, Wei
from websockets.asyncio.client import ClientConnection, connect
from websockets.exceptions import ConnectionClosedError

from jam_sdk.constants import (
    JAM_SETTLEMENT_ABI,
    JAM_SETTLEMENT_CONTRACT,
    QUOTE_CACHE_TTL,
)
from jam_sdk.solver.solver_types import (
    BaseError,
    BaseJAMSchema,
    CachedQuote,
    ExecuteError,
    ExecuteErrorType,
    ExecuteRequest,
    ExecuteResponse,
    InteractionData,
    MessageTypes,
    QuoteError,
    QuoteErrorType,
    QuoteRequest,
    QuoteResponse,
    SolverConnection,
    TakerQuoteResponse,
    TokenAmountResponse,
)

logging.basicConfig(level=logging.INFO)


class BaseSolver:
    """
    Base Solver class for writing custom solvers. Override the `get_quote` and `execute` functions.
    """

    def __init__(self, chain_id: int, rpc_url: str, connection: SolverConnection) -> None:
        """
        Create an instance of the solver with given paramters

        Args:
            chain_id (int): Chain ID of the chain providing solutions for.
            rpc_url (str): JSON RPC Endpoint for the chain.
            connection (SolverConnection): Connection including the details to the JAM server
        """
        self.connection = connection
        self.logger = logging.getLogger("SolverSDK")
        self.web3 = AsyncWeb3(AsyncHTTPProvider(rpc_url))
        self.web3.middleware_onion.inject(async_geth_poa_middleware, "poa", 0)
        self.chain_id = chain_id
        self.jam_contract = self.web3.eth.contract(
            address=to_checksum_address(JAM_SETTLEMENT_CONTRACT[self.chain_id]),
            abi=JAM_SETTLEMENT_ABI,
        )
        self.quote_cache = Cache(Cache.MEMORY)
        self.ws: ClientConnection

    async def start(self) -> None:
        """Starts a websocket connection to JAM."""
        headers = {"name": self.connection.name, "authorization": self.connection.auth}
        retries: int = 1
        while True:
            try:
                self.logger.info(f"Connecting to JAM on {self.connection.url}")
                self.ws = await connect(
                    self.connection.url,
                    additional_headers=headers,
                )
                self.logger.info(f"Solver {self.connection.name} - Successfully connected to JAM")
                await self._handle_ws_message()
            except ConnectionRefusedError:
                if retries > 5:
                    raise Exception("Connection refused too many times") from ConnectionRefusedError
                self.logger.warning(f"Connection refused. Trying again in {retries**2}s...")
                await asyncio.sleep(retries**2)
                retries += 1
            except ConnectionClosedError:
                self.logger.warning("Connection is closed. Reconnecting in 5s...")
                await asyncio.sleep(1)
            except Exception:
                self.logger.exception("Disconnected from JAM. Trying again in 5s...")
                await asyncio.sleep(5)

    async def _send_response(
        self, req_msg: dict, response: QuoteResponse | QuoteError | TakerQuoteResponse | ExecuteResponse | ExecuteError
    ) -> None:
        """
        Send a response to JAM.

        Args:
            req_msg (dict): Request
            response (BaseMessage): Response
        """
        ws_message = BaseJAMSchema(
            chain_id=req_msg["chain_id"],
            msg_topic=req_msg["msg_topic"],
            msg_type=MessageTypes.error if isinstance(response, BaseError) else MessageTypes.response,
            msg=response.to_ws() if not isinstance(response, QuoteError | ExecuteError) else response,
        )
        self.logger.info(f"Sending msg to JAM: {ws_message}")
        await self.ws.send(msgspec.json.encode(ws_message))

    async def _handle_quote_request(self, msg: dict) -> None:
        """Handle incoming JAM request

        Args:
            msg (dict): json message
        """
        chain_id = msg["chain_id"]
        msg_content: dict[str, Any] = msg["msg"]
        match msg["msg_topic"]:
            case "quote":
                gasless = True
            case "taker_quote":
                gasless = False
            case _:
                raise ValueError(f"Invalid msg topic {msg['msg_topic']}")
        request = QuoteRequest.from_ws(msg_content, gasless=gasless)
        try:
            response = (
                await self.get_quote(chain_id, request)
                if request.gasless
                else await self.get_taker_quote(chain_id, request)
            )
            if isinstance(response, QuoteResponse | TakerQuoteResponse) and not response.amounts:
                raise Exception(f"No amounts returned: {response.amounts}")
        except Exception as e:
            self.logger.exception("Failed getting solution")
            response = QuoteError(
                quote_id=request.quote_id, error_type=QuoteErrorType.Unknown, error_msg=f"failed to quote: {e!s}"
            )
        # TODO: other sanity checks
        if isinstance(response, QuoteResponse):
            await self.quote_cache.set(
                key=response.quote_id,
                value=CachedQuote(chain_id=chain_id, request=request, response=response),
                ttl=QUOTE_CACHE_TTL,
            )
        await self._send_response(msg, response)

    async def _handle_execute_request(self, msg: dict) -> None:
        """
        Handle execution request from JAM and forward to implemented function

        Args:
            msg (dict): execution request json

        Raises:
            Exception: If the quote missing
        """
        request = ExecuteRequest.from_ws(msg["msg"])
        try:
            cached_quote = await self.quote_cache.get(request.quote_id)
            if not cached_quote:
                raise Exception("Quote missing from cache")
            # TODO: Check expiry
            response = await self.execute(request, cached_quote)
        except Exception:
            self.logger.exception("Failed to execute solution")
            response = ExecuteError(
                quote_id=request.quote_id, error_type=ExecuteErrorType.Reject, error_msg="failed to execute order"
            )

        self.logger.info(response)
        await self._send_response(msg, response)

    async def _handle_ws_message(self) -> None:
        """
        Handle websocket message from JAM
        """
        try:
            async for data in self.ws:
                try:
                    msg = msgspec.json.decode(data)
                    if isinstance(msg, dict):
                        self.logger.info(f"Solver msg received: {msg}")
                        if msg["msg_topic"] in {"quote", "taker_quote"} and msg["msg_type"] == "request":
                            await self._handle_quote_request(msg)
                        elif msg["msg_topic"] == "execute_order" and msg["msg_type"] == "request":
                            await self._handle_execute_request(msg)
                        else:
                            self.logger.info("Unrecognised message")
                except Exception:
                    self.logger.exception(f"Error handling websocket message: {data!r}")
        except ConnectionClosedError as e:
            self.logger.error(f"Connection closed - Code {e.code}, {e.reason}")  # noqa: TRY400
            raise

    def encode_interactions(self, interactions: list[InteractionData]) -> list[dict]:
        """
        Encode the interactions parameter of a settlement call.

        Args:
            interactions (list[InteractionData]): List of interactions

        Returns:
            list[dict]: Interactions ready for submission to settlement.
        """
        return [decode(encode(interaction)) for interaction in interactions]

    async def build_settle(
        self,
        quote_request: QuoteRequest,
        quote_response: QuoteResponse,
        interactions: list[InteractionData],
        execute_request: ExecuteRequest,
        balance_recipient: str,
        tx_params: TxParams | None = None,
    ) -> TxParams:
        """
        Simulate and build the settlement call to JAM.

        Args:
            quote_request (QuoteRequest): Quote request received for this order
            quote_response (QuoteResponse): Quote response given for this order
            interactions (list[InteractionData]): List of interactions to execute for this order
            execute_request (ExecuteRequest): Execute request received for this order
            balance_recipient (str): The recepient of the user balance before interactions.
            txParams (TxParams | None, optional): _description_. Optional transaction parameters (to, from etc.) to add while building the transaction.

        Raises:
            Exception: Will be raised if the simulating or building fails. This includes gas estimation issues.

        Returns:
            TxParams: Transaction object ready to sign.
        """
        if time.time() > quote_request.expiry:
            raise Exception("Order Expired")
        order = encode_order(quote_request, quote_response, execute_request.min_amounts)
        self.logger.info(f"{order=}")
        call_data = self.jam_contract.encode_abi(
            fn_name="settle",
            args=[
                order,
                execute_request.signature,
                self.encode_interactions(interactions),
                Web3.to_bytes(hexstr=HexStr("0x")),  # quote_request.hooks_data,
                balance_recipient,
            ],
        )

        base_settle_tx: TxParams = {
            "chainId": self.chain_id,
            "to": self.jam_contract.address,
            "data": call_data,
            "value": Wei(0),
        }

        settle_tx = base_settle_tx | tx_params if tx_params else base_settle_tx

        try:
            gas = await self.web3.eth.estimate_gas(settle_tx)
        except Exception:
            self.logger.exception(f"build_settle estimation failed for transaction {settle_tx=}")
            raise

        settle_tx_extra: TxParams = {"gas": gas}
        settle_tx = settle_tx | settle_tx_extra
        return settle_tx

    @abstractmethod
    async def get_quote(self, chain_id: int, request: QuoteRequest) -> QuoteResponse | QuoteError:
        """
        Get a solution to the quote request.

        Args:
            chain_id (int): Chain ID
            request (QuoteRequest): Request for quote

        Returns:
            QuoteResponse | TakerQuoteResponse | QuoteError: Return a `QuoteResponse` with quoted amounts or `QuoteError` to indicate a failure.
        """
        ...

    @abstractmethod
    async def get_taker_quote(self, chain_id: int, request: QuoteRequest) -> TakerQuoteResponse | QuoteError:
        """
        Get a solution to the taker quote request.

        Args:
            chain_id (int): Chain ID
            request (QuoteRequest): Request for quote

        Returns:
            TakerQuoteResponse | QuoteError: Return a `TakerQuoteResponse` with quoted amounts and calldata or `QuoteError` to indicate a failure.
        """
        ...

    @abstractmethod
    async def execute(self, request: ExecuteRequest, quote_cache: CachedQuote) -> ExecuteResponse | ExecuteError:
        """
        Execute the given quote.

        Args:
            request (ExecuteRequest): An execution request with quote details and user signatures.
            quote_cache (CachedQuote): Cached quote request and response for the given execution request.

        Returns:
            ExecuteResponse | ExecuteError: An `ExecuteResponse` for a successful execution and `ExecuteError` otherwise
        """
        ...


# corresponds to order in `settle` call
def encode_order(order: QuoteRequest, quote_response: QuoteResponse, min_amounts: list[TokenAmountResponse]) -> dict:
    """
    Encode a JAM Order into dict ready to submit through settlement.

    Args:
        order (QuoteRequest): The request for this order.
        quote_response (QuoteResponse): The response to the JAM order.
        min_amounts (list[TokenAmountResponse]): Tokens and amounts given as a response to the JAM order with slippage.

    Returns:
        dict: Structured order data ready for submission to settlement.
    """
    buy_tokens: list[str] = []
    sell_tokens: list[str] = []
    buy_amounts: list[int] = []
    sell_amounts: list[int] = []

    for buy_token in min_amounts:
        buy_tokens.append(buy_token.address)
        buy_amounts.append(buy_token.amount)

    for sell_token in order.order_sell_tokens:
        sell_tokens.append(sell_token.address)
        if sell_token.amount:
            sell_amounts.append(sell_token.amount)

    encoded_order = {
        "taker": order.taker,
        "receiver": order.receiver,
        "expiry": order.expiry,
        "exclusivityDeadline": order.exclusivity_deadline,
        "nonce": order.nonce,
        "executor": quote_response.executor,
        "partnerInfo": order.partner_info,
        "sellTokens": sell_tokens,
        "buyTokens": buy_tokens,
        "sellAmounts": sell_amounts,
        "buyAmounts": buy_amounts,
        "usingPermit2": order.using_permit2,
    }

    return encoded_order
