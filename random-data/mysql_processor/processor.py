from datetime import date, datetime, timedelta

import mysql_processor.queries as queries
from dateutil import parser
import numpy as np
import pandas as pd


def _toMySQLDateTime(isoDate):
    if (isoDate != None):
        return parser.parse(isoDate)
    return None


def _listToCSV(data):
    if (data == None):
        data = []
    return ",".join([str(x) for x in data])


def _createOrderData(hit):
    return {
        "store_id":
            hit.get('storeId'),
        "store_address_id":
            hit.get('storeAddressId'),
        "order_id":
            hit.get('orderId'),
        "dispatching_time":
            _toMySQLDateTime(hit.get('dispatchingTime')),
        "acceptance_time":
            _toMySQLDateTime(hit.get('acceptanceTime')),
        "cancel_reason":
            hit.get('cancelReason'),
        "courier_waiting_time_in_seconds":
            hit.get('courierWaitingTimeInSeconds'),
        "creation_time":
            _toMySQLDateTime(hit.get('creationTime')),
        "currency":
            hit.get('currency'),
        "feedback_id":
            hit.get('feedbackId'),
        "feedback_ids":
            _listToCSV(hit.get('feedbackIds')),
        "is_positive_rating":
            hit.get('isPositiveRating'),
        "is_refunded":
            hit.get('isRefunded'),
        "order_preparation_time_in_seconds":
            hit.get('orderPreparationTimeInSeconds'),
        "partner_rating_evaluation":
            hit.get('partnerRatingEvaluation'),
        "partner_rating_reasons":
            _listToCSV(hit.get('partnerRatingReasons')),
        "pick_up_time":
            _toMySQLDateTime(hit.get('pickUpTime')),
        "refunded_amount_in_cents":
            hit.get('refundedAmountInCents'),
        "serving_time":
            _toMySQLDateTime(hit.get('servingTime')),
        "status":
            hit.get('status'),
        "total_product_price_in_cents":
            hit.get('totalProductPriceInCents'),
        "total_products_price_in_cents":
            hit.get('totalProductsPriceInCents')
    }


def _createBoughtProductsData(hit):
    storeId = hit.get("storeId")
    storeAddressId = hit.get("storeAddressId")
    orderId = hit.get("orderId")
    dispatchingTime = _toMySQLDateTime(hit.get("dispatchingTime"))

    if hit.get("boughtProducts") is not None:
        for product in hit['boughtProducts']:
            yield {
                "store_id": storeId,
                "store_address_id": storeAddressId,
                "order_id": orderId,
                "dispatching_time": dispatchingTime,
                "bought_product_id": product.get("boughtProductId"),
                "external_id": product.get("externalId"),
                "name": product.get("name"),
                "price": product.get("price"),
                "product_id": product.get("productId"),
                "quantity": product.get("quantity")
            }


def _createCustomizationsData(hit):
    storeId = hit.get("storeId")
    storeAddressId = hit.get("storeAddressId")
    orderId = hit.get("orderId")
    dispatchingTime = _toMySQLDateTime(hit.get("dispatchingTime"))
    for product in hit['boughtProducts']:
        if product.get("customizations") is not None:
            customizations = product.get("customizations")
            boughtProductId = product.get("boughtProductId")
            for customization in customizations:
                yield {
                    "store_id": storeId,
                    "store_address_id": storeAddressId,
                    "order_id": orderId,
                    "dispatching_time": dispatchingTime,
                    "bought_product_id": boughtProductId,
                    "attribute_id": customization.get("attributeId"),
                    "external_id": customization.get("externalId"),
                    "name": customization.get("name"),
                    "price_impact": customization.get("priceImpact"),
                    "quantity": customization.get("quantity"),
                }


def _createProductIssues(hit):
    storeId = hit.get("storeId")
    storeAddressId = hit.get("storeAddressId")
    orderId = hit.get("orderId")
    dispatchingTime = _toMySQLDateTime(hit.get("dispatchingTime"))
    if hit.get("productIssues") is not None:
        productIssues = hit.get("productIssues")
        for issue in productIssues:
            optionId = issue.get("optionId")
            for product in issue.get("affectedProducts"):
                yield {
                    "store_id": storeId,
                    "store_address_id": storeAddressId,
                    "order_id": orderId,
                    "dispatching_time": dispatchingTime,
                    "option_id": optionId,
                    "bought_product_id": product.get("boughtProductId"),
                    "external_id": product.get("externalId"),
                    "name": product.get("name"),
                    "quantity": product.get("quantity")
                }


def processOrderBulk(mysql_client, hits):
    i = 1
    for hit in hits:
        processOrder(mysql_client, hit)
        i += 1
        if i % 256 == 0:
            mysql_client.commit()
    mysql_client.commit()


def processOrder(mysql_client, hit):
    cursor = mysql_client.cursor()
    data_order = _createOrderData(hit)
    bought_products = _createBoughtProductsData(hit)
    customizations = _createCustomizationsData(hit)
    product_issues = _createProductIssues(hit)

    try:
        cursor.execute(queries.orders_sql, data_order)

        # print ("==================== bought products")
        for bought_product in bought_products:
            # print(bought_product)
            cursor.execute(queries.bought_products_sql, bought_product)

        # print ("==================== customizations")
        for customization in customizations:
            # print(customization)
            cursor.execute(queries.customizations_sql, customization)

        # print ("==================== product issues")
        for product_issue in product_issues:
            # print(product_issue)
            cursor.execute(queries.product_issues_sql, product_issue)
        mysql_client.commit()
    except Exception as e:
        print(e)
        print(data_order)


def bulk(engine, hits):
    orders = []
    bought_products = []
    customizations = []
    product_issues = []
    print("transforming orders")
    for hit in hits:
        orders.append(_createOrderData(hit))
        bought_products.extend(_createBoughtProductsData(hit))
        customizations.extend(_createCustomizationsData(hit))
        product_issues.extend(_createProductIssues(hit))

    orders_df = pd.DataFrame.from_dict(orders)
    bought_products_df = pd.DataFrame.from_dict(bought_products)
    customizations_df = pd.DataFrame.from_dict(customizations)
    product_issues_df = pd.DataFrame.from_dict(product_issues)
    orders_df.to_sql('orders', con=engine, index=False, if_exists='append')
    bought_products_df.to_sql('bought_products',
                              con=engine,
                              index=False,
                              if_exists='append')
    customizations_df.to_sql('customizations',
                             con=engine,
                             index=False,
                             if_exists='append')
    product_issues_df.to_sql('product_issues',
                             con=engine,
                             index=False,
                             if_exists='append')
