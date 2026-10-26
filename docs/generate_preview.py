from pathlib import Path
from temple_plot import TemplePlot

classes = [
    {"name": "Group A", "color": "#2F6F9F", "fractions": [
        {"name": "Batch 1", "segments": {"Category X": 42, "Category Y": 18}},
    ]},
    {"name": "Group B", "color": "#C44536", "fractions": [
        {"name": "Batch 1", "segments": {"Category X": 28, "Category Y": 34}},
    ]},
]
figure = TemplePlot(classes, title="Group composition", width=1000, height=600).create_figure()
figure.add_annotation(x=0.25, y=-0.17, xref="paper", yref="paper",
                      text="■ Category X", font={"color": "#4C78A8", "size": 14}, showarrow=False)
figure.add_annotation(x=0.65, y=-0.17, xref="paper", yref="paper",
                      text="■ Category Y", font={"color": "#F58518", "size": 14}, showarrow=False)
figure.write_image(Path(__file__).with_name("temple-preview.svg"))
figure.write_image(Path(__file__).with_name("temple-preview.png"), scale=1.5)
