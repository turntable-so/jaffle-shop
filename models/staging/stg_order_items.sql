with
    source as (select * from {{ source("ecom", "raw_items") }}),

    orders as (select * from {{ ref("stg_orders") }}),

    joined as (
        select
            source.id as order_item_id,
            source.order_id,
            source.sku as product_id,
            orders.ordered_at
        from source
        left join orders on source.order_id = orders.order_id
    ),

    ranked as (
        select
            *,
            row_number() over (
                partition by order_id order by ordered_at desc
            ) as row_num
        from joined
    ),

    deduplicated as (
        select order_item_id, order_id, product_id, ordered_at as last_order_date
        from ranked
        where row_num = 1
    )

select *
from deduplicated
