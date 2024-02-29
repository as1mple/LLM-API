import yaml

from llama_cpp import Llama
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.modules.dialog_system import ConversationHandler, MessageRole
from src.modules.data_models import UserMessage, AnswerMessage

router = APIRouter()

with open('config.yml', 'r') as file:
    router.config = yaml.safe_load(file)

router.llm = Llama(
    model_path=router.config['model_path'],
    n_ctx=int(router.config['context_tokens']),
    max_answer_len=int(router.config['max_answer_tokens'])
)

router.conversation = ConversationHandler(
    model=router.llm,
    message_role=MessageRole
)


@router.get("v1/service/status", status_code=status.HTTP_200_OK)
async def health() -> AnswerMessage:
    return AnswerMessage(message="OK")


@router.get("v1/chat/completions", response_model=AnswerMessage)
async def chat_completions(user_message: UserMessage) -> AnswerMessage:
    try:
        router.conversation.send_message(user_message.prompt)
        response = router.conversation.generate_reply()
        return AnswerMessage(message=response)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
