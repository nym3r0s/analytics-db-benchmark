from audioop import add
from dis import dis
import random
from faker import Faker
from faker_food import FoodProvider

fake = Faker()
fake.add_provider(FoodProvider)

def _randomDate():
    return fake.date_time_this_month().isoformat()

cancel_reasons = ['PARTNER', 'CUSTOMER', 'GLOVO']
partner_rating_reasons = [fake.word() for i in range(10)]
partner_rating_evaluations = ["POSITIVE", "NEGATIVE", "NEUTRAL"]


def createOrder(storeId, addressId):
    time = _randomDate()
    refunded = fake.boolean(10)
    price = fake.random_int(1000, 2000)
    status = "DELIVERED" if fake.boolean(90) else "CANCELLED"
    orderId = fake.random_int(1000000000, 1000000000000)
    order = {
        "acceptanceTime":
        time,
        "cancelReason":
        random.choice(cancel_reasons) if status == "CANCELLED" else None,
        "courierWaitingTimeInSeconds":
        fake.random_int(10, 100),
        "creationTime":
        time,
        "currency":
        "EUR",
        "dispatchingTime":
        time,
        "feedbackId":
        112233,
        "feedbackIds":
        [fake.random_int(1200, 1400)],
        "isPositiveRating":
        fake.boolean(70),
        "isRefunded":
        refunded,
        "orderId":
        orderId,
        "orderPreparationTimeInSeconds":
        fake.random_int(10, 100),
        "partnerRatingEvaluation":
        random.choice(partner_rating_reasons),
        "partnerRatingReasons":
        [random.choice(partner_rating_evaluations)],
        "pickUpTime":
        time,
        "refundedAmountInCents":
        0 if refunded else fake.random_int(10, 100),
        "servingTime":
        time,
        "status":
        status,
        "storeAddressId":
        addressId,
        "storeId":
        storeId,
        "totalProductPriceInCents":
        price,
        "totalProductsPriceInCents":
        price,
        "boughtProducts":
        _createBoughtProducts(storeId, addressId, orderId, time),
        "productIssues": 
        _createProductIssues()
    }
    return order


def _createBoughtProducts(storeId, addressId, orderId, dispatchingTime):
    boughtProductId = fake.random_int(1000000000, 1000000000000)
    products = []
    for i in range(fake.random_int(1, 5)):
        products.append({
            "storeId":
            storeId,
            "storeAddressId":
            addressId,
            "orderId":
            orderId,
            "dispatchingTime":
            dispatchingTime,
            "boughtProductId":
            boughtProductId,
            "externalId":
            fake.uuid4(),
            "name":
            fake.dish(),
            "price":
            fake.random_int(1000, 2000),
            "productId":
            fake.random_int(1000000000, 1000000000000),
            "quantity":
            fake.random_int(1, 10),
            "customizations":
            _createCustomizations(storeId, addressId, orderId, dispatchingTime,
                                 boughtProductId)
        })
    return products


def _createCustomizations(storeId, addressId, orderId, dispatchingTime,
                         boughtProductId):
    customizations = []
    for i in range(fake.random_int(1, 5)):
        customizations.append({
            "storeId": storeId,
            "storeAddressId": addressId,
            "orderId": orderId,
            "dispatchingTime": dispatchingTime,
            "boughtProductId": boughtProductId,
            "attributeId": fake.random_int(1000000000, 1000000000000),
            "externalId": fake.uuid4(),
            "name": fake.dish(),
            "priceImpact": fake.random_int(1, 10),
            "quantity": fake.random_int(1, 10)
        })
    return customizations

def _createProductIssues():
    issues = []
    for i in range(fake.random_int(1, 2)):
        prods = []
        for k in range(fake.random_int(1, 2)):
            prods.append({
                  "quantity" : fake.random_int(1, 10),
                  "name" : fake.dish(),
                  "externalId" : fake.uuid4(),
                  "boughtProductId" : fake.random_int(1000000000, 1000000000000)
            })
        issues.append({
            "optionId": fake.word(),
            "affectedProducts": prods
        })
    return issues