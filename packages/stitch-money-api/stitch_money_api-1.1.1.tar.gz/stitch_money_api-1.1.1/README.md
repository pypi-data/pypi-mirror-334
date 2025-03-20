# stitch-money-api
A Python package for processing payments via the Stitch API. 
For the complete integration guide, visit [docs.stitch.money](http://localhost:3000/payment-products/payins/wallets/introduction).

# Installation

```bash
$ pip3 install stitch-money-api
```

## Usage

### Payment Initiation

```python
from pyramid.view import view_config
from pyramid.response import Response
from stitch.payins import Wallets
from stitch.utils.types import Wallet, Currency, Transaction
import json
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("STITCH_CLIENT_ID")
client_secret = os.getenv("STITCH_CLIENT_SECRET")

if not client_id or not client_secret:
    raise EnvironmentError(
        "Missing STITCH_CLIENT_ID or STITCH_CLIENT_SECRET in environment variables"
    )

sdk = Wallets(client_id, client_secret, "merchant.money.stitch")


@view_config(route_name="create", request_method="POST", renderer="json")
def create_apple_pay_payment(request) -> Response:
    data = request.json_body
    payment_token = data.get("payment_token")

    if not payment_token:
        return Response(json_body={"error": "Missing payment_token"}, status=400)

    nonce = str(uuid.uuid4())
    quantity = 1
    currency = Currency.ZAR
    reference = "StitchTest"

    transaction: Transaction = sdk.create(
        Wallet.APPLE_PAY, payment_token, quantity, currency, nonce, reference
    )

    return Response(json_body={"transaction": transaction}, status=200)
```


### Merchant Verification
Note this is not required for mobile (native) app integrations. 

```python
from pyramid.view import view_config
from pyramid.response import Response
from stitch.payins import Wallets
from stitch.utils.types import Wallet, Currency, Session
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("STITCH_CLIENT_ID")
client_secret = os.getenv("STITCH_CLIENT_SECRET")

if not client_id or not client_secret:
    raise EnvironmentError(
        "Missing STITCH_CLIENT_ID or STITCH_CLIENT_SECRET in environment variables"
    )

sdk = Wallets(client_id, client_secret, "merchant.money.stitch")


@view_config(route_name="verify", request_method="POST", renderer="json")
def verify_apple_pay_merchant(request) -> Response:
    data = request.json_body
    verification_url = data.get(
        "verification_url"
    )  # 'https://apple-pay-gateway.apple.com/paymentservices/startSession'
    initiative_context = data.get("initiative_context")  # secure.stitch.money (FQDN)

    if not verification_url or not initiative_context:
        return Response(
            json_body={"error": "Missing verification_url or initiative_context"},
            status=400,
        )

    quantity = 1
    currency = Currency.ZAR
    display_name = "Stitch"

    session: Session = sdk.verify(
        Wallet.APPLE_PAY,
        quantity,
        currency,
        verification_url,
        display_name,
        initiative_context,
    )

    return Response(json_body={"session": session}, status=200)
```

# License

The stitch-money-api package is open source and available under the MIT license. See the LICENSE file for more information.