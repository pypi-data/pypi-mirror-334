import json
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from stitch.utils.types import *
import time


class ApiClient:
    """
    A client for interacting with the Stitch API, including authentication and GraphQL operations.

    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        base_url: str = "https://api.stitch.money",
    ):
        """Initialize the class with client credentials and obtain an access token.

        Parameters
        ----------
        client_id : str
            The client ID for API authentication.
        client_secret : str
            The client secret for API authentication.
        base_url : str, optional
            The base URL for the Stitch API. Defaults to "https://api.stitch.money".
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._base_url = base_url
        self._token_url = "https://secure.stitch.money/connect/token"
        self._token = None
        self._token_exp = None
        self._client = None
        self.fetch_token()
        self.get_graphql_client(self._token)

    def fetch_token(self, scopes=["client_paymentrequest client_refund"]) -> None:
        """Fetch an OAuth token using client credentials.

        Parameters
        ----------
        scopes : list of str, optional
            The list of OAuth scopes to request. Defaults to ["client_paymentrequest client_refund"].

        Raises
        ------
        Exception
            If the authentication fails.
        """
        body = {
            "grant_type": "client_credentials",
            "client_id": self._client_id,
            "scope": " ".join(scopes),
            "audience": self._token_url,
            "client_secret": self._client_secret,
        }

        response = requests.post(
            self._token_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=body,
        )

        body = response.json()

        try:
            self._token = body["access_token"]
            self._token_exp = body["expires_in"] + round(time.time())
        except KeyError:
            raise Exception(f"Unable to authenticate: {body}")

    def get_graphql_client(self, token: str) -> None:
        """Initialize the GraphQL client with the provided OAuth token.

        Parameters
        ----------
        token : str
            The OAuth token used for authenticated API requests.
        """
        transport = RequestsHTTPTransport(
            url=f"{self._base_url}/graphql",
            headers={"Authorization": f"Bearer {token}"},
            use_json=True,
            verify=True,
        )
        self._client = Client(transport=transport, fetch_schema_from_transport=False)

    def initiate_wallet_transaction(
        self, input: InitiateTransactionInput
    ) -> Transaction:
        """Initiate a wallet transaction using the Stitch API.

        Parameters
        ----------
        input : InitiateTransactionInput
            The input data required to initiate the transaction.

        Returns
        -------
        Transaction
            The resulting transaction object.

        Raises
        ------
        Exception
            If the transaction initiation fails or returns an unexpected response.
        """
        if self.token_requires_refresh():
            self.fetch_token()

        document = gql(
            """
            mutation initiateWalletTransaction($input: TransactionInitiateInput!) {
                initiateTransaction(input: $input) {
                    __typename
                    id
                    ... on ApplePayTransaction {
                        amount
                        nonce
                        state {
                            ... on TransactionPending {
                                __typename
                                reason
                            }
                            ... on TransactionSuccess {
                                __typename
                            }
                            ... on TransactionFailure {
                                __typename
                                reason
                            }
                        }
                    }
                    ... on SamsungPayTransaction {
                        amount
                        nonce
                        externalReference
                        state {
                            ... on TransactionPending {
                                __typename
                                reason
                            }
                            ... on TransactionSuccess {
                                __typename
                            }
                            ... on TransactionFailure {
                                __typename
                                reason
                            }
                        }
                    }
                    ... on GooglePayTransaction {
                        amount
                        nonce
                        externalReference
                        state {
                            ... on TransactionPending {
                                __typename
                                reason
                            }
                            ... on TransactionSuccess {
                                __typename
                            }
                            ... on TransactionFailure {
                                __typename
                                reason
                            }
                        }
                    }
                }
            }
        """
        )

        params = {
            "input": {
                "amount": {
                    "quantity": input.amount.quantity,
                    "currency": input.amount.currency,
                },
                "externalReference": input.external_reference,
                "nonce": input.nonce,
                "paymentMethods": input.payment_methods,
                "token": input.token,
            },
        }

        try:
            result = self._client.execute(document, variable_values=params)
            response = result["initiateTransaction"]
            if not response or response["__typename"] not in [
                "ApplePayTransaction",
                "SamsungPayTransaction",
                "GooglePayTransaction",
            ]:
                raise Exception(f"Failed to initiate transaction\n{response}")
            return Transaction(
                id=response["id"],
                amount=Money(
                    quantity=response["amount"]["quantity"],
                    currency=response["amount"]["currency"],
                ),
                external_reference=(
                    response["externalReference"]
                    if "externalReference" in response
                    else None
                ),
                nonce=response["nonce"],
                status=response["state"]["__typename"],
                status_reason=(
                    response["state"]["reason"]
                    if "reason" in response["state"]
                    else None
                ),
            )
        except Exception as error:
            raise Exception(str(error))

    def initiate_card_transaction(self, input: InitiateTransactionInput) -> Transaction:
        """Initiate a card transaction using the Stitch API.

        Parameters
        ----------
        input : InitiateTransactionInput
            The input data required to initiate the transaction.

        Returns
        -------
        Transaction
            The resulting transaction object.

        Raises
        ------
        Exception
            If the transaction initiation fails or returns an unexpected response.
        """
        if self.token_requires_refresh():
            self.fetch_token()

        document = gql(
            """
            mutation initiateCardTransaction($input: TransactionInitiateInput!) {
                initiateTransaction(input: $input) {
                    __typename
                    id
                    ... on CardTransaction {
                        amount
                        nonce
                        state {
                            ... on TransactionPending {
                                __typename
                                reason
                            }
                            ... on TransactionSuccess {
                                __typename
                            }
                            ... on TransactionFailure {
                                __typename
                                reason
                            }
                        }
                    }
                }
            }
        """
        )

        params = {
            "input": {
                "amount": {
                    "quantity": input.amount.quantity,
                    "currency": input.amount.currency,
                },
                "externalReference": input.external_reference,
                "nonce": input.nonce,
                "paymentMethods": input.payment_methods,
                "token": input.token,
            },
        }

        try:
            result = self._client.execute(document, variable_values=params)
            response = result["initiateTransaction"]
            if not response or response["__typename"] not in ["CardTransaction"]:
                raise Exception(f"Failed to initiate transaction\n{response}")
            return Transaction(
                id=response["id"],
                amount=Money(
                    quantity=response["amount"]["quantity"],
                    currency=response["amount"]["currency"],
                ),
                external_reference=(
                    response["externalReference"]
                    if "externalReference" in response
                    else None
                ),
                nonce=response["nonce"],
                status=response["state"]["__typename"],
                status_reason=(
                    response["state"]["reason"]
                    if "reason" in response["state"]
                    else None
                ),
            )
        except Exception as error:
            raise Exception(str(error))

    def initiate_refund_transaction(
        self, input: RefundTransactionInitiateInput
    ) -> Transaction:
        """Initiate a card or wallet refund using the Stitch API.

        Parameters
        ----------
        input : RefundTransactionInitiateInput
            The input data required to initiate the refund transaction.

        Returns
        -------
        Transaction
            The resulting transaction object.

        Raises
        ------
        Exception
            If the transaction initiation fails or returns an unexpected response.
        """
        if self.token_requires_refresh():
            self.fetch_token()

        document = gql(
            """
            mutation initiateRefundTransaction($input: RefundTransactionInitiateInput!) {
                refundTransactionInitiate(input: $input) {
                    __typename
                    id
                    amount
                    nonce
                    state {
                        ... on TransactionPending {
                            __typename
                            reason
                        }
                        ... on TransactionSuccess {
                            __typename
                        }
                        ... on TransactionFailure {
                            __typename
                            reason
                        }
                }
            }
        }
        """
        )

        params = {
            "input": {
                "originalPaymentId": input.original_payment_id,
                "refundInput": {
                    "amount": {
                        "quantity": input.amount.quantity,
                        "currency": input.amount.currency,
                    },
                    "externalReference": input.external_reference,
                    "nonce": input.nonce,
                    "reason": input.reason,
                },
            },
        }

        try:
            result = self._client.execute(document, variable_values=params)
            response = result["refundTransactionInitiate"]
            if not response or response["__typename"] not in [
                "CardRefundTransaction",
                "WalletRefundTransaction",
            ]:
                raise Exception(f"Failed to initiate refund transaction\n{response}")
            return Transaction(
                id=response["id"],
                amount=Money(
                    quantity=response["amount"]["quantity"],
                    currency=response["amount"]["currency"],
                ),
                external_reference=(
                    response["externalReference"]
                    if "externalReference" in response
                    else None
                ),
                nonce=response["nonce"],
                status=response["state"]["__typename"],
                status_reason=(
                    response["state"]["reason"]
                    if "reason" in response["state"]
                    else None
                ),
            )
        except Exception as error:
            raise Exception(str(error))

    def validate_apple_pay_merchant(
        self, input: ValidateApplePayMerchantInput
    ) -> Session:
        """Validate an Apple Pay merchant using the Stitch API.

        Parameters
        ----------
        input : ValidateApplePayMerchantInput
            The input data required to validate the Apple Pay merchant.

        Returns
        -------
        Session
            The resulting session data in JSON format.

        Raises
        ------
        Exception
            If the merchant validation fails or returns an unexpected response.
        """
        if self.token_requires_refresh():
            self.fetch_token()

        document = gql(
            """
            mutation Verify(
                $input: ValidateApplePayMerchantInput!
            ) {
            validateApplePayMerchant(input: $input) {
                __typename
                sessionData
            }
        }
        """
        )

        params = {
            "input": {
                "merchantIdentifier": input.merchant_identifier,
                "validationUrl": input.validation_url,
                "displayName": input.display_name,
                "initiative": "web",
                "initiativeContext": input.initiative_context,
            },
        }

        try:
            result = self._client.execute(document, variable_values=params)
            response = result["validateApplePayMerchant"]
            if not response or response["__typename"] not in [
                "ValidateApplePayMerchantPayload"
            ]:
                raise Exception(f"Failed to validate merchant\n{response}")
            return json.loads(response["sessionData"])
        except Exception as error:
            raise Exception(str(error))

    def verify_samsung_pay(self, input: VerifySamsungPayInput) -> Session:
        """Verify a Samsung Pay merchant using the Stitch API.

        Parameters
        ----------
        input : VerifySamsungPayInput
            The input data required to verify the Samsung Pay merchant.

        Returns
        -------
        Session
            The resulting merchant session data.

        Raises
        ------
        Exception
            If the merchant verification fails or returns an unexpected response.
        """
        if self.token_requires_refresh():
            self.fetch_token()

        document = gql(
            """
            mutation Verify(
                $input: VerifySamsungPayInput!
            ) {
            verifySamsungPay(input: $input) {
                __typename
                merchantSession {
                    id
                    href
                    encInfo {
                        keyId
                        mod
                        exp
                    }
                }
            }
        }
        """
        )

        params = {
            "input": {
                "amount": {
                    "quantity": input.amount.quantity,
                    "currency": input.amount.currency,
                },
                "callbackUrl": input.callback_url,
                "displayName": input.display_name,
                "initiativeContext": input.initiative_context,
            },
        }

        try:
            result = self._client.execute(document, variable_values=params)
            response = result["verifySamsungPay"]
            if not response or response["__typename"] not in [
                "VerifySamsungPayPayload"
            ]:
                raise Exception(f"Failed to validate merchant.\n{response}")
            return response["merchantSession"]
        except Exception as error:
            raise Exception(str(error))

    def query_payment_transaction(
        self, input: QueryPaymentTransactionInput
    ) -> list[Transaction]:
        """Query a transaction

        Parameters
        ----------
        input : QueryPaymentTransactionInput
            The input data required to query the transaction. Either an external reference or nonce must be supplied.

        Returns
        -------
        Transaction
            The resulting list of transactions that match the criteria.

        Raises
        ------
        Exception
            If the transaction initiation fails or returns an unexpected response.
        """
        if self.token_requires_refresh():
            self.fetch_token()

        document = gql(
            """
            query TransactionsForExternalReference($externalReference: String!) {
                client {
                    transactions(filter: {
                    externalReference: {
                        eq: $externalReference
                    }
                    }) {
                        edges {
                            node {
                                id
                                amount
                                state {
                                    __typename
                                }
                                externalReference
                                nonce
                            }
                        }

                    }
                }
                }
            """
        )

        params = {"externalReference": input.external_reference}

        try:
            result = self._client.execute(document, variable_values=params)
            edges = result["client"]["transactions"]["edges"]
            print(result)
            if not edges:
                raise Exception(f"Failed to query transactions\n{edges}")

            transactions = []

            for edge in edges:
                node = edge.get("node", {})  # Extract the transaction node
                transaction = Transaction(
                    id=node.get("id"),
                    amount=Money(
                        quantity=node.get("amount", {}).get("quantity"),
                        currency=node.get("amount", {}).get("currency"),
                    ),
                    external_reference=node.get("externalReference"),
                    nonce=node.get("nonce"),
                    status=node.get("state", {}).get("__typename"),
                    status_reason=node.get("state", {}).get("reason"),
                )
                transactions.append(transaction)

            return transactions
        except Exception as error:
            raise Exception(str(error))

    def token_requires_refresh(self) -> bool:
        """Check if the current OAuth token requires refreshing.

        Returns
        -------
        bool
            True if the token needs to be refreshed, False otherwise.
        """
        return round(time.time()) > self._token_exp
