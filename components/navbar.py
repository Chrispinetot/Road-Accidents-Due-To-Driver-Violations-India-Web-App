from dash import html, Dash
import dash_bootstrap_components as dbc

nav_item_1 = dbc.NavItem(dbc.NavLink("Region", href="/page1"))
nav_item_2 = dbc.NavItem(dbc.NavLink("State", href="/page2"))


# define the navbar structure
def Navbar():
    layout = html.Div([
        dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src="assets/logo.png", height="30px")),
                                dbc.Col(dbc.NavbarBrand("Road Accidents Due to Driver "
                                                        "Violations India", className="ms-2")),
                            ],
                            align="center",
                            className="g-0",
                        ),
                        href="https://www.kaggle.com/chrispinetot/road-accidents-india",
                        style={"textDecoration": "none"},
                    ),
                    dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),
                    dbc.Collapse(
                        dbc.Nav(
                            [nav_item_1, nav_item_2],
                            className="ms-auto",
                            navbar=True,
                        ),
                        id="navbar-collapse2",
                        navbar=True,
                    ),
                ],
            ),
            color="dark",
            dark=True,
            className="mb-5",
        )])
    return layout
