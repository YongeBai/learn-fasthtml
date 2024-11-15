from fasthtml.common import *
from fasthtml import common as fh
from starlette.testclient import TestClient

app, rt = fast_app(
    live=True
    )

@rt("/")
def get():
    inp = Input(id="new-prompt", name="prompt", placeholder="Enter a prompt")
    add = Form(
        Group(inp, Button("Generate")), hx_post="/", target_id="gen-list", hx_swap="afterbegin"
    )
    gen_list = Div(id="gen-list")
    return (
        Title("Image Generation App"),
        Main(
            H1("Image Generation"),
            add,
            gen_list,
            cls="container"
            )
    )

def generation_preview(id: int):
    if os.path.exists(f"/gens/{id}.png"):
        return Div(
            Img(src=f"/gens/{id}.png"), id=f"gen_{id}"
        )
    else:
        return Div(
            "Generating...", id=f"gen-{id}",
            hx_post=f"/generations/{id}",
            hx_trigger="every 1s", 
            hx_swap="outerHTML",
        )



serve()