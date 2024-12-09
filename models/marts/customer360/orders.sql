with
    orders as (select * from {{ ref("stg_orders") }}),

    order_items_table as (select * from {{ ref("order_items") }}),

    order_items_summary as (
        select
            order_items.order_id,
            sum(supply_cost) as order_cost,
            sum(is_food_item) as count_food_items,
            sum(is_drink_item) as count_drink_items,
            max(ordered_at) as latest_ordered_at
        from order_items_table as order_items
        group by 1
    ),

    deduplicated_orders as (
        select distinct
            on (orders.order_id) orders.*, order_items_summary.latest_ordered_at
        from orders
        left join order_items_summary on orders.order_id = order_items_summary.order_id
        order by orders.order_id, order_items_summary.latest_ordered_at desc
    ),

    compute_booleans as (
        select
            deduplicated_orders.*,
            count_food_items > 0 as is_food_order,
            count_drink_items > 0 as is_drink_order,
            order_cost,
            latest_ordered_at as last_order_date
        from deduplicated_orders
        left join
            order_items_summary
            on deduplicated_orders.order_id = order_items_summary.order_id
    )

select *
from compute_booleans
