from pydantic import BaseModel, ConfigDict, field_serializer
from pydantic.alias_generators import to_camel


class AnaplanModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    @field_serializer(
        "action_id", "file_id", "process_id", "id", when_used="unless-none", check_fields=False
    )  # While these are of type int, they are serialized as strings in the API payloads
    def str_serializer(self, v: int) -> str:
        return str(v)
