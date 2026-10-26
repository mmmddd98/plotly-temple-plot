
from dash import Dash, dcc, html

from temple_plot import TemplePlot
from demo_data import DEMO_CLASSES, DEMO_CLASSES_ALT

app = Dash(__name__)

landscape_fig = TemplePlot(
    DEMO_CLASSES,
    title="Temple composition",
    orientation="landscape",
    master_legend_title="Datasets",
    composition_legend_title="Evidence levels",
    composition_axis_title="Share within dataset",
    master_axis_title="Total evidence",
).create_figure()

portrait_fig = TemplePlot(
    DEMO_CLASSES_ALT,
    title="Temple composition, portrait",
    orientation="portrait",
    width=760,
    height=900,
    master_legend_title="Datasets",
    composition_legend_title="Evidence levels",
    composition_axis_title="Share within dataset",
    master_axis_title="Total evidence",
).create_figure()

app.layout = html.Div([
    html.H1("Temple Plot"),
    dcc.Graph(
        figure=landscape_fig,
        style={"height": "58vh"},
    ),
    dcc.Graph(
        figure=portrait_fig,
        style={"height": "92vh"},
    ),
])

if __name__ == "__main__":
    app.run(debug=True)
