from fasthtml.common import *
from fasthtml import common as fh
from starlette.testclient import TestClient

def render(todo):
    tid = f"todo-{todo.id}"
    toggle = A("Done", hx_get=f"/toggle/{todo.id}", target_id=tid)
    delete = A("Delete", hx_delete=f"/delete/{todo.id}", hx_swap="delete", target_id=tid)

    return Li(toggle,
              delete,
              todo.title + (" ✅" if todo.done else ""),
              id=tid)

app, rt, todos, Todo = fh.fast_app(
    db_file='todos.db', 
    id=int,
    pk='id',
    title=str, 
    done=bool,
    render=render,
    live=True,
    )

def mk_input():
    return Input(type="text", placeholder="Add a new task", id="title", hx_swap_oob="true")

@rt("/")
def get():
    form = Form(
        Group(mk_input(), Button("Add")),
        hx_post="/",
        hx_target="#todo-list",
        hx_swap="beforeend",
    )
    return (
        Titled(
            "Tasks",
            Card(
                Ul(*todos(), id="todo-list"),
                header=form
            )
            
        )
    )

@rt("/")
def post(todo: Todo):
    return todos.insert(todo), mk_input()

@rt("/delete/{id}")
def delete(id: int):
    todos.delete(id)
    

@rt("/toggle/{id}")
def get(id: int):
    todo = todos[id]
    todo.done = not todo.done
    todos.update(todo)
    return todo

client = TestClient(app)
print(client.get("/").text)

fh.serve()