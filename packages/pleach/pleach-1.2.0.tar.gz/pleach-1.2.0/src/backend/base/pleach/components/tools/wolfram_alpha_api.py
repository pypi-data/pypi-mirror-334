from langchain_community.utilities.wolfram_alpha import WolframAlphaAPIWrapper

from pleach.base.langchain_utilities.model import LCToolComponent
from pleach.field_typing import Tool
from pleach.inputs import MultilineInput, SecretStrInput
from pleach.schema import Data


class WolframAlphaAPIComponent(LCToolComponent):
    display_name = "WolframAlpha API"
    description = """Enables queries to Wolfram Alpha for computational data, facts, and calculations across various \
topics, delivering structured responses."""
    name = "WolframAlphaAPI"

    inputs = [
        MultilineInput(
            name="input_value", display_name="Input Query", info="Example query: 'What is the population of France?'"
        ),
        SecretStrInput(name="app_id", display_name="App ID", required=True),
    ]

    icon = "WolframAlphaAPI"

    def run_model(self) -> list[Data]:
        wrapper = self._build_wrapper()
        result_str = wrapper.run(self.input_value)
        data = [Data(text=result_str)]
        self.status = data
        return data

    def build_tool(self) -> Tool:
        wrapper = self._build_wrapper()
        return Tool(name="wolfram_alpha_api", description="Answers mathematical questions.", func=wrapper.run)

    def _build_wrapper(self) -> WolframAlphaAPIWrapper:
        return WolframAlphaAPIWrapper(wolfram_alpha_appid=self.app_id)
