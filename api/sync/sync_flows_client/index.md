Note

This Class is not meant to be instantiated directly, but rather accessed through the `cw.flows` Property on an instance of [Client](https://vinzenzklass.github.io/anaplan-sdk/api/sync/sync_client/index.md). For more details, see the [Guide](https://vinzenzklass.github.io/anaplan-sdk/guides/cloud_works/index.md).

## get_flows

```
get_flows(current_user_only: bool = False) -> list[FlowSummary]
```

List all flows in CloudWorks.

Parameters:

| Name                | Type   | Description                                                  | Default |
| ------------------- | ------ | ------------------------------------------------------------ | ------- |
| `current_user_only` | `bool` | Filters the flows to only those created by the current user. | `False` |

Returns:

| Type                | Description              |
| ------------------- | ------------------------ |
| `list[FlowSummary]` | A list of FlowSummaries. |

## get_flow

```
get_flow(flow_id: str) -> Flow
```

Get a flow by its ID. This returns the full flow object, including the contained steps and continuation behavior.

Parameters:

| Name      | Type  | Description                | Default    |
| --------- | ----- | -------------------------- | ---------- |
| `flow_id` | `str` | The ID of the flow to get. | *required* |

Returns:

| Type   | Description      |
| ------ | ---------------- |
| `Flow` | The Flow object. |

## run_flow

```
run_flow(flow_id: str, only_steps: list[str] | None = None) -> str
```

Run a flow by its ID. Make sure that neither the flow nor any of its contained are running. If this is the case, the task will error. Anaplan neither schedules these tasks nor can it handle concurrent executions.

Parameters:

| Name         | Type        | Description                | Default                                                             |
| ------------ | ----------- | -------------------------- | ------------------------------------------------------------------- |
| `flow_id`    | `str`       | The ID of the flow to run. | *required*                                                          |
| `only_steps` | \`list[str] | None\`                     | A list of step IDs to run. If not provided, only these will be run. |

Returns:

| Type  | Description        |
| ----- | ------------------ |
| `str` | The ID of the run. |

## create_flow

```
create_flow(flow: FlowInput | dict[str, Any]) -> str
```

Create a new flow in CloudWorks. Be careful not to omit the `depends_on` field. Anaplan will accept these values, but an invalid, corrupted flow will be created, as all Flows must have at least 2 Steps, and they must always be sequential

Parameters:

| Name   | Type        | Description      | Default                                                             |
| ------ | ----------- | ---------------- | ------------------------------------------------------------------- |
| `flow` | \`FlowInput | dict[str, Any]\` | The flow to create. This can be a FlowInput object or a dictionary. |

Returns:

| Type  | Description                 |
| ----- | --------------------------- |
| `str` | The ID of the created flow. |

## update_flow

```
update_flow(flow_id: str, flow: FlowInput | dict[str, Any]) -> None
```

Update a flow in CloudWorks. You must provide the full flow object, partial updates are not supported.

Parameters:

| Name      | Type        | Description                   | Default                                                             |
| --------- | ----------- | ----------------------------- | ------------------------------------------------------------------- |
| `flow_id` | `str`       | The ID of the flow to update. | *required*                                                          |
| `flow`    | \`FlowInput | dict[str, Any]\`              | The flow to update. This can be a FlowInput object or a dictionary. |

## delete_flow

```
delete_flow(flow_id: str) -> None
```

Delete a flow in CloudWorks. This will not delete its contained steps. This will fail if the flow is running or if it has any running steps.

Parameters:

| Name      | Type  | Description                   | Default    |
| --------- | ----- | ----------------------------- | ---------- |
| `flow_id` | `str` | The ID of the flow to delete. | *required* |
