from fastapi_pagination import Page

from pleach.helpers.base_model import BaseModel
from pleach.services.database.models.flow.model import Flow
from pleach.services.database.models.folder.model import FolderRead


class FolderWithPaginatedFlows(BaseModel):
    folder: FolderRead
    flows: Page[Flow]
