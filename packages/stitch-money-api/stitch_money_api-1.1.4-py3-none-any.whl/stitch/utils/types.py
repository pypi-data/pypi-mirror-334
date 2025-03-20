
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


Wallet = Enum('Wallet', ['APPLE_PAY', 'SAMSUNG_PAY', 'GOOGLE_PAY'])
Currency = Enum('Currency', ['ZAR'])


@dataclass
class Money:
    quantity: float
    currency: str


@dataclass
class ValidateApplePayMerchantInput:
    merchant_identifier: str
    validation_url: str
    display_name: str
    initiative_context: str


@dataclass
class VerifySamsungPayInput:
    amount: Money
    callback_url: str
    display_name: str
    initiative_context: str


@dataclass
class InitiateTransactionInput:
    amount: Money
    external_reference: str
    nonce: str
    payment_methods: Dict
    token: Optional[str] = None

@dataclass
class RefundTransactionInitiateInput:
    original_payment_id: str
    amount: Money
    external_reference: str
    nonce: str
    reason: str

@dataclass
class Transaction:
    id: str
    amount: Money
    external_reference: Optional[str]
    nonce: str
    status: str
    status_reason: Optional[str]


Session = Dict[str, Any]
