INSERT INTO {{ source('bronze', 'dim_items_scd_simulation') }}
VALUES
    (1, 'Item A', 'Category 1', current_timestamp()),
    (2, 'Item B', 'Category 2', current_timestamp()),
    (3, 'Item C', 'Category 3', current_timestamp()),
    (4, 'Item D', 'Category 3', current_timestamp()),
    (5, 'Item E', 'Category 2', current_timestamp())
    ;
