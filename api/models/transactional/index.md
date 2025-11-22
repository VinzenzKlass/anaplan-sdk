## User

Parameters:

| Name              | Type   | Description                                              | Default                                         |
| ----------------- | ------ | -------------------------------------------------------- | ----------------------------------------------- |
| `id`              | `str`  | The unique identifier of this user.                      | *required*                                      |
| `active`          | `bool` | Whether this user is active or not.                      | *required*                                      |
| `email`           | `str`  | The email address of this user.                          | *required*                                      |
| `email_opt_in`    | `bool` | Whether this user has opted in to receive emails or not. | *required*                                      |
| `first_name`      | `str`  | The first name of this user.                             | *required*                                      |
| `last_name`       | `str`  | The last name of this user.                              | *required*                                      |
| `last_login_date` | \`str  | None\`                                                   | The last login date of this user in ISO format. |

## ListItem

Parameters:

| Name         | Type             | Description                              | Default                                                |
| ------------ | ---------------- | ---------------------------------------- | ------------------------------------------------------ |
| `id`         | `int`            | The unique identifier of this list item. | *required*                                             |
| `name`       | `str`            | The name of this list item.              | *required*                                             |
| `code`       | \`str            | None\`                                   | The code of this list item.                            |
| `properties` | `dict[str, Any]` | The properties of this list item.        | `{}`                                                   |
| `subsets`    | `dict[str, Any]` | The subsets of this list item.           | `{}`                                                   |
| `parent`     | \`str            | None\`                                   | The parent of this list item.                          |
| `parent_id`  | \`str            | None\`                                   | The unique identifier of the parent of this list item. |

## Module

Parameters:

| Name   | Type  | Description                           | Default    |
| ------ | ----- | ------------------------------------- | ---------- |
| `id`   | `int` | The unique identifier of this module. | *required* |
| `name` | `str` | The name of this module.              | *required* |

## Dimension

Parameters:

| Name   | Type  | Description                              | Default    |
| ------ | ----- | ---------------------------------------- | ---------- |
| `id`   | `int` | The unique identifier of this dimension. | *required* |
| `name` | `str` | The name of this dimension.              | *required* |

## DimensionWithCode

Parameters:

| Name   | Type  | Description                              | Default    |
| ------ | ----- | ---------------------------------------- | ---------- |
| `id`   | `int` | The unique identifier of this dimension. | *required* |
| `name` | `str` | The name of this dimension.              | *required* |
| `code` | `str` | The code of this dimension.              | *required* |

## View

Parameters:

| Name       | Type  | Description                                               | Default    |
| ---------- | ----- | --------------------------------------------------------- | ---------- |
| `code`     | `str` | The code of this view.                                    | *required* |
| `id`       | `int` | The unique identifier of this view.                       | *required* |
| `name`     | `str` | The name of this views.                                   | *required* |
| `moduleId` | `int` | The unique identifier of the module this view belongs to. | *required* |

## ViewInfo

Parameters:

| Name        | Type              | Description                                       | Default    |
| ----------- | ----------------- | ------------------------------------------------- | ---------- |
| `view_id`   | `int`             | The unique identifier of this view.               | *required* |
| `view_name` | `str`             | The name of this view.                            | *required* |
| `rows`      | `list[Dimension]` | The list of dimensions in the rows of this view.  | `[]`       |
| `pages`     | `list[Dimension]` | The list of dimensions in the pages of this view. | `[]`       |

## PeriodType

Parameters:

| Name           | Type                                                              | Description                    | Default    |
| -------------- | ----------------------------------------------------------------- | ------------------------------ | ---------- |
| `entity_id`    | `Literal['YEAR', 'HALF_YEAR', 'MONTH', 'QUARTER', 'WEEK', 'DAY']` | The type of period entity.     | *required* |
| `entity_label` | `Literal['Year', 'Half-Year', 'Month', 'Quarter', 'Week', 'Day']` | The type of period entity.     | *required* |
| `entity_index` | `int`                                                             | The index of the period entity | *required* |

## EntityFormatFilter

Parameters:

| Name                           | Type  | Description                                                | Default    |
| ------------------------------ | ----- | ---------------------------------------------------------- | ---------- |
| `source_line_item_or_property` | `str` | The unique identifier of the source line item or property. | *required* |
| `mapping_hierarchy`            | `str` | The unique identifier of the mapping hierarchy.            | *required* |
| `key_property`                 | `str` | The unique identifier of the key property.                 | *required* |
| `value_property`               | `str` | The unique identifier of the value property.               | *required* |

## TextMetadata

Parameters:

| Name        | Type                                                   | Description                                                | Default    |
| ----------- | ------------------------------------------------------ | ---------------------------------------------------------- | ---------- |
| `data_type` | `Literal['TEXT']`                                      | The data type. Literal for the tagged union discriminator. | *required* |
| `text_type` | `Literal['DRILLTHRU_URI', 'EMAIL_ADDRESS', 'GENERAL']` | The text type.                                             | *required* |

## ListMetadata

Parameters:

| Name                       | Type                 | Description                                                                | Default                             |
| -------------------------- | -------------------- | -------------------------------------------------------------------------- | ----------------------------------- |
| `data_type`                | `Literal['ENTITY']`  | The data type. Literal for the tagged union discriminator.                 | *required*                          |
| `hierarchy_entity_id`      | `int`                | The unique identifier of the hierarchy entity, like Lists or List Subsets. | *required*                          |
| `selective_access_applied` | `bool`               | Whether selective access is applied or not.                                | *required*                          |
| `show_all`                 | `bool`               | Whether to show all values or not.                                         | *required*                          |
| `entity_format_filter`     | \`EntityFormatFilter | None\`                                                                     | Entity format filter configuration. |

## TimePeriodMetadata

Parameters:

| Name          | Type                     | Description                                                | Default    |
| ------------- | ------------------------ | ---------------------------------------------------------- | ---------- |
| `data_type`   | `Literal['TIME_ENTITY']` | The data type. Literal for the tagged union discriminator. | *required* |
| `period_type` | `PeriodType`             | The period type.                                           | *required* |

## NumberMetadata

Parameters:

| Name                         | Type                                                                                                         | Description                                                | Default                          |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------- | -------------------------------- |
| `data_type`                  | `Literal['NUMBER']`                                                                                          | The data type. Literal for the tagged union discriminator. | *required*                       |
| `comparison_increase`        | \`Literal['GOOD', 'BAD', 'NEUTRAL']                                                                          | None\`                                                     | The comparison increase setting. |
| `custom_units`               | \`str                                                                                                        | None\`                                                     | Custom units for display.        |
| `decimal_places`             | `int`                                                                                                        | Number of decimal places.                                  | *required*                       |
| `decimal_separator`          | `Literal['COMMA', 'FULL_STOP']`                                                                              | The decimal separator.                                     | *required*                       |
| `units_display_type`         | `Literal['CUSTOM_SUFFIX', 'CUSTOM_PREFIX', 'CURRENCY_CODE', 'CURRENCY_SYMBOL', 'PERCENTAGE_SUFFIX', 'NONE']` | Units display type.                                        | *required*                       |
| `units_type`                 | `Literal['CUSTOM', 'CURRENCY', 'PERCENTAGE', 'NONE']`                                                        | Units type.                                                | *required*                       |
| `zero_format`                | `Literal['HYPHEN', 'ZERO', 'BLANK']`                                                                         | Zero format display.                                       | *required*                       |
| `grouping_separator`         | `Literal['COMMA', 'FULL_STOP', 'SPACE', 'NONE']`                                                             | The grouping separator.                                    | *required*                       |
| `minimum_significant_digits` | `int`                                                                                                        | Minimum significant digits.                                | *required*                       |
| `negative_number_notation`   | `Literal['MINUS_SIGN', 'PARENTHESES']`                                                                       | Negative number notation.                                  | *required*                       |

## GenericTypeMetadata

Parameters:

| Name        | Type                                 | Description    | Default    |
| ----------- | ------------------------------------ | -------------- | ---------- |
| `data_type` | `Literal['BOOLEAN', 'NONE', 'DATE']` | The data type. | *required* |

## LineItem

Parameters:

| Name                  | Type                                                                          | Description                                                    | Default                                    |
| --------------------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------ |
| `id`                  | `int`                                                                         | The unique identifier of this line item.                       | *required*                                 |
| `name`                | `str`                                                                         | The name of this line item.                                    | *required*                                 |
| `module_id`           | `int`                                                                         | The unique identifier of the module this line item belongs to. | *required*                                 |
| `module_name`         | `str`                                                                         | The name of the module this line item belongs to.              | *required*                                 |
| `format`              | `Literal['NUMBER', 'BOOLEAN', 'TEXT', 'NONE', 'DATE', 'LIST', 'TIME PERIOD']` | The format of this line item.                                  | *required*                                 |
| `format_metadata`     | \`NumberMetadata                                                              | ListMetadata                                                   | TimePeriodMetadata                         |
| `summary`             | `str`                                                                         | The summary of this line item.                                 | *required*                                 |
| `applies_to`          | `list[Dimension]`                                                             | The applies to value of this line item.                        | `[]`                                       |
| `data_tags`           | `list[Dimension]`                                                             | The data tags of this line item.                               | `[]`                                       |
| `referenced_by`       | `list[Dimension]`                                                             | List of references to this line item.                          | `[]`                                       |
| `time_scale`          | `str`                                                                         | The time scale of this line item.                              | *required*                                 |
| `time_range`          | `str`                                                                         | The time range of this line item.                              | *required*                                 |
| `version`             | `Dimension`                                                                   | The version of this line item.                                 | *required*                                 |
| `parent`              | \`Dimension                                                                   | None\`                                                         | The Parent of this line item.              |
| `read_access_driver`  | \`Dimension                                                                   | None\`                                                         | The read access driver of this line item.  |
| `write_access_driver` | \`Dimension                                                                   | None\`                                                         | The write access driver of this line item. |
| `style`               | `str`                                                                         | The style of this line item.                                   | *required*                                 |
| `cell_count`          | \`int                                                                         | None\`                                                         | The cell count of this line item.          |
| `notes`               | `str`                                                                         | The notes of this line item.                                   | *required*                                 |
| `code`                | \`str                                                                         | None\`                                                         | The code of this line item.                |
| `is_summary`          | `bool`                                                                        | Whether this line item is a summary or not.                    | *required*                                 |
| `formula`             | \`str                                                                         | None\`                                                         | The formula of this line item.             |
| `formula_scope`       | `str`                                                                         | The formula scope of this line item.                           | *required*                                 |
| `use_switchover`      | `bool`                                                                        | Whether the switchover is used or not.                         | *required*                                 |
| `breakback`           | `bool`                                                                        | Whether the breakback is enabled or not.                       | *required*                                 |
| `brought_forward`     | `bool`                                                                        | Whether the brought forward is enabled or not.                 | *required*                                 |
| `start_of_section`    | `bool`                                                                        | Whether this line item is the start of a section or not.       | *required*                                 |

## Failure

Parameters:

| Name      | Type  | Description                        | Default    |
| --------- | ----- | ---------------------------------- | ---------- |
| `index`   | `int` | The index of the item that failed. | *required* |
| `reason`  | `str` | The reason for the failure.        | *required* |
| `details` | `str` | The details of the failure.        | *required* |

## ModelStatus

Parameters:

| Name                         | Type    | Description                      | Default                                          |
| ---------------------------- | ------- | -------------------------------- | ------------------------------------------------ |
| `peak_memory_usage_estimate` | \`int   | None\`                           | The peak memory usage estimate of this model.    |
| `peak_memory_usage_time`     | \`int   | None\`                           | The peak memory usage time of this model.        |
| `progress`                   | `float` | The progress of this model.      | *required*                                       |
| `current_step`               | `str`   | The current step of this model.  | *required*                                       |
| `tooltip`                    | \`str   | None\`                           | The tooltip of this model.                       |
| `task_id`                    | \`str   | None\`                           | The unique identifier of the task of this model. |
| `creation_time`              | `int`   | The creation time of this model. | *required*                                       |
| `export_task_type`           | \`str   | None\`                           | The export task type of this model.              |

## InsertionResult

Parameters:

| Name       | Type            | Description                                        | Default    |
| ---------- | --------------- | -------------------------------------------------- | ---------- |
| `added`    | `int`           | The number of items successfully added.            | *required* |
| `ignored`  | `int`           | The number of items ignored, or items that failed. | *required* |
| `total`    | `int`           | The total number of items.                         | *required* |
| `failures` | `list[Failure]` | The list of failures.                              | `[]`       |

## ListDeletionResult

Parameters:

| Name       | Type            | Description                               | Default    |
| ---------- | --------------- | ----------------------------------------- | ---------- |
| `deleted`  | `int`           | The number of items successfully deleted. | *required* |
| `failures` | `list[Failure]` | The list of failures.                     | `[]`       |

## PartialCurrentPeriod

Parameters:

| Name          | Type  | Description                                              | Default    |
| ------------- | ----- | -------------------------------------------------------- | ---------- |
| `period_text` | `str` | The text representation of the current period.           | *required* |
| `last_day`    | `str` | The last day of the current period in YYYY-MM-DD format. | *required* |

## CurrentPeriod

Parameters:

| Name            | Type  | Description                                              | Default    |
| --------------- | ----- | -------------------------------------------------------- | ---------- |
| `period_text`   | `str` | The text representation of the current period.           | *required* |
| `last_day`      | `str` | The last day of the current period in YYYY-MM-DD format. | *required* |
| `calendar_type` | `str` | The type of calendar used for the current period.        | *required* |

## FiscalYear

Parameters:

| Name         | Type  | Description                                                | Default    |
| ------------ | ----- | ---------------------------------------------------------- | ---------- |
| `year`       | `str` | The fiscal year in the format set in the model, e.g. FY24. | *required* |
| `start_date` | `str` | The start date of the fiscal year in YYYY-MM-DD format.    | *required* |
| `end_date`   | `str` | The end date of the fiscal year in YYYY-MM-DD format.      | *required* |

## TotalsSelection

Parameters:

| Name                   | Type   | Description                              | Default    |
| ---------------------- | ------ | ---------------------------------------- | ---------- |
| `quarter_totals`       | `bool` | Whether quarter totals are enabled.      | *required* |
| `half_year_totals`     | `bool` | Whether half year totals are enabled.    | *required* |
| `year_to_date_summary` | `bool` | Whether year to date summary is enabled. | *required* |
| `year_to_go_summary`   | `bool` | Whether year to go summary is enabled.   | *required* |
| `total_of_all_periods` | `bool` | Whether total of all periods is enabled. | *required* |

## TotalsSelectionWithQuarter

Parameters:

| Name                   | Type                  | Description                                       | Default    |
| ---------------------- | --------------------- | ------------------------------------------------- | ---------- |
| `quarter_totals`       | `bool`                | Whether quarter totals are enabled.               | *required* |
| `half_year_totals`     | `bool`                | Whether half year totals are enabled.             | *required* |
| `year_to_date_summary` | `bool`                | Whether year to date summary is enabled.          | *required* |
| `year_to_go_summary`   | `bool`                | Whether year to go summary is enabled.            | *required* |
| `total_of_all_periods` | `bool`                | Whether total of all periods is enabled.          | *required* |
| `extra_month_quarter`  | `Literal[1, 2, 3, 4]` | The quarter in which the extra month is included. | *required* |

## BaseCalendar

Parameters:

| Name             | Type                                                                                                                      | Description                       | Default    |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------- | --------------------------------- | ---------- |
| `calendar_type`  | `Literal['Calendar Months/Quarters/Years', 'Weeks: 4-4-5, 4-5-4 or 5-4-4', 'Weeks: General', 'Weeks: 13 4-week Periods']` | The type of calendar used.        | *required* |
| `current_period` | `PartialCurrentPeriod`                                                                                                    | The current period configuration. | *required* |

## MonthsQuartersYearsCalendar

Parameters:

| Name               | Type                                                                                                                      | Description                                          | Default    |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- | ---------- |
| `calendar_type`    | `Literal['Calendar Months/Quarters/Years', 'Weeks: 4-4-5, 4-5-4 or 5-4-4', 'Weeks: General', 'Weeks: 13 4-week Periods']` | The type of calendar used.                           | *required* |
| `current_period`   | `PartialCurrentPeriod`                                                                                                    | The current period configuration.                    | *required* |
| `past_years_count` | `int`                                                                                                                     | The number of past years included.                   | *required* |
| `fiscal_year`      | `FiscalYear`                                                                                                              | The fiscal year configuration.                       | *required* |
| `totals_selection` | `TotalsSelection`                                                                                                         | The totals selection configuration for the calendar. | *required* |

## WeeksGeneralCalendar

Parameters:

| Name             | Type                                                                                                                      | Description                                          | Default    |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- | ---------- |
| `calendar_type`  | `Literal['Calendar Months/Quarters/Years', 'Weeks: 4-4-5, 4-5-4 or 5-4-4', 'Weeks: General', 'Weeks: 13 4-week Periods']` | The type of calendar used.                           | *required* |
| `current_period` | `PartialCurrentPeriod`                                                                                                    | The current period configuration.                    | *required* |
| `start_date`     | `str`                                                                                                                     | The start date of the calendar in YYYY-MM-DD format. | *required* |
| `weeks_count`    | `int`                                                                                                                     | The number of weeks in the calendar.                 | *required* |

## WeeksPeriodsCalendar

Parameters:

| Name                 | Type                                                                                                                      | Description                                          | Default    |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- | ---------- |
| `calendar_type`      | `Literal['Calendar Months/Quarters/Years', 'Weeks: 4-4-5, 4-5-4 or 5-4-4', 'Weeks: General', 'Weeks: 13 4-week Periods']` | The type of calendar used.                           | *required* |
| `current_period`     | `PartialCurrentPeriod`                                                                                                    | The current period configuration.                    | *required* |
| `fiscal_year`        | `FiscalYear`                                                                                                              | The fiscal year configuration.                       | *required* |
| `past_years_count`   | `int`                                                                                                                     | The number of past years included.                   | *required* |
| `future_years_count` | `int`                                                                                                                     | The number of future years included.                 | *required* |
| `extra_week_month`   | `int`                                                                                                                     | The month in which the extra week is included.       | *required* |
| `week_format`        | `Literal['Numbered', 'Week Commencing', 'Week Ending']`                                                                   | The format of the week.                              | *required* |
| `totals_selection`   | `TotalsSelectionWithQuarter`                                                                                              | The totals selection configuration for the calendar. | *required* |

## WeeksGroupingCalendar

Parameters:

| Name                 | Type                                                                                                                      | Description                                                         | Default    |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | ---------- |
| `calendar_type`      | `Literal['Calendar Months/Quarters/Years', 'Weeks: 4-4-5, 4-5-4 or 5-4-4', 'Weeks: General', 'Weeks: 13 4-week Periods']` | The type of calendar used.                                          | *required* |
| `current_period`     | `PartialCurrentPeriod`                                                                                                    | The current period configuration.                                   | *required* |
| `fiscal_year`        | `FiscalYear`                                                                                                              | The fiscal year configuration.                                      | *required* |
| `past_years_count`   | `int`                                                                                                                     | The number of past years included.                                  | *required* |
| `future_years_count` | `int`                                                                                                                     | The number of future years included.                                | *required* |
| `extra_week_month`   | `int`                                                                                                                     | The month in which the extra week is included.                      | *required* |
| `week_format`        | `Literal['Numbered', 'Week Commencing', 'Week Ending']`                                                                   | The format of the week.                                             | *required* |
| `totals_selection`   | `TotalsSelection`                                                                                                         | The totals selection configuration for the calendar.                | *required* |
| `week_grouping`      | `str`                                                                                                                     | The week grouping configuration, e.g. '4-4-5', '4-5-4', or '5-4-4'. | *required* |
