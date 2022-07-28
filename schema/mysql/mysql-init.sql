CREATE DATABASE IF NOT EXISTS glovo;
USE glovo;
CREATE TABLE orders (
    `store_id` BIGINT UNSIGNED NOT NULL,
    `store_address_id` BIGINT UNSIGNED NOT NULL,
    `order_id` BIGINT UNSIGNED NOT NULL,
    `dispatching_time` DATETIME DEFAULT NULL,
    `acceptance_time` DATETIME DEFAULT NULL,
    `cancel_reason` VARCHAR(255),
    `courier_waiting_time_in_seconds` INT,
    `creation_time` DATETIME DEFAULT NULL,
    `currency` VARCHAR(50),
    `feedback_id` BIGINT UNSIGNED NOT NULL,
    `feedback_ids` BIGINT UNSIGNED NOT NULL,
    `is_positive_rating` BOOLEAN,
    `is_refunded` BOOLEAN,
    `order_preparation_time_in_seconds` BIGINT UNSIGNED NOT NULL,
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
    `store_id` BIGINT UNSIGNED NOT NULL,
    `store_address_id` BIGINT UNSIGNED NOT NULL,
    `order_id` BIGINT UNSIGNED NOT NULL,
    `dispatching_time` DATETIME DEFAULT NULL,
    `boughtProductId` BIGINT UNSIGNED NOT NULL,
    `externalId` VARCHAR(255),
    `name` VARCHAR(255),
    `price` BIGINT UNSIGNED NOT NULL,
    `productId` BIGINT UNSIGNED NOT NULL,
    `quantity` BIGINT UNSIGNED NOT NULL
);
CREATE TABLE customizations (
    `store_id` BIGINT UNSIGNED NOT NULL,
    `store_address_id` BIGINT UNSIGNED NOT NULL,
    `order_id` BIGINT UNSIGNED NOT NULL,
    `dispatching_time` DATETIME DEFAULT NULL,
    `boughtProductId` BIGINT UNSIGNED NOT NULL,
    `attributeId` BIGINT UNSIGNED NOT NULL,
    `externalId` VARCHAR(255),
    `name` VARCHAR(255),
    `priceImpact` BIGINT UNSIGNED NOT NULL,
    `quantity` BIGINT UNSIGNED NOT NULL
);
CREATE TABLE product_issues (
    `store_id` BIGINT UNSIGNED NOT NULL,
    `store_address_id` BIGINT UNSIGNED NOT NULL,
    `order_id` BIGINT UNSIGNED NOT NULL,
    `dispatching_time` DATETIME DEFAULT NULL,
    `boughtProductId` BIGINT UNSIGNED NOT NULL,
    `externalId` VARCHAR(255),
    `name` VARCHAR(255),
    `quantity` BIGINT UNSIGNED NOT NULL
);