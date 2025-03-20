from decimal import Decimal

from eth_account.messages import SignableMessage, _hash_eip191_message, encode_typed_data
from eth_utils.address import to_checksum_address

from jam_sdk.constants import (
    HUNDRED_PERCENT_BPS,
    JAM_BALANCE_MANAGER,
    JAM_ORDER_TYPES,
    JAM_SETTLEMENT_CONTRACT,
    PERMIT2_ADDRESS,
    PERMIT2_WITH_JAM_ORDER_TYPES,
)


def apply_slippage(amount: int, slippage: Decimal) -> int:
    min_amount = int(Decimal(amount) * (Decimal(1) - (slippage / Decimal(100))))
    return min_amount


def get_fee_amount(amount: int, fee_bps: int) -> int:
    fee_amount = amount * fee_bps // HUNDRED_PERCENT_BPS
    return fee_amount


def hash_jam_order(chain_id: int, order: dict) -> str:
    jam_settlement_domain: dict = {
        "name": "JamSettlement",
        "version": "2",
        "chainId": chain_id,
        "verifyingContract": JAM_SETTLEMENT_CONTRACT[chain_id],
    }
    structured_data: SignableMessage = encode_typed_data(jam_settlement_domain, JAM_ORDER_TYPES, order)
    return _hash_eip191_message(structured_data).hex()


def hash_permit2_with_witness(chain_id: int, permit2_with_order_witness: dict) -> str:
    jam_settlement_domain: dict = {
        "name": "Permit2",
        "chainId": chain_id,
        "verifyingContract": PERMIT2_ADDRESS[chain_id],
    }
    structured_data: SignableMessage = encode_typed_data(
        jam_settlement_domain, PERMIT2_WITH_JAM_ORDER_TYPES, permit2_with_order_witness
    )
    return _hash_eip191_message(structured_data).hex()


def hash_permit2_jam_order(chain_id: int, order: dict) -> str:
    permit2_with_order_witness = {
        "permitted": [
            {"token": token, "amount": amount}
            for token, amount in zip(order["sellTokens"], order["sellAmounts"], strict=True)
        ],
        "spender": JAM_BALANCE_MANAGER[chain_id],
        "nonce": order["nonce"],
        "deadline": order["expiry"],
        "witness": order,
    }
    return hash_permit2_with_witness(chain_id, permit2_with_order_witness)


def hash_tosign_field(chain_id: int, to_sign: dict) -> str:
    if "witness" in to_sign:
        return hash_permit2_with_witness(chain_id, to_sign)
    return hash_jam_order(chain_id, to_sign)


def decode_partner_info(partner_info_packed: int) -> tuple[int, int, str]:
    """Decodes packed PartnerInfo into protocol_fee_bps, partner_fee_bps, partner_address"""
    protocol_fee_bps = partner_info_packed & 0xFFFF
    partner_fee_bps = (partner_info_packed >> 16) & 0xFFFF
    partner_address_int = (partner_info_packed >> 32) & ((1 << 160) - 1)
    partner_address = "0x" + partner_address_int.to_bytes(20, "big").hex()
    partner_address = to_checksum_address(partner_address)

    if partner_fee_bps + protocol_fee_bps >= HUNDRED_PERCENT_BPS:
        raise ValueError("Invalid Fee Percentage, total fees must be less than 100%")
    if not (partner_fee_bps > 0 or (partner_fee_bps == 0 and partner_address_int == 0)):
        raise ValueError("Invalid Partner Address, must be 0x0 if partner fee is 0")
    return protocol_fee_bps, partner_fee_bps, partner_address
