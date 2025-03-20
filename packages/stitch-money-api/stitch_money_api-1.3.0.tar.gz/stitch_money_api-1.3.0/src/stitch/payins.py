import base64
import json
from typing import Union, Dict
from stitch.services.api import ApiClient
from stitch.utils.types import *


class Wallets:
    """
    A class to process wallet payments using the Stitch API.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        gateway_merchant_id: str,
    ):
        """Initialize the Wallets instance with necessary credentials.

        Parameters
        ----------
        client_id : str
            The client ID for API authentication.
        client_secret : str
            The client secret for API authentication.
        gateway_merchant_id : str
            The merchant ID associated with wallet providers.
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._gateway_merchant_id = gateway_merchant_id
        self._client = ApiClient(client_id, client_secret)

    def verify(
        self,
        wallet: Wallet,
        quantity: float,
        currency: Currency,
        url: str,
        display_name: str,
        initiative_context: str,
    ) -> Session:
        """Verify the merchant session for a specific wallet provider.

        Parameters
        ----------
        wallet : Wallet
            The wallet provider
        quantity : float
            The transaction amount.
        currency : Currency
            The currency of the transaction in IS04127 format.
        url : str
            The validation (Apple) or callback (Samsung) URL.
        display_name : str
            The canonical display name of the merchant.
        initiative_context : str
            The fully-qualified domain name

        Returns
        -------
        Session
            The session data returned by the verification process.

        Raises
        ------
        Exception
            If the wallet type is not supported.
        """
        if wallet == Wallet.APPLE_PAY:
            mutation_input = ValidateApplePayMerchantInput(
                merchant_identifier=self._gateway_merchant_id,
                validation_url=url,
                display_name=display_name,
                initiative_context=initiative_context,
            )
            session = self._client.validate_apple_pay_merchant(mutation_input)
            return session
        elif wallet == Wallet.SAMSUNG_PAY:
            mutation_input = VerifySamsungPayInput(
                amount=Money(quantity=quantity, currency=currency.name),
                callback_url=url,
                display_name=display_name,
                initiative_context=initiative_context,
            )
            session = self._client.verify_samsung_pay(mutation_input)
            return session
        else:
            raise Exception("Method not supported")

    def create(
        self,
        wallet: Wallet,
        token: Union[str, Dict],
        quantity: float,
        currency: Currency,
        external_reference: str,
        nonce: str,
    ) -> Transaction:
        """Create a transaction for a specific wallet provider.

        Parameters
        ----------
        wallet : Wallet
            The wallet provider use for the transaction.
        token : Union[str, Dict]
            The payment token, which can be a string or a dictionary depending on the wallet type.
        quantity : float
            The transaction amount.
        currency : Currency
            The currency of the transaction.
        external_reference : str
            An external reference for the transaction.
        nonce : str
            A unique nonce for the transaction.

        Returns
        -------
        Transaction
            The resulting transaction object.

        Raises
        ------
        Exception
            If the wallet type is not supported or if token is of incorrect type for the wallet.
        """
        if wallet == Wallet.APPLE_PAY:
            if not isinstance(token, dict):
                raise Exception("Token must be of type Dict for Apple Pay")

            mutation_input = InitiateTransactionInput(
                amount=Money(quantity=quantity, currency=currency.name),
                external_reference=external_reference,
                nonce=nonce,
                payment_methods={
                    "applePay": {
                        "network": "Visa",
                        "displayName": "Apple",
                        "type": "credit",
                    }
                },
                token=base64.b64encode(
                    json.dumps(token["paymentData"]).encode()
                ).decode(),
            )

            transaction = self._client.initiate_wallet_transaction(mutation_input)
            return transaction
        elif wallet == Wallet.SAMSUNG_PAY:
            mutation_input = InitiateTransactionInput(
                amount=Money(quantity=quantity, currency=currency.name),
                external_reference=external_reference,
                nonce=nonce,
                payment_methods={"samsungPay": {}},
            )

            if isinstance(token, str):
                mutation_input.payment_methods["samsungPay"]["referenceId"] = token
            else:
                mutation_input.token = base64.b64encode(
                    json.dumps(token).encode()
                ).decode()

            transaction = self._client.initiate_wallet_transaction(mutation_input)
            return transaction
        elif wallet == Wallet.GOOGLE_PAY:
            if not isinstance(token, str):
                raise Exception("Token must be of type string for Google Pay")

            mutation_input = InitiateTransactionInput(
                amount=Money(quantity=quantity, currency=currency.name),
                external_reference=external_reference,
                nonce=nonce,
                payment_methods={"googlePay": {}},
                token=base64.b64encode(token.encode()).decode(),
            )

            transaction = self._client.initiate_wallet_transaction(mutation_input)
            return transaction


class Stitch:
    """
    A class to process payments using the Stitch API.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
    ):
        """Initialize the Stitch instance with required secrets.

        Parameters
        ----------
        client_id : str
            The client ID for API authentication.
        client_secret : str
            The client secret for API authentication.
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._client = ApiClient(client_id, client_secret)

    def initiate_card_transaction(
        self,
        quantity: float,
        currency: str,
        external_reference: str,
        nonce: str,
        card: Dict,
    ) -> Transaction:
        mutation_input = InitiateTransactionInput(
            amount=Money(quantity=quantity, currency=currency),
            external_reference=external_reference,
            nonce=nonce,
            payment_methods={
                "card": {
                    "cardInput": {
                        "cardUsageType": "onceOff",
                        "cardholderName": card.cardholder_name,
                        "expiryYear": card.expiry.year,
                        "expiryMonth": card.expiry.month,
                        "bin": card.bin,
                        "last4": card.last4,
                        "reacted": {
                            "redactedCardNumber": card.pan,
                            "redactedSecurityCode": card.cvv,
                        },
                    }
                }
            },
        )

        transaction = self._client.initiate_card_transaction(mutation_input)
        return transaction

    def initiate_card_refund_transaction(
        self,
        original_payment_id: str,
        quantity: float,
        currency: str,
        external_reference: str,
        nonce: str,
        reason: str,
    ) -> Transaction:
        mutation_input = RefundTransactionInitiateInput(
            amount=Money(quantity=quantity, currency=currency),
            external_reference=external_reference,
            nonce=nonce,
            reason=reason,
            original_payment_id=original_payment_id,
        )

        transaction = self._client.initiate_refund_transaction(mutation_input)
        return transaction

    def query_transaction(
        self, external_reference: Optional[str] = None, nonce: Optional[str] = None
    ) -> list[Transaction]:
        query_input = QueryPaymentTransactionInput(
            external_reference=external_reference,
            nonce=nonce,
        )
        transactions = self._client.query_payment_transaction(query_input)
        return transactions
