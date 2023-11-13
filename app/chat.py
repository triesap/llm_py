from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from langchain.chains import ConversationChain
from lanarky import LangchainRouter
from lanarky.testing import mount_gradio_app
from langchain.llms import Ollama

llm = Ollama(
    model="orca-mini",
)

def create_chain():
    return ConversationChain(
        llm=llm,
        verbose=True,
    )


app = mount_gradio_app(FastAPI(title="llm_py"))
templates = Jinja2Templates(directory="templates")
chain = create_chain()


@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


langchain_router = LangchainRouter(
    langchain_url="/chat", langchain_object=chain, streaming_mode=1
)
langchain_router.add_langchain_api_route(
    "/chat_json", langchain_object=chain, streaming_mode=2
)
langchain_router.add_langchain_api_websocket_route("/ws", langchain_object=chain)

app.include_router(langchain_router)
