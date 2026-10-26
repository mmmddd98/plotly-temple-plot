from math import isfinite
from numbers import Real
import json
import uuid

import plotly.graph_objects as go
import plotly.io as pio


DEFAULT_SEGMENT_COLORS = [
    "#4E79A7",
    "#F28E2B",
    "#59A14F",
    "#E15759",
    "#76B7B2",
    "#EDC948",
    "#B07AA1",
    "#FF9DA7",
]

DEFAULT_CLASS_COLORS = [
    "#2F6F9F",
    "#C44536",
    "#3F8F64",
    "#8B5FBF",
    "#D68910",
    "#4D908E",
]


class TempleFigure(go.Figure):
    def __init__(self, *args, temple_fields=None, temple_legends=None, temple_model=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._temple_fields = temple_fields or []
        self._temple_legends = temple_legends or []
        self._temple_model = temple_model or {}

    def _repr_html_(self):
        return self.to_temple_html(include_plotlyjs=True)

    def show(self, *args, **kwargs):
        try:
            from IPython.display import HTML, display
        except ImportError:
            return super().show(*args, **kwargs)

        display(HTML(self.to_temple_html(include_plotlyjs=True)))
        return None

    def to_temple_html(self, include_plotlyjs=True):
        plot_id = f"temple-{uuid.uuid4().hex}"
        plot_html = pio.to_html(
            self,
            include_plotlyjs=include_plotlyjs,
            full_html=False,
            div_id=plot_id,
            config={"displayModeBar": True, "responsive": True},
        )
        fields_json = json.dumps(self._temple_fields)
        legends_json = json.dumps(self._temple_legends)
        model_json = json.dumps(self._temple_model)
        return f"""
<div class="temple-wrap" data-temple="{plot_id}">
  <div class="temple-plot">{plot_html}</div>
  <div class="temple-ui" aria-label="Temple controls"></div>
  <div class="temple-tooltip" role="tooltip"></div>
</div>
<style>
  .temple-wrap {{
    position: relative;
    display: inline-block;
    width: fit-content;
    max-width: 100%;
    overflow: visible;
  }}
  .temple-plot {{
    display: block;
  }}
  .temple-ui {{
    position: absolute;
    z-index: 1000;
    width: 176px;
    padding: 0;
    border: 0;
    background: transparent;
    font: 14px Arial, sans-serif;
    color: #263442;
    pointer-events: auto;
    user-select: none;
  }}
  .temple-legend-section + .temple-legend-section {{
    margin-top: 18px;
    padding-top: 12px;
    border-top: 1px solid #C9D3DF;
  }}
  .temple-legend-title {{
    margin-bottom: 7px;
    font-weight: 700;
    color: #111827;
    letter-spacing: 0;
  }}
  .temple-legend-item {{
    display: flex;
    align-items: center;
    gap: 7px;
    width: 100%;
    margin: 3px 0;
    border: 0;
    background: transparent;
    color: inherit;
    cursor: pointer;
    padding: 3px 0;
    text-align: left;
    font: inherit;
  }}
  .temple-legend-item:hover {{
    color: #0f172a;
  }}
  .temple-legend-item.is-off {{
    opacity: 0.35;
  }}
  .temple-swatch {{
    width: 12px;
    height: 12px;
    border-radius: 1px;
    border: 1px solid rgba(17, 24, 39, 0.32);
    flex: 0 0 auto;
  }}
  .temple-tooltip {{
    display: none;
    position: absolute;
    z-index: 10;
    max-width: 220px;
    padding: 8px 9px;
    border: 1px solid #d7dee8;
    background: rgba(255, 255, 255, 0.96);
    box-shadow: 0 3px 10px rgba(15, 23, 42, 0.10);
    color: #1f2933;
    font: 14px Arial, sans-serif;
    line-height: 1.25;
    pointer-events: none;
  }}
  .temple-tooltip::before {{
    content: "";
    position: absolute;
    left: -7px;
    top: 50%;
    transform: translateY(-50%);
    border-top: 7px solid transparent;
    border-bottom: 7px solid transparent;
    border-right: 7px solid #d7dee8;
  }}
  .temple-tooltip::after {{
    content: "";
    position: absolute;
    left: -6px;
    top: 50%;
    transform: translateY(-50%);
    border-top: 6px solid transparent;
    border-bottom: 6px solid transparent;
    border-right: 6px solid rgba(255, 255, 255, 0.96);
  }}
  .temple-tooltip.left::before {{
    left: auto;
    right: -7px;
    border-right: 0;
    border-left: 7px solid #d7dee8;
  }}
  .temple-tooltip.left::after {{
    left: auto;
    right: -6px;
    border-right: 0;
    border-left: 6px solid rgba(255, 255, 255, 0.96);
  }}
</style>
<script>
(function() {{
  const plotId = {json.dumps(plot_id)};
  const baseFields = {fields_json};
  let activeFields = baseFields.slice();
  const legends = {legends_json};
  const model = {model_json};

  function init() {{
    const wrap = document.querySelector('[data-temple="' + plotId + '"]');
    const gd = document.getElementById(plotId);
    if (!wrap || !gd || !gd._fullLayout) {{
      window.setTimeout(init, 50);
      return;
    }}

    const tooltip = wrap.querySelector('.temple-tooltip');
    const ui = wrap.querySelector('.temple-ui');
    if (!legends.length) {{
      ui.style.display = 'none';
    }}
    const hidden = new Set();

    function positionLegend() {{
      if (!legends.length) return;
      const layout = gd._fullLayout;
      const margin = layout.margin || {{}};
      const left = Math.max(0, layout.width - (margin.r || 0) + 18);
      const top = Math.max(0, (margin.t || 0) + 22);
      ui.style.left = left + 'px';
      ui.style.top = top + 'px';
    }}

    function traceMeta(trace) {{
      return trace.meta || {{}};
    }}

    function classHidden(className) {{
      return hidden.has('master:' + className);
    }}

    function segmentHidden(segmentName) {{
      return hidden.has('segment:' + segmentName);
    }}

    function activeSegmentsFor(cls) {{
      return Object.keys(cls.segments).filter(function(segmentName) {{
        return !segmentHidden(segmentName) && cls.segments[segmentName] > 0;
      }});
    }}

    function activeClassItems() {{
      return model.classes.filter(function(cls) {{
        return !classHidden(cls.name) && activeSegmentsFor(cls).length > 0;
      }});
    }}

    function fieldHtml(className, fractionName, segmentName, rawValue, normalized) {{
      return '<b>' + className + '</b><br>' +
        'Fraction: ' + fractionName + '<br>' +
        'Segment: ' + segmentName + '<br>' +
        'Raw value: ' + rawValue + '<br>' +
        'Normalized: ' + (normalized * 100).toFixed(1) + '%';
    }}

    function masterHtml(cls, total) {{
      return '<b>' + cls.name + '</b><br>' +
        'Fractions: ' + (cls.fractions || '') + '<br>' +
        'Total value: ' + total;
    }}

    function renderLegend() {{
      ui.innerHTML = '';
      if (!legends.length) return;
      legends.forEach(function(section) {{
        const sectionEl = document.createElement('div');
        sectionEl.className = 'temple-legend-section';
        const title = document.createElement('div');
        title.className = 'temple-legend-title';
        title.textContent = section.title;
        sectionEl.appendChild(title);
        section.items.forEach(function(item) {{
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.className = 'temple-legend-item';
          btn.dataset.group = item.group;
          const swatch = document.createElement('span');
          swatch.className = 'temple-swatch';
          swatch.style.background = item.color;
          const label = document.createElement('span');
          label.textContent = item.label;
          btn.appendChild(swatch);
          btn.appendChild(label);
          btn.addEventListener('click', function(event) {{
            event.preventDefault();
            event.stopPropagation();
            if (hidden.has(item.group)) {{
              hidden.delete(item.group);
              btn.classList.remove('is-off');
            }} else {{
              hidden.add(item.group);
              btn.classList.add('is-off');
            }}
            updateVisibility();
            hideTooltip();
          }});
          sectionEl.appendChild(btn);
        }});
        ui.appendChild(sectionEl);
      }});
    }}

    function updateVisibility() {{
      const layout = computeLayout();
      activeFields = layout.fields;
      gd.data.forEach(function(trace, index) {{
        const meta = traceMeta(trace);
        const entry = layout.byClass[meta.class];
        const segmentEntry = entry && meta.segment ? entry.segments[meta.segment] : null;
        let update = {{visible: true}};

        if (meta.role === 'master') {{
          if (!entry) update.visible = false;
          else if (model.orientation === 'portrait') {{
            update.x = [[layout.masterX1 - layout.masterX0]];
            update.y = [[entry.height]];
            update.base = [[entry.y0]];
            update.width = [[layout.masterX1 - layout.masterX0]];
          }} else {{
            update.x = [[(entry.x0 + entry.x1) / 2]];
            update.y = [[layout.masterY1 - layout.masterY0]];
            update.base = [[layout.masterY0]];
            update.width = [[entry.width]];
          }}
        }} else if (meta.role === 'segment') {{
          if (!segmentEntry) update.visible = false;
          else if (model.orientation === 'portrait') {{
            update.x = [[segmentEntry.x1 - segmentEntry.x0]];
            update.y = [[entry.yCenter]];
            update.base = [[segmentEntry.x0]];
            update.width = [[model.barWidth]];
          }} else {{
            update.x = [[entry.xCenter]];
            update.y = [[segmentEntry.y1 - segmentEntry.y0]];
            update.base = [[segmentEntry.y0]];
            update.width = [[model.barWidth]];
          }}
        }} else if (meta.role === 'connector') {{
          if (!entry) update.visible = false;
          else {{
            const p = connectorPoints(layout, entry, meta.edge);
            update.x = [p.x];
            update.y = [p.y];
          }}
        }} else if (meta.role === 'master_hover') {{
          if (!entry) update.visible = false;
          else {{
            const box = entry.masterBox;
            update.x = [[box.x0, box.x1, box.x1, box.x0, box.x0]];
            update.y = [[box.y0, box.y0, box.y1, box.y1, box.y0]];
            update.customdata = [[entry.masterHtml, entry.masterHtml, entry.masterHtml, entry.masterHtml, entry.masterHtml]];
          }}
        }} else if (meta.role === 'segment_hover') {{
          if (!segmentEntry) update.visible = false;
          else {{
            const box = segmentEntry.box;
            update.x = [[box.x0, box.x1, box.x1, box.x0, box.x0]];
            update.y = [[box.y0, box.y0, box.y1, box.y1, box.y0]];
            update.customdata = [[segmentEntry.html, segmentEntry.html, segmentEntry.html, segmentEntry.html, segmentEntry.html]];
          }}
        }} else if (trace.legendgroup && hidden.has(trace.legendgroup)) {{
          update.visible = false;
        }}
        Plotly.restyle(gd, update, [index]);
      }});
      (gd.layout.annotations || []).forEach(function(annotation) {{
        const annotationMeta = parseAnnotationName(annotation.name);
        if (annotationMeta && annotationMeta.class) {{
          const entry = layout.byClass[annotationMeta.class];
          annotation.visible = !!entry;
          if (entry && annotationMeta.role === 'master_label') {{
            if (model.orientation === 'portrait') {{
              annotation.x = layout.masterX0 - 0.2;
              annotation.y = entry.yCenter;
            }} else {{
              annotation.x = entry.xCenter;
              annotation.y = layout.masterY1 + 0.2;
            }}
          }} else if (entry && annotationMeta.role === 'fraction_label') {{
            annotation.x = entry.xCenter;
          }}
        }}
      }});
      const relayout = {{annotations: gd.layout.annotations}};
      if (model.orientation === 'portrait') {{
        relayout['yaxis.range'] = [-0.35, Math.max(layout.extent + 0.2, 0.2)];
      }} else {{
        relayout['xaxis.range'] = [-0.35, Math.max(layout.extent + 0.2, 0.2)];
      }}
      Plotly.relayout(gd, relayout);
    }}

    function computeLayout() {{
      const activeClasses = activeClassItems();
      const visibleTotals = activeClasses.map(function(cls) {{
        return activeSegmentsFor(cls).reduce(function(total, segmentName) {{
          return total + cls.segments[segmentName];
        }}, 0);
      }});
      const grandTotal = visibleTotals.reduce(function(total, value) {{ return total + value; }}, 0);
      const byClass = {{}};
      const fields = [];
      let cursor = 0;
      const masterY0 = model.compositionSize + 0.55;
      const masterY1 = masterY0 + model.masterSize;
      const masterX0 = -model.masterSize - 0.55;
      const masterX1 = -0.55;
      const minCenterDistance = model.barWidth + model.minBarGap;
      const desiredCenters = [];

      activeClasses.forEach(function(cls, classIndex) {{
        const classTotal = visibleTotals[classIndex];
        const span = grandTotal ? classTotal / grandTotal * activeClasses.length : 1;
        const entry = {{
          className: cls.name,
          total: classTotal,
          width: span,
          height: span,
          segments: {{}},
        }};
        if (model.orientation === 'portrait') {{
          entry.y0 = cursor;
          entry.y1 = cursor + span;
          entry.yCenter = (entry.y0 + entry.y1) / 2;
          desiredCenters.push(entry.yCenter);
          entry.masterBox = {{x0: masterX0, x1: masterX1, y0: entry.y0, y1: entry.y1}};
        }} else {{
          entry.x0 = cursor;
          entry.x1 = cursor + span;
          entry.xCenter = (entry.x0 + entry.x1) / 2;
          desiredCenters.push(entry.xCenter);
          entry.masterBox = {{x0: entry.x0, x1: entry.x1, y0: masterY0, y1: masterY1}};
        }}

        entry.masterHtml = masterHtml(cls, classTotal);
        fields.push(Object.assign({{html: entry.masterHtml, group: 'master:' + cls.name}}, entry.masterBox));
        byClass[cls.name] = entry;
        cursor += span;
      }});

      const separatedCenters = separatedPositions(desiredCenters, minCenterDistance, model.barWidth / 2);
      const compositionExtent = separatedCenters.length
        ? Math.max(cursor, separatedCenters[separatedCenters.length - 1] + model.barWidth / 2)
        : cursor;
      activeClasses.forEach(function(cls, classIndex) {{
        const entry = byClass[cls.name];
        const center = separatedCenters[classIndex];
        if (model.orientation === 'portrait') {{
          entry.yCenter = center;
        }} else {{
          entry.xCenter = center;
        }}
      }});

      activeClasses.forEach(function(cls) {{
        const entry = byClass[cls.name];
        let running = 0;
        activeSegmentsFor(cls).forEach(function(segmentName) {{
          const value = cls.segments[segmentName];
          const classTotal = entry.total;
          const normalized = classTotal ? value / classTotal : 0;
          const size = normalized * model.compositionSize;
          const segment = {{html: fieldHtml(cls.name, cls.name, segmentName, value, normalized)}};
          if (model.orientation === 'portrait') {{
            segment.x0 = running;
            segment.x1 = running + size;
            segment.y0 = entry.yCenter - model.barWidth / 2;
            segment.y1 = entry.yCenter + model.barWidth / 2;
          }} else {{
            segment.x0 = entry.xCenter - model.barWidth / 2;
            segment.x1 = entry.xCenter + model.barWidth / 2;
            segment.y0 = running;
            segment.y1 = running + size;
          }}
          segment.box = {{x0: segment.x0, x1: segment.x1, y0: segment.y0, y1: segment.y1}};
          entry.segments[segmentName] = segment;
          fields.push(Object.assign({{html: segment.html, group: 'segment:' + segmentName}}, segment.box));
          running += size;
        }});
      }});

      return {{
        byClass: byClass,
        fields: fields,
        extent: compositionExtent,
        masterY0: masterY0,
        masterY1: masterY1,
        masterX0: masterX0,
        masterX1: masterX1,
      }};
    }}

    function separatedPositions(desired, minDistance, minCenter) {{
      if (desired.length <= 1) return desired.slice();
      const blocks = [];
      desired.forEach(function(value, index) {{
        blocks.push({{start: index, end: index, weight: 1, mean: value - index * minDistance}});
        while (blocks.length >= 2) {{
          const last = blocks[blocks.length - 1];
          const previous = blocks[blocks.length - 2];
          if (previous.mean <= last.mean) break;
          const weight = previous.weight + last.weight;
          previous.mean = (previous.mean * previous.weight + last.mean * last.weight) / weight;
          previous.weight = weight;
          previous.end = last.end;
          blocks.pop();
        }}
      }});
      const positions = new Array(desired.length);
      blocks.forEach(function(block) {{
        for (let index = block.start; index <= block.end; index += 1) {{
          positions[index] = block.mean + index * minDistance;
        }}
      }});
      if (positions[0] < minCenter) {{
        const offset = minCenter - positions[0];
        for (let index = 0; index < positions.length; index += 1) positions[index] += offset;
      }}
      return positions;
    }}

    function connectorPoints(layout, entry, edge) {{
      if (model.orientation === 'portrait') {{
        const y = edge === 'start' ? entry.masterBox.y0 : entry.masterBox.y1;
        const targetY = edge === 'start'
          ? entry.yCenter - model.barWidth / 2
          : entry.yCenter + model.barWidth / 2;
        return {{x: [layout.masterX1, 0], y: [y, targetY]}};
      }}
      const x = edge === 'start' ? entry.masterBox.x0 : entry.masterBox.x1;
      const targetX = edge === 'start'
        ? entry.xCenter - model.barWidth / 2
        : entry.xCenter + model.barWidth / 2;
      return {{x: [x, targetX], y: [layout.masterY0, model.compositionSize]}};
    }}

    function parseAnnotationName(name) {{
      if (!name || name.indexOf('temple|') !== 0) return null;
      const parts = name.split('|');
      return {{role: parts[1], class: parts.slice(2).join('|')}};
    }}

    function dataFromMouse(event) {{
      const rect = gd.getBoundingClientRect();
      const xa = gd._fullLayout.xaxis;
      const ya = gd._fullLayout.yaxis;
      const px = event.clientX - rect.left;
      const py = event.clientY - rect.top;
      return {{
        x: xa.p2l(px - xa._offset),
        y: ya.p2l(py - ya._offset),
        px: px,
        py: py,
        xa: xa,
        ya: ya,
      }};
    }}

    function findField(pos) {{
      for (let i = activeFields.length - 1; i >= 0; i -= 1) {{
        const field = activeFields[i];
        if (hidden.has(field.group)) continue;
        if (pos.x >= field.x0 && pos.x <= field.x1 && pos.y >= field.y0 && pos.y <= field.y1) {{
          return field;
        }}
      }}
      return null;
    }}

    function showTooltip(field, pos) {{
      const wrapRect = wrap.getBoundingClientRect();
      const gdRect = gd.getBoundingClientRect();
      const cx = pos.xa.l2p((field.x0 + field.x1) / 2) + pos.xa._offset + gdRect.left - wrapRect.left;
      const cy = pos.ya.l2p((field.y0 + field.y1) / 2) + pos.ya._offset + gdRect.top - wrapRect.top;
      tooltip.innerHTML = field.html;
      tooltip.style.display = 'block';
      tooltip.classList.remove('left');
      const tw = tooltip.offsetWidth;
      const th = tooltip.offsetHeight;
      let left = cx + 10;
      if (left + tw > wrap.clientWidth - 4) {{
        left = cx - tw - 10;
        tooltip.classList.add('left');
      }}
      tooltip.style.left = left + 'px';
      tooltip.style.top = (cy - th / 2) + 'px';
    }}

    function hideTooltip() {{
      tooltip.style.display = 'none';
    }}

    gd.addEventListener('mousemove', function(event) {{
      const pos = dataFromMouse(event);
      const field = findField(pos);
      if (field) {{
        showTooltip(field, pos);
      }} else {{
        hideTooltip();
      }}
    }});
    gd.addEventListener('mouseleave', hideTooltip);

    renderLegend();
    positionLegend();
    gd.on('plotly_relayout', positionLegend);
    window.addEventListener('resize', positionLegend);
    gd.layout.showlegend = false;
    Plotly.relayout(gd, {{showlegend: false}});
  }}
  init();
}})();
</script>
"""


class TemplePlot:
    """
    Plotly implementation of a Temple-style composition plot.

    Input shape:
    - classes: master categories, usually 2-4 items
    - fractions: bars below/next to each master category
    - segments: normalized composition inside each fraction
    """

    def __init__(
        self,
        classes,
        width=1180,
        height=680,
        orientation="landscape",
        bar_width=0.48,
        fraction_gap=0.12,
        class_gap=0.62,
        master_size=1.35,
        composition_size=4.6,
        aggregate_classes=True,
        show_legend=True,
        composition_gridlines=True,
        min_bar_gap=0.18,
        master_legend_title="Groups",
        composition_legend_title="Segments",
        composition_axis_title="Share within group",
        master_axis_title="Total by group",
        title=None,
    ):
        self.classes = classes
        self.width = width
        self.height = height
        self.orientation = orientation
        self.bar_width = bar_width
        self.fraction_gap = fraction_gap
        self.class_gap = class_gap
        self.master_size = master_size
        self.composition_size = composition_size
        self.aggregate_classes = aggregate_classes
        self.show_legend = show_legend
        self.composition_gridlines = composition_gridlines
        self.min_bar_gap = min_bar_gap
        self.master_legend_title = master_legend_title
        self.composition_legend_title = composition_legend_title
        self.composition_axis_title = composition_axis_title
        self.master_axis_title = master_axis_title
        self.title = title

    def create_figure(self):
        orientation = self._normalize_orientation(self.orientation)
        self._validate()

        fig = TempleFigure()
        segment_colors = self._segment_color_map()
        self._legend_entries_added = set()
        self._legend_section_titles_added = set()
        self._legend_section_counts = {self.master_legend_title: 0, self.composition_legend_title: 0}
        self._temple_fields = []
        self._temple_legend_sections = []
        self._temple_legend_groups = set()

        if orientation == "landscape":
            extent = self._add_landscape(fig, segment_colors)
            self._style_landscape(fig, extent)
        else:
            extent = self._add_portrait(fig, segment_colors)
            self._style_portrait(fig, extent)

        fig.update_layout(
            width=self.width,
            height=self.height,
            template="plotly_white",
            barmode="overlay",
            title=dict(text=self.title, x=0.24, y=0.965, xanchor="left", yanchor="top", font=dict(size=20))
            if self.title
            else None,
            font=dict(family="Arial, sans-serif", size=13, color="#1F2933"),
            paper_bgcolor="white",
            plot_bgcolor="white",
            showlegend=False,
            hovermode=False,
            hoverlabel=dict(bgcolor="white", bordercolor="#D7DEE8", font_size=14),
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02,
                title=None,
                traceorder="normal",
                groupclick="togglegroup",
                tracegroupgap=8,
            ),
        )
        fig._temple_fields = self._temple_fields
        fig._temple_legends = self._temple_legend_sections
        fig._temple_model = self._temple_model(orientation, segment_colors)

        return fig

    def _add_landscape(self, fig, segment_colors):
        current_x = 0
        master_y0 = self.composition_size + 0.55
        master_y1 = master_y0 + self.master_size
        layouts = []

        for class_index, cls in enumerate(self.classes):
            fractions = cls["fractions"]
            class_width = self._class_width(cls)
            class_x0 = current_x
            class_x1 = current_x + class_width
            if self.aggregate_classes:
                master_x0 = class_x0
                master_x1 = class_x1
            else:
                master_x0 = class_x0 - (self.class_gap / 2 if class_index else 0)
                master_x1 = class_x1 + (self.class_gap / 2 if class_index < len(self.classes) - 1 else 0)
            layouts.append(
                {
                    "cls": cls,
                    "fractions": fractions,
                    "class_index": class_index,
                    "class_x0": class_x0,
                    "class_x1": class_x1,
                    "master_x0": master_x0,
                    "master_x1": master_x1,
                    "desired_center": (class_x0 + class_x1) / 2,
                }
            )
            current_x = class_x1 if self.aggregate_classes else class_x1 + self.class_gap

        master_extent = max(current_x if self.aggregate_classes else current_x - self.class_gap, 0)
        adjusted_centers = self._separated_positions(
            [layout["desired_center"] for layout in layouts],
            self.bar_width + self.min_bar_gap,
            self.bar_width / 2,
        )
        extent = master_extent

        for layout, adjusted_center in zip(layouts, adjusted_centers):
            cls = layout["cls"]
            fractions = layout["fractions"]
            class_index = layout["class_index"]
            class_x0 = layout["class_x0"]
            class_x1 = layout["class_x1"]
            master_x0 = layout["master_x0"]
            master_x1 = layout["master_x1"]
            class_color = cls.get("color", DEFAULT_CLASS_COLORS[class_index % len(DEFAULT_CLASS_COLORS)])
            master_group = f"master:{cls['name']}"

            self._add_rect(
                fig,
                master_x0,
                master_x1,
                master_y0,
                master_y1,
                class_color,
                width=0.7,
                legendgroup=master_group,
                legend_name=cls["name"],
                legend_section=self.master_legend_title,
                meta={"role": "master", "class": cls["name"]},
            )
            self._add_master_label(
                fig,
                (class_x0 + class_x1) / 2,
                master_y1 + 0.2,
                cls["name"],
                meta={"role": "master_label", "class": cls["name"]},
            )

            if self.aggregate_classes:
                x_center = adjusted_center
                frac = self._aggregate_fraction(cls)
                self._add_vertical_fraction(fig, cls["name"], frac, x_center, segment_colors)
                self._add_fraction_label(
                    fig,
                    x_center,
                    -0.35,
                    cls["name"],
                    angle=0,
                    meta={"role": "fraction_label", "class": cls["name"]},
                )
                composition_x0 = x_center - self.bar_width / 2
                composition_x1 = x_center + self.bar_width / 2
                extent = max(extent, composition_x1)
            else:
                for fraction_index, frac in enumerate(fractions):
                    x_center = class_x0 + fraction_index * (1 + self.fraction_gap) + 0.5
                    self._add_vertical_fraction(fig, cls["name"], frac, x_center, segment_colors)
                    self._add_fraction_label(fig, x_center, -0.35, frac["name"], angle=45)
                composition_x0 = class_x0 + 0.5 - self.bar_width / 2
                composition_x1 = class_x1 - 0.5 + self.bar_width / 2
                extent = max(extent, composition_x1)

            self._add_master_connector(
                fig,
                orientation="landscape",
                master_x0=master_x0,
                master_x1=master_x1,
                master_y0=master_y0,
                master_y1=master_y1,
                composition_x0=composition_x0,
                composition_x1=composition_x1,
                composition_y0=0,
                composition_y1=self.composition_size,
                legendgroup=master_group,
                class_name=cls["name"],
            )
            self._add_master_hover_bar(
                fig,
                cls,
                orientation="landscape",
                x0=master_x0,
                x1=master_x1,
                y0=master_y0,
                y1=master_y1,
                legendgroup=master_group,
            )

        self._add_composition_gridlines(fig, orientation="landscape", extent=extent)
        self._add_composition_axis_label(fig, orientation="landscape")
        self._add_master_axis_label(fig, orientation="landscape", master_y0=master_y0, master_y1=master_y1)
        self._add_composition_tick_labels(fig, orientation="landscape")
        return extent

    def _add_portrait(self, fig, segment_colors):
        current_y = 0
        master_x0 = -self.master_size - 0.55
        master_x1 = -0.55
        layouts = []

        for class_index, cls in enumerate(self.classes):
            fractions = cls["fractions"]
            class_height = self._class_width(cls)
            class_y0 = current_y
            class_y1 = current_y + class_height
            if self.aggregate_classes:
                master_y0 = class_y0
                master_y1 = class_y1
            else:
                master_y0 = class_y0 - (self.class_gap / 2 if class_index else 0)
                master_y1 = class_y1 + (self.class_gap / 2 if class_index < len(self.classes) - 1 else 0)
            layouts.append(
                {
                    "cls": cls,
                    "fractions": fractions,
                    "class_index": class_index,
                    "class_y0": class_y0,
                    "class_y1": class_y1,
                    "master_y0": master_y0,
                    "master_y1": master_y1,
                    "desired_center": (class_y0 + class_y1) / 2,
                }
            )
            current_y = class_y1 if self.aggregate_classes else class_y1 + self.class_gap

        master_extent = max(current_y if self.aggregate_classes else current_y - self.class_gap, 0)
        adjusted_centers = self._separated_positions(
            [layout["desired_center"] for layout in layouts],
            self.bar_width + self.min_bar_gap,
            self.bar_width / 2,
        )
        extent = master_extent

        for layout, adjusted_center in zip(layouts, adjusted_centers):
            cls = layout["cls"]
            fractions = layout["fractions"]
            class_index = layout["class_index"]
            class_y0 = layout["class_y0"]
            class_y1 = layout["class_y1"]
            master_y0 = layout["master_y0"]
            master_y1 = layout["master_y1"]
            class_color = cls.get("color", DEFAULT_CLASS_COLORS[class_index % len(DEFAULT_CLASS_COLORS)])
            master_group = f"master:{cls['name']}"

            self._add_rect(
                fig,
                master_x0,
                master_x1,
                master_y0,
                master_y1,
                class_color,
                width=0.7,
                legendgroup=master_group,
                legend_name=cls["name"],
                legend_section=self.master_legend_title,
                meta={"role": "master", "class": cls["name"]},
            )
            self._add_master_label(
                fig,
                master_x0 - 0.2,
                (class_y0 + class_y1) / 2,
                cls["name"],
                angle=-90,
                xanchor="right",
                yanchor="middle",
                meta={"role": "master_label", "class": cls["name"]},
            )

            if self.aggregate_classes:
                y_center = adjusted_center
                frac = self._aggregate_fraction(cls)
                self._add_horizontal_fraction(fig, cls["name"], frac, y_center, segment_colors)
                composition_y0 = y_center - self.bar_width / 2
                composition_y1 = y_center + self.bar_width / 2
                extent = max(extent, composition_y1)
            else:
                for fraction_index, frac in enumerate(fractions):
                    y_center = class_y0 + fraction_index * (1 + self.fraction_gap) + 0.5
                    self._add_horizontal_fraction(fig, cls["name"], frac, y_center, segment_colors)
                composition_y0 = class_y0 + 0.5 - self.bar_width / 2
                composition_y1 = class_y1 - 0.5 + self.bar_width / 2
                extent = max(extent, composition_y1)

            self._add_master_connector(
                fig,
                orientation="portrait",
                master_x0=master_x0,
                master_x1=master_x1,
                master_y0=master_y0,
                master_y1=master_y1,
                composition_x0=0,
                composition_x1=self.composition_size,
                composition_y0=composition_y0,
                composition_y1=composition_y1,
                legendgroup=master_group,
                class_name=cls["name"],
            )
            self._add_master_hover_bar(
                fig,
                cls,
                orientation="portrait",
                x0=master_x0,
                x1=master_x1,
                y0=master_y0,
                y1=master_y1,
                legendgroup=master_group,
            )

        self._add_composition_gridlines(fig, orientation="portrait", extent=extent)
        self._add_master_axis_label(fig, orientation="portrait", master_x0=master_x0, master_x1=master_x1, extent=extent)
        return extent

    def _add_vertical_fraction(self, fig, class_name, frac, x_center, segment_colors):
        total = sum(frac["segments"].values())
        running_y = 0

        for segment_name, value in frac["segments"].items():
            normalized = value / total if total else 0
            segment_height = normalized * self.composition_size
            color = frac.get("segment_colors", {}).get(segment_name, segment_colors[segment_name])

            self._add_rect(
                fig,
                x_center - self.bar_width / 2,
                x_center + self.bar_width / 2,
                running_y,
                running_y + segment_height,
                color,
                legendgroup=f"segment:{segment_name}",
                legend_name=segment_name,
                legend_section=self.composition_legend_title,
                meta={"role": "segment", "class": class_name, "segment": segment_name},
            )
            self._add_segment_hover_area(
                fig,
                x_center - self.bar_width / 2,
                x_center + self.bar_width / 2,
                running_y,
                running_y + segment_height,
                class_name,
                frac["name"],
                segment_name,
                value,
                normalized,
                legendgroup=f"segment:{segment_name}",
            )
            running_y += segment_height

    def _add_horizontal_fraction(self, fig, class_name, frac, y_center, segment_colors):
        total = sum(frac["segments"].values())
        running_x = 0

        for segment_name, value in frac["segments"].items():
            normalized = value / total if total else 0
            segment_width = normalized * self.composition_size
            color = frac.get("segment_colors", {}).get(segment_name, segment_colors[segment_name])

            self._add_rect(
                fig,
                running_x,
                running_x + segment_width,
                y_center - self.bar_width / 2,
                y_center + self.bar_width / 2,
                color,
                orientation="horizontal",
                legendgroup=f"segment:{segment_name}",
                legend_name=segment_name,
                legend_section=self.composition_legend_title,
                meta={"role": "segment", "class": class_name, "segment": segment_name},
            )
            self._add_segment_hover_area(
                fig,
                running_x,
                running_x + segment_width,
                y_center - self.bar_width / 2,
                y_center + self.bar_width / 2,
                class_name,
                frac["name"],
                segment_name,
                value,
                normalized,
                legendgroup=f"segment:{segment_name}",
            )
            running_x += segment_width

    def _add_rect(
        self,
        fig,
        x0,
        x1,
        y0,
        y1,
        color,
        width=0.8,
        orientation="vertical",
        legendgroup=None,
        legend_name=None,
        legend_section=None,
        meta=None,
    ):
        self._add_custom_legend_item(legend_section, legendgroup, legend_name, color)
        legend_options = self._legend_options(legendgroup, legend_name, legend_section)
        marker = dict(color=color, line=dict(color="white", width=width))
        if orientation == "horizontal":
            fig.add_trace(
                go.Bar(
                    x=[x1 - x0],
                    y=[(y0 + y1) / 2],
                    base=[x0],
                    width=[y1 - y0],
                    orientation="h",
                    marker=marker,
                    hoverinfo="skip",
                    meta=meta,
                    **legend_options,
                )
            )
            return

        fig.add_trace(
            go.Bar(
                x=[(x0 + x1) / 2],
                y=[y1 - y0],
                base=[y0],
                width=[x1 - x0],
                marker=marker,
                hoverinfo="skip",
                meta=meta,
                **legend_options,
            )
        )

    def _add_master_connector(
        self,
        fig,
        orientation,
        master_x0,
        master_x1,
        master_y0,
        master_y1,
        composition_x0,
        composition_x1,
        composition_y0,
        composition_y1,
        legendgroup=None,
        class_name=None,
    ):
        line = dict(color="rgba(100, 116, 139, 0.68)", width=1.6, dash="dot")
        if orientation == "landscape":
            self._add_line(fig, master_x0, master_y0, composition_x0, composition_y1, line, legendgroup, {"role": "connector", "class": class_name, "edge": "start"})
            self._add_line(fig, master_x1, master_y0, composition_x1, composition_y1, line, legendgroup, {"role": "connector", "class": class_name, "edge": "end"})
            return

        self._add_line(fig, master_x1, master_y0, composition_x0, composition_y0, line, legendgroup, {"role": "connector", "class": class_name, "edge": "start"})
        self._add_line(fig, master_x1, master_y1, composition_x0, composition_y1, line, legendgroup, {"role": "connector", "class": class_name, "edge": "end"})

    def _add_line(self, fig, x0, y0, x1, y1, line, legendgroup=None, meta=None):
        fig.add_trace(
            go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                mode="lines",
                line=line,
                hoverinfo="skip",
                showlegend=False,
                legendgroup=legendgroup,
                meta=meta,
            )
        )

    def _add_segment_hover_area(
        self,
        fig,
        x0,
        x1,
        y0,
        y1,
        class_name,
        fraction_name,
        segment_name,
        value,
        normalized,
        legendgroup=None,
    ):
        hover_text = (
            f"<b>{class_name}</b><br>"
            f"Fraction: {fraction_name}<br>"
            f"Segment: {segment_name}<br>"
            f"Raw value: {value:g}<br>"
            f"Normalized: {normalized:.1%}"
        )
        self._add_hover_area(
            fig,
            x0,
            x1,
            y0,
            y1,
            hover_text,
            legendgroup=legendgroup,
            meta={"role": "segment_hover", "class": class_name, "segment": segment_name},
        )

    def _add_hover_area(self, fig, x0, x1, y0, y1, hover_text, legendgroup=None, meta=None):
        self._record_field(x0, x1, y0, y1, hover_text, legendgroup)
        fig.add_trace(
            go.Scatter(
                x=[x0, x1, x1, x0, x0],
                y=[y0, y0, y1, y1, y0],
                mode="lines",
                fill="toself",
                fillcolor="rgba(255,255,255,0.01)",
                hoveron="fills",
                hoverinfo="text",
                hovertemplate="%{customdata}<extra></extra>",
                line=dict(color="rgba(0,0,0,0)", width=0),
                name="",
                showlegend=False,
                legendgroup=legendgroup,
                customdata=[hover_text] * 5,
                meta=meta,
            )
        )

    def _add_master_hover_bar(self, fig, cls, orientation, x0, x1, y0, y1, legendgroup=None):
        fraction_count = len(cls["fractions"])
        total = sum(sum(frac["segments"].values()) for frac in cls["fractions"])
        fraction_label = "Fraction" if fraction_count == 1 else "Fractions"
        hover_text = (
            f"<b>{cls['name']}</b><br>"
            f"{fraction_label}: {fraction_count}<br>"
            f"Total value: {total:g}"
        )

        self._add_hover_area(
            fig,
            x0,
            x1,
            y0,
            y1,
            hover_text,
            legendgroup=legendgroup,
            meta={"role": "master_hover", "class": cls["name"]},
        )

    def _add_master_label(self, fig, x, y, text, angle=0, xanchor="center", yanchor="bottom", meta=None):
        fig.add_annotation(
            x=x,
            y=y,
            text=f"<b>{text}</b>",
            showarrow=False,
            textangle=angle,
            xanchor=xanchor,
            yanchor=yanchor,
            font=dict(size=15, color="#111827"),
            name=self._annotation_name(meta),
        )

    def _add_fraction_label(self, fig, x, y, text, angle=0, xanchor="center", meta=None):
        fig.add_annotation(
            x=x,
            y=y,
            text=text,
            showarrow=False,
            textangle=angle,
            xanchor=xanchor,
            yanchor="top" if angle else "middle",
            font=dict(size=12, color="#334155"),
            name=self._annotation_name(meta),
        )

    def _add_composition_axis_label(self, fig, orientation):
        if not self.composition_axis_title:
            return

        if orientation == "landscape":
            fig.add_annotation(
                x=-0.29,
                y=self.composition_size / 2,
                text=self.composition_axis_title,
                showarrow=False,
                textangle=-90,
                xanchor="center",
                yanchor="middle",
                font=dict(size=16, color="#111827"),
            )
            return

        fig.add_annotation(
            x=self.composition_size / 2,
            y=-0.45,
            text=self.composition_axis_title,
            showarrow=False,
            xanchor="center",
            yanchor="top",
            font=dict(size=14, color="#111827"),
        )

    def _add_master_axis_label(self, fig, orientation, master_y0=None, master_y1=None, master_x0=None, master_x1=None, extent=None):
        if not self.master_axis_title:
            return

        if orientation == "landscape":
            fig.add_annotation(
                x=-0.29,
                y=(master_y0 + master_y1) / 2,
                text=self.master_axis_title,
                showarrow=False,
                textangle=-90,
                xanchor="center",
                yanchor="middle",
                font=dict(size=14, color="#111827"),
            )
            return

        fig.add_annotation(
            x=(master_x0 + master_x1) / 2,
            y=max(extent or 0, 0) + 0.28,
            text=self.master_axis_title,
            showarrow=False,
            xanchor="center",
            yanchor="bottom",
            font=dict(size=14, color="#111827"),
        )

    def _add_composition_tick_labels(self, fig, orientation):
        if orientation != "landscape":
            return

        for value, label in [
            (0, "0%"),
            (self.composition_size * 0.25, "25%"),
            (self.composition_size * 0.5, "50%"),
            (self.composition_size * 0.75, "75%"),
            (self.composition_size, "100%"),
        ]:
            fig.add_annotation(
                x=-0.065,
                y=value,
                text=label,
                showarrow=False,
                xanchor="right",
                yanchor="middle",
                font=dict(size=14, color="#1F2933"),
            )

    def _add_composition_gridlines(self, fig, orientation, extent):
        if not self.composition_gridlines:
            return

        line = dict(color="rgba(100, 116, 139, 0.16)", width=1)
        values = [
            0,
            self.composition_size * 0.25,
            self.composition_size * 0.5,
            self.composition_size * 0.75,
            self.composition_size,
        ]

        if orientation == "landscape":
            for value in values:
                fig.add_shape(
                    type="line",
                    x0=0.02,
                    x1=max(extent, 0.02),
                    y0=value,
                    y1=value,
                    line=line,
                    layer="below",
                )
            return

        for value in values:
            fig.add_shape(
                type="line",
                x0=value,
                x1=value,
                y0=0,
                y1=max(extent, 0),
                line=line,
                layer="below",
            )

    def _legend_options(self, legendgroup, legend_name, legend_section):
        if not legendgroup:
            return {"showlegend": False}

        showlegend = self.show_legend and legendgroup not in self._legend_entries_added
        options = {
            "name": legend_name or "",
            "legendgroup": legendgroup,
            "showlegend": showlegend,
        }
        if showlegend:
            self._legend_entries_added.add(legendgroup)
            if legend_section in self._legend_section_counts:
                section_base = 100 if legend_section == self.master_legend_title else 300
                options["legendrank"] = section_base + self._legend_section_counts[legend_section]
                self._legend_section_counts[legend_section] += 1
            if legend_section and legend_section not in self._legend_section_titles_added:
                options["legendgrouptitle_text"] = legend_section
                self._legend_section_titles_added.add(legend_section)
        return options

    def _add_custom_legend_item(self, section, group, label, color):
        if not self.show_legend or not section or not group or group in self._temple_legend_groups:
            return

        for legend_section in self._temple_legend_sections:
            if legend_section["title"] == section:
                legend_section["items"].append({"group": group, "label": label, "color": color})
                self._temple_legend_groups.add(group)
                return

        self._temple_legend_sections.append(
            {
                "title": section,
                "items": [{"group": group, "label": label, "color": color}],
            }
        )
        self._temple_legend_groups.add(group)

    def _record_field(self, x0, x1, y0, y1, html, group):
        self._temple_fields.append(
            {
                "x0": min(x0, x1),
                "x1": max(x0, x1),
                "y0": min(y0, y1),
                "y1": max(y0, y1),
                "html": html,
                "group": group,
            }
        )

    def _annotation_name(self, meta):
        if not meta:
            return None
        return f"temple|{meta.get('role', '')}|{meta.get('class', '')}"

    def _style_landscape(self, fig, extent):
        top = self.composition_size + self.master_size + 1.0
        fig.update_layout(margin=dict(l=148, r=220 if self.show_legend else 24, t=78, b=92))
        fig.update_xaxes(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-0.3, extent + 0.16],
            fixedrange=False,
        )
        fig.update_yaxes(
            title=None,
            tickfont=dict(size=14),
            tickformat=".0%",
            tickvals=[
                0,
                self.composition_size * 0.25,
                self.composition_size * 0.5,
                self.composition_size * 0.75,
                self.composition_size,
            ],
            showticklabels=False,
            range=[-0.9, top],
            showgrid=False,
            ticks="",
            zeroline=False,
            fixedrange=False,
        )

    def _style_portrait(self, fig, extent):
        right = self.composition_size + 0.2
        fig.update_layout(margin=dict(l=142, r=220 if self.show_legend else 28, t=78, b=62))
        fig.update_xaxes(
            title=dict(text="Normalized composition", standoff=18, font=dict(size=14)),
            tickformat=".0%",
            tickvals=[
                0,
                self.composition_size * 0.25,
                self.composition_size * 0.5,
                self.composition_size * 0.75,
                self.composition_size,
            ],
            ticktext=["0%", "25%", "50%", "75%", "100%"],
            range=[-self.master_size - 1.4, right],
            showgrid=False,
            zeroline=False,
            fixedrange=False,
        )
        fig.update_yaxes(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-0.35, extent + 0.2],
            fixedrange=False,
        )

    def _class_width(self, cls):
        fractions = cls["fractions"]
        if self.aggregate_classes:
            grand_total = self._total_value(self.classes)
            if grand_total == 0:
                return 1
            return self._total_value([cls]) / grand_total * len(self.classes)
        if not fractions:
            return 0
        return len(fractions) + max(len(fractions) - 1, 0) * self.fraction_gap

    def _separated_positions(self, desired_positions, min_distance, min_center):
        if len(desired_positions) <= 1:
            return list(desired_positions)

        blocks = []
        for index, value in enumerate(desired_positions):
            blocks.append(
                {
                    "start": index,
                    "end": index,
                    "weight": 1,
                    "mean": value - index * min_distance,
                }
            )
            while len(blocks) >= 2 and blocks[-2]["mean"] > blocks[-1]["mean"]:
                last = blocks.pop()
                previous = blocks[-1]
                weight = previous["weight"] + last["weight"]
                previous["mean"] = (previous["mean"] * previous["weight"] + last["mean"] * last["weight"]) / weight
                previous["weight"] = weight
                previous["end"] = last["end"]

        positions = [0] * len(desired_positions)
        for block in blocks:
            for index in range(block["start"], block["end"] + 1):
                positions[index] = block["mean"] + index * min_distance

        if positions[0] < min_center:
            offset = min_center - positions[0]
            positions = [position + offset for position in positions]

        return positions

    def _total_value(self, classes):
        return sum(
            sum(frac["segments"].values())
            for cls in classes
            for frac in cls["fractions"]
        )

    def _temple_model(self, orientation, segment_colors):
        classes = []
        for class_index, cls in enumerate(self.classes):
            class_color = cls.get("color", DEFAULT_CLASS_COLORS[class_index % len(DEFAULT_CLASS_COLORS)])
            aggregate = self._aggregate_fraction(cls)
            classes.append(
                {
                    "name": cls["name"],
                    "color": class_color,
                    "fractions": len(cls["fractions"]),
                    "total": sum(aggregate["segments"].values()),
                    "segments": aggregate["segments"],
                }
            )

        return {
            "classes": classes,
            "segmentColors": segment_colors,
            "orientation": orientation,
            "aggregateClasses": self.aggregate_classes,
            "barWidth": self.bar_width,
            "classGap": self.class_gap,
            "fractionGap": self.fraction_gap,
            "masterSize": self.master_size,
            "compositionSize": self.composition_size,
            "minBarGap": self.min_bar_gap,
            "masterLegendTitle": self.master_legend_title,
            "compositionLegendTitle": self.composition_legend_title,
            "compositionAxisTitle": self.composition_axis_title,
            "masterAxisTitle": self.master_axis_title,
        }

    def _aggregate_fraction(self, cls):
        segments = {}
        segment_colors = {}
        for frac in cls["fractions"]:
            for segment_name, value in frac["segments"].items():
                segments[segment_name] = segments.get(segment_name, 0) + value
            segment_colors.update(frac.get("segment_colors", {}))

        return {
            "name": cls["name"],
            "segments": segments,
            "segment_colors": segment_colors,
        }

    def _segment_color_map(self):
        colors = {}
        for cls in self.classes:
            for frac in cls["fractions"]:
                for segment_name in frac["segments"]:
                    if segment_name not in colors:
                        colors[segment_name] = DEFAULT_SEGMENT_COLORS[len(colors) % len(DEFAULT_SEGMENT_COLORS)]
                    if segment_name in frac.get("segment_colors", {}):
                        colors[segment_name] = frac["segment_colors"][segment_name]
        return colors

    def _validate(self):
        if not self.classes:
            raise ValueError("TemplePlot requires at least one class.")
        if not isinstance(self.min_bar_gap, Real) or not isfinite(self.min_bar_gap) or self.min_bar_gap < 0:
            raise ValueError("min_bar_gap must be a non-negative finite number.")

        for cls in self.classes:
            if "name" not in cls or "fractions" not in cls:
                raise ValueError("Each class needs 'name' and 'fractions'.")
            if not cls["fractions"]:
                raise ValueError(f"Class {cls['name']!r} needs at least one fraction.")

            for frac in cls["fractions"]:
                if "name" not in frac or "segments" not in frac:
                    raise ValueError(f"Each fraction in class {cls['name']!r} needs 'name' and 'segments'.")
                if not frac["segments"]:
                    raise ValueError(f"Fraction {frac['name']!r} needs at least one segment.")
                if any(not isinstance(value, Real) for value in frac["segments"].values()):
                    raise ValueError(f"Fraction {frac['name']!r} contains non-numeric segment values.")
                if any(not isfinite(value) for value in frac["segments"].values()):
                    raise ValueError(f"Fraction {frac['name']!r} contains non-finite segment values.")
                if any(value < 0 for value in frac["segments"].values()):
                    raise ValueError(f"Fraction {frac['name']!r} contains negative segment values.")

    def _normalize_orientation(self, orientation):
        aliases = {
            "landscape": "landscape",
            "horizontal": "landscape",
            "wide": "landscape",
            "portrait": "portrait",
            "vertical": "portrait",
            "hochkant": "portrait",
        }
        try:
            return aliases[orientation.lower()]
        except KeyError as exc:
            raise ValueError("orientation must be 'landscape' or 'portrait'.") from exc
