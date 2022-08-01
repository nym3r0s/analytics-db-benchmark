orders_sql = ('''
INSERT INTO glovo.orders
(
    store_id, 
    store_address_id, 
    order_id, 
    dispatching_time,
    acceptance_time,
    cancel_reason,
    courier_waiting_time_in_seconds,
    creation_time,
    currency,
    feedback_id,
    feedback_ids,
    is_positive_rating,
    is_refunded,
    order_preparation_time_in_seconds,
    partner_rating_evaluation,
    partner_rating_reasons,
    pick_up_time,
    refunded_amount_in_cents,
    serving_time,
    status,
    total_product_price_in_cents,
    total_products_price_in_cents
 )
VALUES(
    %(store_id)s, 
    %(store_address_id)s, 
    %(order_id)s, 
    %(dispatching_time)s,
    %(acceptance_time)s,
    %(cancel_reason)s,
    %(courier_waiting_time_in_seconds)s,
    %(creation_time)s,
    %(currency)s,
    %(feedback_id)s,
    %(feedback_ids)s,
    %(is_positive_rating)s,
    %(is_refunded)s,
    %(order_preparation_time_in_seconds)s,
    %(partner_rating_evaluation)s,
    %(partner_rating_reasons)s,
    %(pick_up_time)s,
    %(refunded_amount_in_cents)s,
    %(serving_time)s,
    %(status)s,
    %(total_product_price_in_cents)s,
    %(total_products_price_in_cents)s);
''')

bought_products_sql = '''
INSERT INTO glovo.bought_products
(
    store_id,
    store_address_id,
    order_id,
    dispatching_time,
    bought_product_id,
    external_id,
    name,
    price,
    product_id,
    quantity
)
VALUES(
    %(store_id)s,
    %(store_address_id)s,
    %(order_id)s,
    %(dispatching_time)s,
    %(bought_product_id)s,
    %(external_id)s,
    %(name)s,
    %(price)s,
    %(product_id)s,
    %(quantity)s
);
'''

customizations_sql = '''
INSERT INTO glovo.customizations
(
    store_id,
    store_address_id,
    order_id,
    dispatching_time,
    bought_product_id,
    attribute_id,
    external_id,
    name,
    price_impact,
    quantity
)
VALUES(
    %(store_id)s,
    %(store_address_id)s,
    %(order_id)s,
    %(dispatching_time)s,
    %(bought_product_id)s,
    %(attribute_id)s,
    %(external_id)s,
    %(name)s,
    %(price_impact)s,
    %(quantity)s
);
'''

product_issues_sql = '''
INSERT INTO glovo.product_issues
(
    store_id,
    store_address_id,
    order_id,
    dispatching_time,
    option_id,
    bought_product_id,
    external_id,
    name,
    quantity
)
VALUES(
    %(store_id)s,
    %(store_address_id)s,
    %(order_id)s,
    %(dispatching_time)s,
    %(option_id)s,
    %(bought_product_id)s,
    %(external_id)s,
    %(name)s,
    %(quantity)s
);
'''