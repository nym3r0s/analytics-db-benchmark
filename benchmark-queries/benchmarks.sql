-- Sales per window compared to previous time period
--  Clickhouse
select
    toStartOfDay(dispatching_time) as d,
    sum(total_product_price_in_cents) as p
from orders
where
    store_address_id in (212,215,214,218,213,210,211,216,217,219)
  and dispatching_time > '2022-07-10 00:00:00.000'
  and dispatching_time < '2022-07-24 00:00:00.000'
group by d
order by d asc

-- MySQL
select
    date(dispatching_time) as d,
    sum(total_product_price_in_cents) as p
from orders
where
        store_address_id in (212,215,214,218,213,210,211,216,217,219)
  and dispatching_time > '2022-07-10 00:00:00.000'
  and dispatching_time < '2022-07-24 00:00:00.000'
group by d
order by d asc

-- Average Preparation time of an Order
-- Clickhouse
select
    toStartOfDay(dispatching_time) as d,
    avg(order_preparation_time_in_seconds) as a
from orders
where
        store_address_id in (212,215,214,218,213,210,211,216,217,219)
  and dispatching_time > '2022-07-10 00:00:00.000'
  and dispatching_time < '2022-07-24 00:00:00.000'
group by d
order by d asc

-- MySQL
select
    date(dispatching_time) as d,
    avg(order_preparation_time_in_seconds) as a
from orders
where
    store_address_id in (212,215,214,218,213,210,211,216,217,219)
  and dispatching_time > '2022-07-10 00:00:00.000'
  and dispatching_time < '2022-07-24 00:00:00.000'
group by d
order by d asc

-- Top X reported issues across products with counts
-- Clickhouse
select
    option_id,
    count(*) as cnt
from product_issues
where
        store_address_id in (212,215,214,218,213,210,211,216,217,219)
  and dispatching_time > '2022-07-10 00:00:00.000'
  and dispatching_time < '2022-07-24 00:00:00.000'
group by option_id
order by cnt desc
limit 10

-- MySQL
select
    option_id,
    count(*) as cnt
from product_issues
where
        store_address_id in (212,215,214,218,213,210,211,216,217,219)
  and dispatching_time > '2022-07-10 00:00:00.000'
  and dispatching_time < '2022-07-24 00:00:00.000'
group by option_id
order by cnt desc
    limit 10

-- Top X most/least ordered products
select
    name,
    count(*) as cnt
from product_issues
where
        store_address_id in (212,215,214,218,213,210,211,216,217,219)
  and dispatching_time > '2022-07-10 00:00:00.000'
  and dispatching_time < '2022-07-24 00:00:00.000'
group by name
order by cnt desc
    limit 10

-- Total Positive and Negative Reviews
select
    is_positive_rating,
    count(*) as cnt
from orders
where
        store_address_id in (212,215,214,218,213,210,211,216,217,219)
  and dispatching_time > '2022-07-10 00:00:00.000'
  and dispatching_time < '2022-07-24 00:00:00.000'
group by is_positive_rating

-- Order History filtered by canceled / refunded / orders with issues
select
    *
from orders
where
        store_address_id in (212,215,214,218,213,210,211,216,217,219)
  and dispatching_time > '2022-07-10 00:00:00.000'
  and dispatching_time < '2022-07-24 00:00:00.000'
 and status = 'CANCELLED'
order by dispatching_time asc
limit 10

-- Average Value of an Order
select avg(total_product_price_in_cents)
from orders
where
        store_address_id in (212,215,214,218,213,210,211,216,217,219)
  and dispatching_time > '2022-07-10 00:00:00.000'
  and dispatching_time < '2022-07-24 00:00:00.000'