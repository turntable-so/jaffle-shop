with

source as (

    select * from {{ ref('raw_customers') }}

),

renamed as (

    select * from ( select

        ----------  ids
        id as customer_id,

        ---------- text
        name as customer_name

    from {{ ref('raw_customers') }} )

)

select * from renamed
