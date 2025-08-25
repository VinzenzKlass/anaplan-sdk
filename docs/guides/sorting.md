!!! danger "Anaplan Sorting is not consistent"
    If you are sorting by a field that is potentially ambiguous (e.g., `name`), the order of results is not guaranteed
    to be internally consistent across multiple requests. This will lead to wrong results when paginating through
    result sets where the ambiguous order can cause records to slip between pages or be duplicated on multiple pages.
    The only way to ensure correct results when sorting is to make sure the entire result set fits in one page,
    or to sort by a field that is guaranteed to be unique (e.g., `id`).

Some endpoints support sorting results by a specified field in either ascending or descending order. The methods for
these endpoints include a `sort_by` parameter to specify the field to sort on, and a `descending` boolean parameter
to specify the sort order (default is ascending).  

## Syntax

These Methods support sorting. The Type Literals for the `sort_by` will tell you which fields are supported for sorting.

```python
# Audit
anaplan.audit.get_users(sort_by="email")

# Workspaces & Models
anaplan.get_workspaces(sort_by="size_allowance", descending=True)
anaplan.get_models(sort_by="active_state")

# Model Objects
anaplan.get_files(sort_by="name")
anaplan.get_actions(sort_by="id")
anaplan.get_processes(sort_by="name")
anaplan.get_imports(sort_by="id")
anaplan.get_exports(sort_by="name")

# Transactional
anaplan.tr.get_modules(sort_by="name")
anaplan.tr.get_views(sort_by="module_id")
anaplan.tr.get_lists(sort_by="id")

# ALM
anaplan.alm.get_revisions(sort_by="created_on")

# CloudWorks
anaplan.cw.get_integrations(sort_by_name="descending")
```
