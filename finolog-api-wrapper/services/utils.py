from pydantic import BaseModel


def serialise_pydantic(model: BaseModel):
    json = model.model_dump_json(exclude_none=True)
    return json
