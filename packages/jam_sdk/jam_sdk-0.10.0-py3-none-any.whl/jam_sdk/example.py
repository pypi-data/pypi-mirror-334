import asyncio

from web3.constants import ADDRESS_ZERO

from jam_sdk.constants import JAM_SETTLEMENT_CONTRACT
from jam_sdk.solver.base import BaseSolver
from jam_sdk.solver.solver_types import (
    CachedQuote,
    ExecuteError,
    ExecuteRequest,
    ExecuteResponse,
    InteractionData,
    InteractionDetails,
    QuoteError,
    QuoteRequest,
    QuoteResponse,
    SolverConnection,
    TakerQuoteResponse,
    TokenAmountResponse,
)


class MySolver(BaseSolver):
    async def get_quote(self, chain_id: int, request: QuoteRequest) -> QuoteResponse | QuoteError:
        return QuoteResponse(
            quote_id=request.quote_id,
            amounts=[
                TokenAmountResponse(address="0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174", amount=100000)
            ],  # Output token amount
            fee=50000000000000000,  # Fee in wei
            executor=ADDRESS_ZERO,
        )

    async def get_taker_quote(self, chain_id: int, request: QuoteRequest) -> TakerQuoteResponse | QuoteError:
        return TakerQuoteResponse(
            quote_id=request.quote_id,
            amounts=[
                TokenAmountResponse(address="0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174", amount=100000)
            ],  # Output token amount
            fee=0,  # Fee in wei
            executor=request.taker,
            interactions=[  # A set of calls to make on chain in order to fulfil the quote
                InteractionDetails(
                    data=InteractionData(
                        result=True,
                        to="0x0000",
                        value=0,
                        data="0x00000000000",  # Whether the interaction must succeed
                    ),
                    gas=500000,
                ),
            ],
            balance_recipient=JAM_SETTLEMENT_CONTRACT[chain_id],  # or Solver contract address
        )

    async def execute(self, request: ExecuteRequest, quote_cache: CachedQuote) -> ExecuteResponse | ExecuteError:
        interactions = [  # A set of calls to make on chain in order to fulfil the quote
            InteractionData(
                result=True,
                to="0x0000",
                value=0,
                data="0x00000000000",  # Whether the interaction must succeed
            )
        ]
        account = self.web3.eth.account.from_key("<a private key>")
        settle_tx = await self.build_settle(
            quote_cache.request,
            quote_cache.response,
            interactions,
            request,
            self.jam_contract.address,  # The recipient of user sell tokens. Can be your own solver contract
            {"from": account.address},
        )
        signed_transaction = account.sign_transaction(settle_tx)
        await self.web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        return ExecuteResponse(quote_id=request.quote_id)


if __name__ == "__main__":
    connection = SolverConnection(
        name="my-solver", auth="mypassword123", url="wss://api-test.bebop.xyz/jam/polygon/solver"
    )  # Obtain from Bebop
    solver = MySolver(chain_id=137, rpc_url="https://polygon-rpc.com", connection=connection)
    asyncio.run(solver.start())
