CREATE TABLE IF NOT EXISTS glovo.orders (
    store_id UInt64,
    store_address_id UInt64,
    order_id UInt64,
    dispatching_time DateTime64(3, 'UTC'),
    acceptance_time DateTime64(3, 'UTC') NULL,
    cancel_reason String,
    courier_waiting_time_in_seconds UInt32,
    creation_time DateTime64(3, 'UTC') NULL,
    currency String NULL,
    feedback_id UInt32,
    feedback_ids String NULL,
    is_positive_rating Bool,
    is_refunded Bool NULL,
    order_preparation_time_in_seconds UInt32 NULL,
    partner_rating_evaluation String NULL,
    partner_rating_reasons String NULL,
    pick_up_time DateTime64(3, 'UTC') NULL,
    refunded_amount_in_cents UInt32 NULL,
    serving_time DateTime64(3, 'UTC') NULL,
    status String NULL,
    total_product_price_in_cents UInt32 NULL,
    total_products_price_in_cents UInt32 NULL
) ENGINE = MergeTree() ORDER BY (store_address_id, dispatching_time);

CREATE TABLE IF NOT EXISTS glovo.bought_products (
    store_id UInt64,
    store_address_id UInt64,
    order_id UInt64,
    dispatching_time DateTime64(3, 'UTC'),
    bought_product_id UInt64,
    external_id String,
    name String,
    price UInt64,
    product_id UInt64,
    quantity UInt64
) ENGINE = MergeTree() ORDER BY (store_address_id, dispatching_time);

CREATE TABLE IF NOT EXISTS glovo.customizations (
    store_id UInt64,
    store_address_id UInt64,
    order_id UInt64,
    dispatching_time DateTime64(3, 'UTC'),
    bought_product_id UInt64,
    attribute_id UInt64,
    external_id String,
    name String,
    price_impact UInt64,
    quantity UInt64
) ENGINE = MergeTree() ORDER BY (store_address_id, dispatching_time);

CREATE TABLE IF NOT EXISTS glovo.product_issues (
    store_id UInt64,
    store_address_id UInt64,
    order_id UInt64,
    dispatching_time DateTime64(3, 'UTC'),
    option_id String,
    bought_product_id UInt64,
    external_id String,
    name String,
    quantity UInt32
) ENGINE = MergeTree() ORDER BY (store_address_id, dispatching_time);