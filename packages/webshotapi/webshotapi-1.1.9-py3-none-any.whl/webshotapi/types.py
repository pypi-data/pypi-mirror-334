from typing import TypedDict, Dict, List

class ScreenshotJsonResponse(TypedDict):
    url: str
    expire_sec: int

class PositionType(TypedDict):
    x: int
    y: int
    width: int
    height: int

class ElementType(PositionType, TypedDict):
    xpath: str
    css_selector: str
    style: Dict[str, str]
    attributes: Dict[str, str]

class WordType(TypedDict):
    word: str
    position: PositionType
    word_index: int
    xpath: str
    offset: int

class ViewportType(TypedDict):
    width: int
    height: int

class DocumentType(TypedDict):
    width: int
    height: int

class PagePropertiesType(TypedDict):
    viewport: ViewportType
    document: DocumentType

class SavedInCloudType(TypedDict):
    completed: bool

class ExtractResponse(TypedDict):
    status_code: int
    html: str
    text: str
    elements: List[ElementType]
    words: List[WordType]
    page_properties: PagePropertiesType
    saved_in_cloud: SavedInCloudType