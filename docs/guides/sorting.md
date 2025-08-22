# Sorting 


!!! danger "Anaplan Sorting is not consistent"
    If you are sorting by a field that is potentially ambiguous (e.g., `name`), the order of results is not guaranteed
    to be internally consistent across multiple requests. This will lead to wrong results when paginating through 
    result sets where the ambiguous order can cause records to slip between pages or be duplicated on multiple pages.
    The only way to ensure correct results when sorting is to make sure the entire result set fits in one page, 
    or to sort by a field that is guaranteed to be unique (e.g., `id`).

