from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from ParserService import ParserService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ParseRequest(BaseModel):
    url: str
    tag: str | None = None


@app.post("/parse")
def parse_html(req: ParseRequest):
    dom = ParserService.parse_html(req.url)
    dom_dict = dom.__dict__
    dom_dict["children"] = [child.__dict__ for child in dom.children]
    return {"dom": dom_dict}


@app.post("/search")
def search_tag(req: ParseRequest):
    results = ParserService.search_tag(req.url, req.tag)
    return {"results": results}