import unittest

from temple_plot import TemplePlot


CLASSES = [
    {
        "name": "A",
        "color": "#111111",
        "fractions": [
            {"name": "F1", "segments": {"X": 2, "Y": 1}},
            {"name": "F2", "segments": {"X": 1, "Y": 3}},
        ],
    },
    {
        "name": "B",
        "color": "#222222",
        "fractions": [
            {"name": "F3", "segments": {"X": 4, "Y": 2}},
        ],
    },
]

PROPORTIONAL_CLASSES = [
    {"name": "semi_Nterm", "color": "#111111", "fractions": [{"name": "all", "segments": {"X": 300}}]},
    {"name": "specific", "color": "#222222", "fractions": [{"name": "all", "segments": {"X": 600}}]},
    {"name": "semi_Cterm", "color": "#333333", "fractions": [{"name": "all", "segments": {"X": 100}}]},
]

TIGHT_CLASSES = [
    {"name": "Large", "color": "#111111", "fractions": [{"name": "all", "segments": {"X": 900}}]},
    {"name": "Small A", "color": "#222222", "fractions": [{"name": "all", "segments": {"X": 40}}]},
    {"name": "Small B", "color": "#333333", "fractions": [{"name": "all", "segments": {"X": 35}}]},
    {"name": "Small C", "color": "#444444", "fractions": [{"name": "all", "segments": {"X": 25}}]},
]


class TemplePlotTest(unittest.TestCase):
    def test_landscape_builds_continuous_master_bar(self):
        fig = TemplePlot(CLASSES).create_figure()
        master_traces = [trace for trace in fig.data if trace.type == "bar" and trace.legendgroup in {"master:A", "master:B"}]
        connector_traces = [trace for trace in fig.data if trace.type == "scatter" and trace.hoverinfo == "skip"]
        first_master = master_traces[0]
        second_master = master_traces[1]

        self.assertEqual(len(fig.layout.shapes), 5)
        self.assertEqual(fig.layout.shapes[0].x0, 0.02)
        self.assertEqual(len(connector_traces), 4)
        self.assertFalse(fig.layout.yaxis.showgrid)
        self.assertEqual(first_master.base[0], second_master.base[0])
        self.assertAlmostEqual(first_master.x[0] + first_master.width[0] / 2, second_master.x[0] - second_master.width[0] / 2)
        self.assertFalse(fig.layout.yaxis.showticklabels)
        annotation_texts = [annotation.text for annotation in fig.layout.annotations]
        self.assertTrue(all(label in annotation_texts for label in ["0%", "25%", "50%", "75%", "100%"]))
        segment_hover = next(trace for trace in fig.data if trace.customdata and "Raw value: 3" in trace.customdata[0])
        self.assertIn("Fraction: A", segment_hover.customdata[0])
        self.assertIn("Normalized: 42.9%", segment_hover.customdata[0])
        self.assertEqual(segment_hover.hoverinfo, "text")
        self.assertEqual(segment_hover.name, "")
        self.assertIsNone(segment_hover.text)
        self.assertEqual(segment_hover.type, "scatter")
        self.assertEqual(segment_hover.hoveron, "fills")
        master_hover = next(trace for trace in fig.data if trace.customdata and "Total value" in trace.customdata[0])
        self.assertEqual(master_hover.type, "scatter")
        self.assertEqual(master_hover.hoveron, "fills")
        self.assertEqual(master_hover.hoverinfo, "text")
        self.assertEqual(master_hover.name, "")
        self.assertIsNone(master_hover.text)
        self.assertIn("<b>A</b>", master_hover.customdata[0])
        self.assertIn("Fractions: 2", master_hover.customdata[0])
        self.assertIn("Total value: 7", master_hover.customdata[0])
        legend_groups = {trace.legendgroup for trace in fig.data if trace.showlegend is True}
        self.assertEqual(legend_groups, {"master:A", "master:B", "segment:X", "segment:Y"})
        self.assertFalse(fig.layout.showlegend)
        self.assertEqual(fig.layout.legend.groupclick, "togglegroup")
        legend_ranks = {trace.name: trace.legendrank for trace in fig.data if trace.showlegend is True}
        self.assertLess(legend_ranks["B"], legend_ranks["X"])
        self.assertLess(legend_ranks["B"], legend_ranks["Y"])

    def test_portrait_rotates_the_layout(self):
        fig = TemplePlot(CLASSES, orientation="portrait").create_figure()
        master_traces = [trace for trace in fig.data if trace.type == "bar" and trace.legendgroup in {"master:A", "master:B"}]
        connector_traces = [trace for trace in fig.data if trace.type == "scatter" and trace.hoverinfo == "skip"]
        first_master = master_traces[0]
        second_master = master_traces[1]

        self.assertEqual(len(fig.layout.shapes), 5)
        self.assertEqual(len(connector_traces), 4)
        self.assertFalse(fig.layout.xaxis.showgrid)
        self.assertEqual(first_master.x[0], second_master.x[0])
        self.assertAlmostEqual(first_master.base[0] + first_master.y[0], second_master.base[0])
        self.assertEqual(fig.layout.xaxis.ticktext, ("0%", "25%", "50%", "75%", "100%"))
        master_hover = next(trace for trace in fig.data if trace.customdata and "Total value" in trace.customdata[0])
        self.assertEqual(master_hover.type, "scatter")
        self.assertEqual(master_hover.hoveron, "fills")
        annotation_texts = [annotation.text for annotation in fig.layout.annotations]
        self.assertNotIn("F1", annotation_texts)
        self.assertNotIn("A", annotation_texts)

    def test_can_keep_one_bar_per_fraction(self):
        fig = TemplePlot(CLASSES, aggregate_classes=False).create_figure()

        connector_traces = [trace for trace in fig.data if trace.type == "scatter" and trace.hoverinfo == "skip"]
        self.assertEqual(len(fig.layout.shapes), 5)
        self.assertEqual(len(connector_traces), 4)
        hover = next(trace for trace in fig.data if trace.customdata and "Fraction: F1" in trace.customdata[0])
        self.assertIn("Fraction: F1", hover.customdata[0])

    def test_can_hide_composition_gridlines(self):
        fig = TemplePlot(CLASSES, composition_gridlines=False).create_figure()

        self.assertFalse(fig.layout.yaxis.showgrid)
        self.assertEqual(len(fig.layout.shapes), 0)

    def test_aggregate_master_bar_uses_class_totals(self):
        fig = TemplePlot(PROPORTIONAL_CLASSES).create_figure()
        master_traces = [
            trace
            for trace in fig.data
            if trace.type == "bar" and trace.legendgroup in {"master:semi_Nterm", "master:specific", "master:semi_Cterm"}
        ]
        widths = [trace.width[0] for trace in master_traces]
        total_width = sum(widths)

        self.assertAlmostEqual(widths[0] / total_width, 0.3, places=6)
        self.assertAlmostEqual(widths[1] / total_width, 0.6, places=6)
        self.assertAlmostEqual(widths[2] / total_width, 0.1, places=6)

    def test_aggregate_composition_bars_keep_minimum_gap(self):
        plot = TemplePlot(TIGHT_CLASSES, min_bar_gap=0.2)
        fig = plot.create_figure()
        centers = [
            trace.x[0]
            for trace in fig.data
            if trace.type == "bar" and trace.meta and trace.meta.get("role") == "segment"
        ]

        min_distance = plot.bar_width + plot.min_bar_gap
        self.assertTrue(all((b - a) + 1e-9 >= min_distance for a, b in zip(centers, centers[1:])))

    def test_aggregate_composition_bars_stay_centered_when_there_is_room(self):
        plot = TemplePlot(PROPORTIONAL_CLASSES, min_bar_gap=0.2)
        fig = plot.create_figure()
        centers = [
            trace.x[0]
            for trace in fig.data
            if trace.type == "bar" and trace.meta and trace.meta.get("role") == "segment"
        ]

        for actual, expected in zip(centers, [0.45, 1.8, 2.85]):
            self.assertAlmostEqual(actual, expected)

    def test_custom_html_contains_split_legend_and_field_metadata(self):
        fig = TemplePlot(CLASSES).create_figure()
        html = fig.to_temple_html(include_plotlyjs=False)

        self.assertIn("temple-ui", html)
        self.assertIn("Groups", html)
        self.assertIn("Segments", html)
        self.assertIn("master:A", html)
        self.assertIn("segment:X", html)
        self.assertIn("Raw value: 3", html)
        self.assertIn("function showTooltip", html)
        self.assertIn("position: absolute", html)
        self.assertIn("function computeLayout", html)
        self.assertIn("function positionLegend", html)
        self.assertIn("layout.width - (margin.r || 0)", html)

    def test_can_customize_legend_and_axis_titles(self):
        fig = TemplePlot(
            CLASSES,
            master_legend_title="Datasets",
            composition_legend_title="Evidence levels",
            composition_axis_title="Share within dataset",
            master_axis_title="Total observations",
        ).create_figure()
        html = fig.to_temple_html(include_plotlyjs=False)
        annotation_texts = [annotation.text for annotation in fig.layout.annotations]

        self.assertIn("Datasets", html)
        self.assertIn("Evidence levels", html)
        self.assertIn("Share within dataset", annotation_texts)
        self.assertIn("Total observations", annotation_texts)

    def test_rejects_invalid_data(self):
        with self.assertRaises(ValueError):
            TemplePlot([{"name": "A", "fractions": []}]).create_figure()

        with self.assertRaises(ValueError):
            TemplePlot(
                [{"name": "A", "fractions": [{"name": "F1", "segments": {"X": -1}}]}]
            ).create_figure()


if __name__ == "__main__":
    unittest.main()
