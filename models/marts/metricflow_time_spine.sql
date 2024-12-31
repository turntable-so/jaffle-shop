
-- metricflow_time_spine.sql
with 

days as (
    {% if target.type == 'clickhouse' %}
    select toDate('2014-01-01') + number as date_day
    from numbers(3650)  -- 10 years * 365 days
    {% elif target.type == 'duckdb' %}
    select date_day
    from generate_series(date '2014-01-01', date '2024-01-01', interval 1 day) as date_day
    {% else %}
    {{ dbt_date.get_base_dates(n_dateparts=365*10, datepart="day") }}
    {% endif %}
),

cast_to_date as (
    select 
        {% if target.type == 'clickhouse' %}
        date_day
        {% elif target.type == 'duckdb' %}
        date_day
        {% else %}
        DATE(date_day) as date_day
        {% endif %}
    from days
)

select * from cast_to_date
