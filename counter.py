from fasthtml.common import *
from fasthtml.common import FastHTML
from starlette.testclient import TestClient

app = FastHTML()

count = 0

@app.get("/")
def home():
    return (
        Title("Counter"), 
        Main(
            H1("Counter"),
            P(f"Count is set to {count}", cls="count"),
            Button(
                "Increment", 
                hx_post="/increment",
                hx_target=".count",
                hx_swap="innerHTML"
                )
        )
    )

@app.post("/increment")
def increment():
    print("Incrementing")
    global count
    count += 1
    return f"Count set to {count}\n"
