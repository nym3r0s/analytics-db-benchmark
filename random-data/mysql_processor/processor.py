from datetime import date, datetime, timedelta

import mysql_processor.queries as queries
from dateutil import parser
import numpy as np


def _toMySQLDateTime(isoDate):
    if (isoDate != None):
        return parser.parse(isoDate)
    return None


def _listToCSV(data):
    if (data == None):
        data = []
    return ",".join([str(x) for x in data])


def _createOrderData(hit):
    return (
        hit.get('storeId'),
        hit.get('storeAddressId'),
        hit.get('orderId'),
        _toMySQLDateTime(hit.get('dispatchingTime')),
        _toMySQLDateTime(hit.get('acceptanceTime')),
        hit.get('cancelReason'),
        hit.get('courierWaitingTimeInSeconds'),
        _toMySQLDateTime(hit.get('creationTime')),
        hit.get('currency'),
        hit.get('feedbackId'),
        _listToCSV(hit.get('feedbackIds')),
        hit.get('isPositiveRating'),
        hit.get('isRefunded'),
        hit.get('orderPreparationTimeInSeconds'),
        hit.get('partnerRatingEvaluation'),
        _listToCSV(hit.get('partnerRatingReasons')),
        _toMySQLDateTime(hit.get('pickUpTime')),
        hit.get('refundedAmountInCents'),
        _toMySQLDateTime(hit.get('servingTime')),
        hit.get('status'),
        hit.get('totalProductPriceInCents'),
        hit.get('totalProductsPriceInCents')
    )


def _createBoughtProductsData(hit):
    storeId = hit.get("storeId")
    storeAddressId = hit.get("storeAddressId")
    orderId = hit.get("orderId")
    dispatchingTime = _toMySQLDateTime(hit.get("dispatchingTime"))
    products = []
    if hit.get("boughtProducts") is not None:
        for product in hit['boughtProducts']:
            products.append((
                storeId,
                storeAddressId,
                orderId,
                dispatchingTime,
                product.get("boughtProductId"),
                product.get("externalId"),
                product.get("name"),
                product.get("price"),
                product.get("productId"),
                product.get("quantity")
            ))
    return products


def _createCustomizationsData(hit):
    storeId = hit.get("storeId")
    storeAddressId = hit.get("storeAddressId")
    orderId = hit.get("orderId")
    dispatchingTime = _toMySQLDateTime(hit.get("dispatchingTime"))
    ret = []
    for product in hit['boughtProducts']:
        if product.get("customizations") is not None:
            customizations = product.get("customizations")
            boughtProductId = product.get("boughtProductId")
            for customization in customizations:
                ret.append( (
                    storeId,
                    storeAddressId,
                    orderId,
                    dispatchingTime,
                    boughtProductId,
                    customization.get("attributeId"),
                    customization.get("externalId"),
                    customization.get("name"),
                    customization.get("priceImpact"),
                    customization.get("quantity"),
                ))
    return ret


def _createProductIssues(hit):
    storeId = hit.get("storeId")
    storeAddressId = hit.get("storeAddressId")
    orderId = hit.get("orderId")
    dispatchingTime = _toMySQLDateTime(hit.get("dispatchingTime"))
    ret = []
    if hit.get("productIssues") is not None:
        productIssues = hit.get("productIssues")
        for issue in productIssues:
            optionId = issue.get("optionId")
            for product in issue.get("affectedProducts"):
                ret.append( (
                    storeId,
                    storeAddressId,
                    orderId,
                    dispatchingTime,
                    optionId,
                    product.get("boughtProductId"),
                    product.get("externalId"),
                    product.get("name"),
                    product.get("quantity")
                ))
    return ret


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

        #print ("==================== bought products")
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

def bulk(mysql_client, hits):
    cursor = mysql_client.cursor()
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

    # try:
    print("inserting {} orders".format(len(orders)))
    cursor.executemany(queries.orders_sql, orders)
    mysql_client.commit()

    #print ("==================== bought products")
    # for bought_product in bought_products:
    #     print(bought_product)
    print("inserting {} bought_products".format(len(bought_products)))
    for i in range(0, len(bought_products), 100):
        chunk = bought_products[i:i + 100]
        cursor.executemany(queries.bought_products_sql, chunk)
        mysql_client.commit()

    # print ("==================== customizations")
    # for customization in customizations:
        # print(customization)
    print("inserting {} customizations".format(len(customizations)))
    for i in range(0, len(customizations), 500):
        chunk = customizations[i:i + 500]
        cursor.executemany(queries.customizations_sql, chunk)
        mysql_client.commit()

    # print ("==================== product issues")
    # for product_issue in product_issues:
        # print(product_issue)
    print("inserting {} product_issues".format(len(product_issues)))
    for i in range(0, len(product_issues), 500):
        chunk = product_issues[i:i + 500]
        cursor.executemany(queries.product_issues_sql, chunk)
        mysql_client.commit()
    # except Exception as e:
    #     print(e)
    #     print(orders)