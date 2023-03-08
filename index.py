# import libraries
from dash import html, dcc
from dash.dependencies import Input, Output

# connect to main app.py
from app import app, server

# connect to your app pages
from pages import page1, page2

# connect navbar to index
from components import navbar

server = app.server

# define the navbar
nav = navbar.Navbar()

# define the index page layout
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    nav,
    html.Div(id="page-content", children=[]),
])


# create a callback for the multipage inputs
@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/page1":
        return page1.layout
    if pathname == "/page2":
        return page2.layout
    else:
        return page1.layout

# run app
if __name__ == '__main__':
    app.run_server(debug=True)
