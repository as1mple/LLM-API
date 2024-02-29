from pydantic import BaseModel


class UserMessage(BaseModel):
    prompt: str


class AnswerMessage(BaseModel):
    message: str
