select 
    product_id,
    product_name,
    product_type,
    product_description,
    case when product_id = 'JAF-001' then product_price else product_price * 1.1 end as product_price

from {{ ref('stg_products') }}
where is_food_item = 1

union all

-- Add one new row as a test
select 
    '999' as product_id,
    'Manual Test Product' as product_name,
    'Test Type' as product_type,
    'A manually added test product' as product_description,
    11.00 as product_price