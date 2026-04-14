from pydantic import BaseModel

class ArticleInfo(BaseModel):
    title: str
    url: str
    text: str
    sentiment: str