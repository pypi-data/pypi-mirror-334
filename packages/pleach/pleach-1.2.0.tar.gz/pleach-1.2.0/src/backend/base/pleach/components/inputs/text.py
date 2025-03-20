from pleach.base.io.text import TextComponent
from pleach.io import MultilineInput, Output
from pleach.schema.message import Message


class TextInputComponent(TextComponent):
    display_name = "Text Input"
    description = "Get text inputs from the Playground."
    icon = "type"
    name = "TextInput"

    inputs = [
        MultilineInput(
            name="input_value",
            display_name="Text",
            info="Text to be passed as input.",
        ),
    ]
    outputs = [
        Output(display_name="Message", name="text", method="text_response"),
    ]

    def text_response(self) -> Message:
        return Message(
            text=self.input_value,
        )
