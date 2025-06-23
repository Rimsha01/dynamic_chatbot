from pydantic import BaseModel


class UploadData(BaseModel):
    file_name: str
    file_type :str
    description : str


class Chunk(BaseModel):
    file_id :int
    chunk_text : str

class ChatMessage(BaseModel):
    id : int
    query: str
    response: str


