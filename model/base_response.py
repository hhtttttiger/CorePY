from pydantic import BaseModel


class FileReader(BaseModel):
    succeed: bool
    data: any
    msg: str