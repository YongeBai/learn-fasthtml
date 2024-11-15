from fasthtml.common import FastHTML
from fasthtml.common import *
from starlette.testclient import TestClient

css = Style("""
            :root {
                --pico-font-size: 100%;
                --pico-font-family: Pacifico, cursive;
                }            
            """)
app = FastHTML(hdrs=(picolink, css))
messages = ["King gidera take me to ya leader"]

@app.route("/", methods="get")
def home():
    return (
        Main(
            H1("Message"),
            *[P(msg) for msg in messages],
            A("Link to page to page 2", href="/page2")
        )
    )

@app.get("/page2")
def page2():
    return (
        Main(
            P("Add msg with form below:"),
            Form(
                Input(type="text", name="data"),
                Button("Submit"),
                action="/", method="post"
            )
        )
    )

@app.post("/")
def add_msg(data: str):
    messages.append(data)
    return home()

client = TestClient(app)
print(client.get("/").text)