from dataclasses import dataclass

from llama_cpp import Llama
from llama_cpp import ChatCompletionRequestMessage as Message
from llama_cpp import ChatCompletionRequestSystemMessage as SystemMessage
from llama_cpp import ChatCompletionRequestAssistantMessage as AssistantMessage
from llama_cpp import ChatCompletionRequestUserMessage as UserMessage


@dataclass
class MessageRole:
    ASSISTANT: str = "assistant"
    SYSTEM: str = "system"
    USER: str = "user"
    EXIT: str = "exit"


class ConversationHandler:
    def __init__(self, model: Llama, message_role: MessageRole) -> None:
        self.model: Llama = model
        self.message_role = message_role
        self.messages: list[Message] = [
            SystemMessage(
                role=self.message_role.SYSTEM,
                content='You are a helpful developer assistant, answer all the questions correctly and concisely.'
            ),
            AssistantMessage(role=self.message_role.ASSISTANT, content='Hello, do you have any question?'),
        ]

    def send_message(self, content: str):
        new_message = UserMessage(role=self.message_role.USER, content=content)
        self.messages.append(new_message)

    def generate_reply(self) -> str:
        response = self.model.create_chat_completion(
            messages=self.messages,
            temperature=0.7,
            top_p=0.9,
            top_k=20,
            max_tokens=128
        )

        response_content = response['choices'][0]['message']
        self.messages.append(AssistantMessage(role=self.message_role.ASSISTANT, content=response_content))

        return response_content
