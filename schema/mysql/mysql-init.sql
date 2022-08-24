CREATE DATABASE IF NOT EXISTS glovo;
USE glovo;
CREATE TABLE orders (
    `store_id` BIGINT,
    `store_address_id` BIGINT,
    `order_id` BIGINT,
    `dispatching_time` DATETIME DEFAULT NULL,
    `acceptance_time` DATETIME DEFAULT NULL,
    `cancel_reason` VARCHAR(255),
    `courier_waiting_time_in_seconds` INT,
    `creation_time` DATETIME DEFAULT NULL,
    `currency` VARCHAR(50),
    `feedback_id` BIGINT,
    `feedback_ids` VARCHAR(255),
    `is_positive_rating` BOOLEAN,
    `is_refunded` BOOLEAN,
    `order_preparation_time_in_seconds` BIGINT,
    `partner_rating_evaluation` VARCHAR(255),
    `partner_rating_reasons` VARCHAR(255),
    `pick_up_time` DATETIME DEFAULT NULL,
    `refunded_amount_in_cents` INT,
    `serving_time` DATETIME DEFAULT NULL,
    `status` VARCHAR(255),
    `total_product_price_in_cents` INT,
    `total_products_price_in_cents` INT
);
CREATE TABLE bought_products (
    `store_id` BIGINT,
    `store_address_id` BIGINT,
    `order_id` BIGINT,
    `dispatching_time` DATETIME DEFAULT NULL,
    `bought_product_id` BIGINT,
    `external_id` VARCHAR(255),
    `name` VARCHAR(255),
    `price` BIGINT,
    `product_id` BIGINT,
    `quantity` BIGINT
);
CREATE TABLE customizations (
    `store_id` BIGINT,
    `store_address_id` BIGINT,
    `order_id` BIGINT,
    `dispatching_time` DATETIME DEFAULT NULL,
    `bought_product_id` BIGINT,
    `attribute_id` BIGINT,
    `external_id` VARCHAR(255),
    `name` VARCHAR(255),
    `price_impact` BIGINT,
    `quantity` BIGINT
);
CREATE TABLE product_issues (
    `store_id` BIGINT,
    `store_address_id` BIGINT,
    `order_id` BIGINT,
    `dispatching_time` DATETIME DEFAULT NULL,
    `option_id` VARCHAR(255),
    `bought_product_id` BIGINT,
    `external_id` VARCHAR(255),
    `name` VARCHAR(255),
    `quantity` BIGINT
);
-- Indexes
alter table orders add index `address_id_time_price` (store_address_id, dispatching_time, total_product_price_in_cents);
alter table orders add index `address_id_time_prep_time` (store_address_id, dispatching_time, order_preparation_time_in_seconds);
alter table product_issues  add index `address_id_time_option_id` (store_address_id, dispatching_time, option_id);
alter table bought_products  add index `address_id_time_name` (store_address_id, dispatching_time, name);
alter table orders add index `address_id_time_rating` (store_address_id, dispatching_time, is_positive_rating);
alter table orders add index `address_id_time_status` (store_address_id, dispatching_time, status);
alter table customizations  add index `address_id_time_name` (store_address_id, dispatching_time, name);