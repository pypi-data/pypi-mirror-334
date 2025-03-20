from __future__ import annotations

from decimal import Decimal
from enum import Enum
from typing import Any, cast

import msgspec
from eth_abi.abi import encode as encode_abi
from eth_typing import HexStr
from eth_utils.abi import collapse_if_tuple
from msgspec.json import decode, encode
from pydantic import BaseModel
from web3 import Web3
from web3.auto import w3

from jam_sdk.constants import HASH_HOOKS_ABI, NATIVE_TOKEN_ADDRESS


class ApprovalType(Enum):
    Standard = "Standard"
    Permit = "Permit"
    Permit2 = "Permit2"


class OrderType(Enum):
    OneToOne = "121"
    OneToMany = "12M"
    ManyToOne = "M21"
    ManyToMany = "M2M"


class TokenAmount(msgspec.Struct):
    address: str
    amount: int | None
    usd_price: float | None

    def to_ws(self) -> dict:
        return {
            "address": self.address,
            "amount": str(self.amount) if self.amount else None,
            "usd_price": self.usd_price,
        }

    @staticmethod
    def from_ws(data: dict) -> TokenAmount:
        return TokenAmount(
            address=data["address"],
            amount=(int(data["amount"]) if "amount" in data and data["amount"] is not None else None),
            usd_price=data["usd_price"],
        )


class TokenAmountResponse(msgspec.Struct):
    address: str
    amount: int

    def to_ws(self) -> dict:
        return {"address": self.address, "amount": str(self.amount)}

    @staticmethod
    def from_ws(data: dict) -> TokenAmountResponse:
        return TokenAmountResponse(
            address=data["address"],
            amount=(int(data["amount"])),
        )


class InteractionData(msgspec.Struct):
    result: bool
    to: str
    value: int
    data: str

    def to_ws(self) -> dict:
        return {
            "result": self.result,
            "to": self.to,
            "value": str(self.value),
            "data": self.data,
        }

    @staticmethod
    def from_ws(data: dict) -> InteractionData:
        return InteractionData(
            result=data["result"],
            to=data["to"],
            value=int(data["value"]),
            data=data["data"],
        )

    def abi_encode(self) -> bytes:
        return encode_abi(
            ["bool", "address", "uint256", "bytes"],
            [self.result, self.to, self.value, Web3.to_bytes(hexstr=HexStr(self.data))],
        )


class AllHooks(msgspec.Struct):
    before_settle: list[InteractionData]
    after_settle: list[InteractionData]

    @property
    def hooks_hash(self) -> str:
        if len(self.after_settle) == 0 and len(self.before_settle) == 0:
            return "0x0000000000000000000000000000000000000000000000000000000000000000"
        keccak_hash = w3.keccak(hexstr=self.hooks_data)
        return keccak_hash.hex()

    @property
    def hooks_data(self) -> str:
        if len(self.after_settle) == 0 and len(self.before_settle) == 0:
            return "0x"
        hooks = [
            [self._flatten_hooks(h) for h in self.before_settle],
            [self._flatten_hooks(h) for h in self.after_settle],
        ]
        args_types = [collapse_if_tuple(cast(dict[str, Any], arg)) for arg in HASH_HOOKS_ABI["inputs"]]
        hooks_encoded = w3.codec.encode(args_types, [hooks])
        return hooks_encoded.hex()

    def _flatten_hooks(self, h: InteractionData) -> tuple[bool, str, int, str]:
        return h.result, h.to, h.value, h.data

    def to_blockchain_args(self) -> list[list[dict[str, Any]]]:
        return [
            [interaction.to_ws() for interaction in self.before_settle],
            [interaction.to_ws() for interaction in self.after_settle],
        ]


class InteractionDetails(msgspec.Struct):
    data: InteractionData
    gas: int

    def to_ws(self) -> dict:
        return {
            "data": self.data.to_ws(),
            "gas": self.gas,
        }

    @staticmethod
    def from_ws(data: dict) -> InteractionDetails:
        return InteractionDetails(
            data=InteractionData.from_ws(data["data"]),
            gas=data["gas"],
        )


class QuoteRequest(msgspec.Struct):
    quote_id: str
    order_type: OrderType
    base_settle_gas: int
    approval_type: ApprovalType
    taker: str
    receiver: str
    expiry: int
    exclusivity_deadline: int  # if block.timestamp > exclusivityDeadline, then order can be executed by any executor
    nonce: int
    slippage: Decimal
    hooks_data: str  # encoded hooks into bytes
    partner_info: int  # encoded partnerInfo into bytes
    sell_tokens: list[TokenAmount]
    buy_tokens: list[TokenAmount]
    native_token_price: float
    exclude_fee: bool = False
    source: str | None = None
    gasless: bool = False

    @property
    def usd_prices(self) -> dict[str, float]:
        prices = {}
        for token in self.sell_tokens + self.buy_tokens:
            if token.usd_price:
                prices[token.address] = token.usd_price

        prices[NATIVE_TOKEN_ADDRESS] = self.native_token_price
        return prices

    @property
    def using_permit2(self) -> bool:
        return self.approval_type == ApprovalType.Permit2

    def to_ws(self) -> dict[str, Any]:
        data: dict[str, Any] = decode(encode(self))
        data["sell_tokens"] = [token.to_ws() for token in self.sell_tokens]
        data["buy_tokens"] = [token.to_ws() for token in self.buy_tokens]
        data["nonce"] = str(self.nonce)
        data["partner_info"] = str(self.partner_info)
        data["slippage"] = float(self.slippage)
        del data["gasless"]
        return data

    @staticmethod
    def from_ws(data: dict, gasless: bool) -> QuoteRequest:
        return QuoteRequest(
            order_type=OrderType(data["order_type"]),
            quote_id=data["quote_id"],
            base_settle_gas=data["base_settle_gas"],
            approval_type=ApprovalType(data["approval_type"]),
            taker=data["taker"],
            receiver=data["receiver"],
            expiry=data["expiry"],
            exclusivity_deadline=data["exclusivity_deadline"],
            nonce=int(data["nonce"]),
            partner_info=int(data["partner_info"]),
            hooks_data=data["hooks_data"],
            slippage=Decimal(str(data["slippage"])),
            buy_tokens=[TokenAmount.from_ws(token) for token in data["buy_tokens"]],
            sell_tokens=[TokenAmount.from_ws(token) for token in data["sell_tokens"]],
            native_token_price=data["native_token_price"],
            exclude_fee=bool(data.get("exclude_fee")),
            gasless=gasless,
            source=data.get("source"),
        )

    @property
    def order_sell_tokens(self) -> list[TokenAmount]:
        """
        tokens formatted as required for the jam order object
        """
        return merge_tokens(self.sell_tokens)

    @property
    def order_buy_tokens(self) -> list[TokenAmount]:
        """
        tokens formatted as required for the jam order object
        """
        return merge_tokens(self.buy_tokens)


class QuoteResponse(msgspec.Struct):
    quote_id: str  # Quote ID of the request
    amounts: list[TokenAmountResponse]  # Output amounts
    fee: int  # Estimated fee in native token
    executor: str

    def to_ws(self) -> dict[str, Any]:
        msg: dict[str, Any] = {
            "quote_id": self.quote_id,
            "amounts": [amount.to_ws() for amount in self.amounts],
            "fee": str(self.fee),
            "executor": self.executor,
        }
        return msg

    @staticmethod
    def from_ws(msg: dict[str, Any]) -> QuoteResponse:
        amounts: list[TokenAmountResponse] = []
        for amount in msg["amounts"]:
            amounts.append(TokenAmountResponse(address=amount["address"], amount=int(amount["amount"])))
        return QuoteResponse(
            quote_id=msg["quote_id"],
            amounts=amounts,
            fee=int(msg["fee"]),
            executor=msg["executor"],
        )


class TakerQuoteResponse(QuoteResponse):
    interactions: list[InteractionDetails]
    balance_recipient: str

    def to_ws(self) -> dict:
        return {
            "quote_id": self.quote_id,
            "amounts": [amount.to_ws() for amount in self.amounts],
            "fee": str(self.fee),
            "executor": self.executor,
            "interactions": [interaction.to_ws() for interaction in self.interactions] if self.interactions else None,
            "balance_recipient": self.balance_recipient,
        }

    @staticmethod
    def from_ws(msg: dict[str, Any]) -> TakerQuoteResponse:
        amounts: list[TokenAmountResponse] = []
        for amount in msg["amounts"]:
            amounts.append(TokenAmountResponse(address=amount["address"], amount=int(amount["amount"])))
        return TakerQuoteResponse(
            quote_id=msg["quote_id"],
            amounts=amounts,
            fee=int(msg["fee"]),
            executor=msg["executor"],
            interactions=[InteractionDetails.from_ws(interaction) for interaction in msg["interactions"]],
            balance_recipient=msg["balance_recipient"],
        )


class ExecuteRequest(msgspec.Struct):
    quote_id: str
    signature: str
    min_amounts: list[TokenAmountResponse]  # User min amounts
    contract_min_amounts: list[TokenAmountResponse]  # Real min amounts

    def to_ws(self) -> dict:
        data = {
            "quote_id": self.quote_id,
            "signature": self.signature,
            "min_amounts": [amount.to_ws() for amount in self.min_amounts],
        }
        if self.contract_min_amounts:
            data["contract_min_amounts"] = [amount.to_ws() for amount in self.contract_min_amounts]
        return data

    @staticmethod
    def from_ws(data: dict) -> ExecuteRequest:
        min_amounts = [TokenAmountResponse.from_ws(amount) for amount in data["min_amounts"]]
        contract_min_amounts = (
            [TokenAmountResponse.from_ws(amount) for amount in data["contract_min_amounts"]]
            if data.get("contract_min_amounts")
            else []
        )
        return ExecuteRequest(
            quote_id=data["quote_id"],
            signature=data["signature"],
            min_amounts=min_amounts,
            contract_min_amounts=contract_min_amounts,
        )


class ExecuteResponse(msgspec.Struct):
    quote_id: str

    def to_ws(self) -> dict:
        return {"quote_id": self.quote_id}

    @staticmethod
    def from_ws(data: dict) -> ExecuteResponse:
        return ExecuteResponse(quote_id=data["quote_id"])


class QuoteErrorType(Enum):
    Unavailable = "unavailable"  # Unavailable to provide quotes
    NotSupported = "not_supported"  # Type of order or tokens not supported
    GasExceedsSize = "gas_exceeds_size"  # Order size is too small to cover fee
    Unknown = "unknown"  # Unknown error
    Timeout = "timeout"  # Solver took too long to respond


class ExecuteErrorType(Enum):
    Reject = "reject"  # Rejected executing the order
    Timeout = "timeout"  # Solver took too long to respond


class BaseError(msgspec.Struct):
    quote_id: str
    error_type: Enum
    error_msg: str | None = None


class QuoteError(BaseError):
    error_type: QuoteErrorType

    @staticmethod
    def from_ws(data: dict) -> QuoteError:
        return QuoteError(
            quote_id=data["quote_id"], error_type=QuoteErrorType(data["error_type"]), error_msg=data["error_msg"]
        )


class ExecuteError(BaseError):
    error_type: ExecuteErrorType

    @staticmethod
    def from_ws(data: dict) -> ExecuteError:
        return ExecuteError(
            quote_id=data["quote_id"], error_type=ExecuteErrorType(data["error_type"]), error_msg=data["error_msg"]
        )


class CachedQuote(msgspec.Struct):
    chain_id: int
    request: QuoteRequest
    response: QuoteResponse


class SolverConnection(BaseModel):
    name: str
    auth: str
    url: str


class Message(msgspec.Struct):
    code: str
    text: str | None


# ---------------------------------------------------------------------------- #
#                                    Schemas                                   #
# ---------------------------------------------------------------------------- #
class MessageTopics(Enum):
    websocket = "websocket"  # for websocket connection
    quote = "quote"
    taker_quote = "taker_quote"
    execute_order = "execute_order"


class MessageTypes(Enum):
    error = "error"
    response = "response"
    request = "request"
    update = "update"
    success = "success"


class BaseJAMSchema(msgspec.Struct):
    chain_id: int
    msg_topic: MessageTopics
    msg_type: MessageTypes
    msg: Any


class MessageSchema(msgspec.Struct):
    chain_id: int
    msg_topic: MessageTopics
    msg_type: MessageTypes
    msg: Message


# ---------------------------------------------------------------------------- #
#                                     Utils                                    #
# ---------------------------------------------------------------------------- #


def merge_tokens(tokens: list[TokenAmount]) -> list[TokenAmount]:
    """
    Combine split tokens

    Args:
        tokens (list[TokenAmount]): list of tokens

    Returns:
        _type_: merged tokens
    """
    merged_tokens: dict[str, TokenAmount] = {}
    for token in tokens:
        if token.address in merged_tokens and token.amount:
            current_amount = merged_tokens[token.address].amount
            if current_amount:
                merged_tokens[token.address].amount = current_amount + token.amount
        else:
            merged_tokens[token.address] = TokenAmount(
                address=token.address, amount=token.amount, usd_price=token.usd_price
            )
    return list(merged_tokens.values())
