from pleach.components.helpers.memory import MemoryComponent
from pleach.components.inputs import ChatInput
from pleach.components.models import OpenAIModelComponent
from pleach.components.outputs import ChatOutput
from pleach.components.prompts import PromptComponent
from pleach.graph import Graph


def memory_chatbot_graph(template: str | None = None):
    if template is None:
        template = """{context}

    User: {user_message}
    AI: """
    memory_component = MemoryComponent()
    chat_input = ChatInput()
    prompt_component = PromptComponent()
    prompt_component.set(
        template=template, user_message=chat_input.message_response, context=memory_component.retrieve_messages_as_text
    )
    openai_component = OpenAIModelComponent()
    openai_component.set(input_value=prompt_component.build_prompt)

    chat_output = ChatOutput()
    chat_output.set(input_value=openai_component.text_response)

    return Graph(chat_input, chat_output)
