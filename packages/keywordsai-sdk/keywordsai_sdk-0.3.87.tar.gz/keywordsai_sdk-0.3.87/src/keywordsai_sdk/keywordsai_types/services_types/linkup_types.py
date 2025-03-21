from typing import Optional, List, Literal, Dict, Any
from pydantic import Field
from keywordsai_sdk.keywordsai_types.base_types import KeywordsAIBaseModel


class LinkupParams(KeywordsAIBaseModel):
    """
    Parameters for the Linkup API search endpoint.
    
    Based on the Linkup API documentation: https://docs.linkup.so/pages/documentation/api-reference/endpoint/post-search
    """
    api_key:str
    q: str = Field(..., description="The search query")
    depth: Optional[Literal["standard", "deep"]] = Field(
        None, 
        description="The depth of the search. 'shallow' for faster results, 'deep' for more comprehensive results"
    )
    output_type: Optional[Literal["sourcedAnswer", "structured", "searchResults"]] = Field(
        None, 
        description="The type of output. 'sourcedAnswer' for an answer with sources, 'raw' for raw search results"
    )
    structured_output_schema: Optional[str] = Field(
        None, 
        description="JSON schema for structured output"
    )
    include_images: Optional[bool] = Field(
        None, 
        description="Whether to include images in the response"
    )
    mock_response: Optional['LinkupResponse'] = None
    
    def model_dump(self, *args, **kwargs) -> Dict[str, Any]:
        kwargs["exclude_none"] = True
        return super().model_dump(*args, **kwargs)


class LinkupSource(KeywordsAIBaseModel):
    """
    Represents a source in the Linkup API response.
    """
    name: str
    url: str
    snippet: str


class LinkupResponse(KeywordsAIBaseModel):
    """
    Response from the Linkup API search endpoint.
    """
    answer: str
    sources: List[LinkupSource]
