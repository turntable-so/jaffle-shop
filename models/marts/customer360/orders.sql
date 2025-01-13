with 
--test
orders as (
    
    select * from {{ ref('stg_orders')}}

),

order_items_table as (
    
    select * from {{ ref('order_items')}}

),

order_items_summary as (

    select

        order_items.order_id,

        sum(supply_cost) as order_cost,
        sum(is_food_item) as count_food_items,
        sum(is_drink_item) as count_drink_items


    from order_items_table as order_items

    group by 1

),


compute_booleans as (
    select

        orders.*,
        count_food_items > 0 as is_food_order,
        count_drink_items > 0 as is_drink_order,
        order_cost

    from orders
    
    left join order_items_summary on orders.order_id = order_items_summary.order_id
),

customers as (
    select * from {{ ref('stg_customers') }}
),

orders_table as (
    select * from {{ ref('orders') }}
),

order_items_table as (
    select * from {{ ref('order_items') }}
),

order_summary as (
    select
        customer_id,
        count(distinct orders.order_id) as count_lifetime_orders,
        count(distinct orders.order_id) > 1 as is_repeat_buyer,
        min(orders.ordered_at) as first_ordered_at,
        max(orders.ordered_at) as last_ordered_at,
        sum(order_items.product_price) as lifetime_spend_pretax,
        sum(orders.order_total) as lifetime_spend
    from orders_table as orders
    left join order_items_table as order_items on orders.order_id = order_items.order_id
    group by 1
),

deduplicated_customers as (
    select distinct on (customer_id)
        *
    from customers
    order by customer_id, customer_name
),

joined as (
    select
        deduplicated_customers.*,
        order_summary.count_lifetime_orders,
        order_summary.first_ordered_at,
        order_summary.last_ordered_at,
        order_summary.lifetime_spend_pretax,
        order_summary.lifetime_spend,
        case
            when order_summary.is_repeat_buyer then 'returning'
            else 'new'
        end as customer_type
    from deduplicated_customers
    left join order_summary
        on deduplicated_customers.customer_id = order_summary.customer_id
)

select * from joined