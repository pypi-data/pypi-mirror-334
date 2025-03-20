# Pytterns
Pytterns is a Python library that provides an easy and intuitive way to use Design Patterns in your Python code.

## Implemented Design Patterns

### Strategy
The Strategy pattern allows the definition of a family of algorithms, encapsulating them and making them interchangeable at runtime.

#### Usage Example
```
from pytterns import strategy, load

@strategy("payment")
class CreditCardPayment:
    def check(self, method):
        return method == "credit_card"
    
    def execute(self):
        return "Processing payment via Credit Card"

@strategy("payment")
class PayPalPayment:
    def check(self, method):
        return method == "paypal"
    
    def execute(self):
        return "Processing payment via PayPal"

# Selecting strategy based on payment method
payment_strategy = load.strategy("payment").check("paypal").execute()
print(payment_strategy)  # Output: Processing payment via PayPal
```

### Chain of Responsibility
Chain of Responsibility is a behavioral design pattern that allows a request to be processed by a sequence of handlers. The order of the handlers will be defined in the decorator/annotation itself.

#### Usage Example
```
from pytterns import chain, load

@chain("auth_chain", order=1)
class Authenticator:
    def handle(self, request):
        if not request.get("authenticated", False):
            print("Authentication failed!")
            return  # Interrompe a cadeia aqui
        print("User authenticated")

@chain("auth_chain", order=2)
class Authorizer:
    def handle(self, request):
        if request.get("role") != "admin":
            print("Authorization failed!")
            return
        print("User authorized")

@chain("auth_chain", order=3)
class Logger:
    def handle(self, request):
        print(f"Logging request: {request}")

# Carregando a cadeia
auth_chain = load.chain("auth_chain")

# Simulando requisições
print("=== Request 1 ===")
auth_chain.handle({"authenticated": False, "role": "admin"})

print("\n=== Request 2 ===")
auth_chain.handle({"authenticated": True, "role": "user"})

print("\n=== Request 3 ===")
auth_chain.handle({"authenticated": True, "role": "admin"})
```

#### Expected Output
```
=== Request 1 ===
Authentication failed!

=== Request 2 ===
User authenticated
Authorization failed!

=== Request 3 ===
User authenticated
User authorized
Logging request: {'authenticated': True, 'role': 'admin'}
```