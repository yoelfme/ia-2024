from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from langserve import add_routes

from chains.text_to_sql_chain import chain as text_to_sql_chain

origins = [
    "http://localhost",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://127.0.0.1"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Edit this to add the chain you want to add
add_routes(app, text_to_sql_chain, path="/text-to-sql")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
