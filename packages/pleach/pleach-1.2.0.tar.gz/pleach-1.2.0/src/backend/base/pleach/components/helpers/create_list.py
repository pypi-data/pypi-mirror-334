from pleach.custom import Component
from pleach.inputs import StrInput
from pleach.schema import Data
from pleach.template import Output


class CreateListComponent(Component):
    display_name = "Create List"
    description = "Creates a list of texts."
    icon = "list"
    name = "CreateList"
    legacy = True

    inputs = [
        StrInput(
            name="texts",
            display_name="Texts",
            info="Enter one or more texts.",
            is_list=True,
        ),
    ]

    outputs = [
        Output(display_name="Data List", name="list", method="create_list"),
    ]

    def create_list(self) -> list[Data]:
        data = [Data(text=text) for text in self.texts]
        self.status = data
        return data
