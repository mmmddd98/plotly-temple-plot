
from temple_plot import TemplePlot
from demo_data import DEMO_CLASSES

plot = TemplePlot(
    DEMO_CLASSES,
    title="Temple composition",
    orientation="landscape",
    master_legend_title="Datasets",
    composition_legend_title="Evidence levels",
    composition_axis_title="Share within dataset",
    master_axis_title="Total evidence",
)

fig = plot.create_figure()

fig.show()
