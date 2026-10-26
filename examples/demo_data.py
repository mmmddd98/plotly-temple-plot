MODIFICATION_COLORS = {
    "dimethyl": "#7C3AED",
    "free": "#14B8A6",
    "acetyl": "#F59E0B",
}

ALT_MODIFICATION_COLORS = {
    "dimethyl": "#8B5CF6",
    "free": "#20C5B5",
    "acetyl": "#F7A928",
}

AGE_COLORS = {
    "0-14": "#4E79A7",
    "15-64": "#F28E2B",
    "65+": "#59A14F",
}

LAND_USE_COLORS = {
    "agriculture": "#E3A64A",
    "forest": "#4C9B6B",
    "urban": "#7B8794",
    "other": "#8B6F47",
}

BUDGET_COLORS = {
    "housing": "#4E79A7",
    "food": "#59A14F",
    "transport": "#F28E2B",
    "health": "#E15759",
    "leisure/savings": "#B07AA1",
}


DEMO_CLASSES = [
    {
        "name": "Discovery",
        "color": "#2F6F9F",
        "fractions": [
            {
                "name": "batch_A",
                "segments": {
                    "high confidence": 42,
                    "shared": 18,
                    "low evidence": 7,
                },
            },
            {
                "name": "batch_B",
                "segments": {
                    "high confidence": 31,
                    "shared": 25,
                    "low evidence": 11,
                },
            },
        ],
    },
    {
        "name": "Validation",
        "color": "#C44536",
        "fractions": [
            {
                "name": "batch_A",
                "segments": {
                    "high confidence": 28,
                    "shared": 34,
                    "low evidence": 8,
                },
            },
            {
                "name": "batch_B",
                "segments": {
                    "high confidence": 36,
                    "shared": 22,
                    "low evidence": 15,
                },
            },
            {
                "name": "batch_C",
                "segments": {
                    "high confidence": 19,
                    "shared": 39,
                    "low evidence": 12,
                },
            },
        ],
    },
    {
        "name": "Reference",
        "color": "#3F8F64",
        "fractions": [
            {
                "name": "curated",
                "segments": {
                    "high confidence": 12,
                    "shared": 4,
                    "low evidence": 2,
                },
            },
            {
                "name": "extended",
                "segments": {
                    "high confidence": 8,
                    "shared": 7,
                    "low evidence": 2,
                },
            },
        ],
    },
]


TERMINI_DEMO_CLASSES = [
    {
        "name": "semi_Nterm",
        "color": "#636EFA",
        "fractions": [
            {
                "name": "baseline",
                "segments": {
                    "dimethyl": 70,
                    "free": 110,
                    "acetyl": 20,
                },
                "segment_colors": MODIFICATION_COLORS,
            },
            {
                "name": "replicate_A",
                "segments": {
                    "dimethyl": 35,
                    "free": 50,
                    "acetyl": 15,
                },
                "segment_colors": MODIFICATION_COLORS,
            },
        ],
    },
    {
        "name": "specific",
        "color": "#EF553B",
        "fractions": [
            {
                "name": "baseline",
                "segments": {
                    "dimethyl": 55,
                    "free": 175,
                    "acetyl": 50,
                },
                "segment_colors": MODIFICATION_COLORS,
            },
            {
                "name": "replicate_A",
                "segments": {
                    "dimethyl": 30,
                    "free": 95,
                    "acetyl": 25,
                },
                "segment_colors": MODIFICATION_COLORS,
            },
            {
                "name": "replicate_B",
                "segments": {
                    "dimethyl": 35,
                    "free": 105,
                    "acetyl": 30,
                },
                "segment_colors": MODIFICATION_COLORS,
            },
        ],
    },
    {
        "name": "semi_Cterm",
        "color": "#00CC96",
        "fractions": [
            {
                "name": "baseline",
                "segments": {
                    "dimethyl": 5,
                    "free": 50,
                    "acetyl": 10,
                },
                "segment_colors": MODIFICATION_COLORS,
            },
            {
                "name": "replicate_A",
                "segments": {
                    "dimethyl": 3,
                    "free": 27,
                    "acetyl": 5,
                },
                "segment_colors": MODIFICATION_COLORS,
            },
        ],
    },
]


def _with_palette(classes, class_colors, segment_colors=None):
    recolored = []
    for cls in classes:
        new_cls = {
            **cls,
            "color": class_colors.get(cls["name"], cls.get("color")),
            "fractions": [],
        }
        for frac in cls["fractions"]:
            new_frac = {**frac}
            if segment_colors:
                new_frac["segment_colors"] = {
                    **frac.get("segment_colors", {}),
                    **segment_colors,
                }
            new_cls["fractions"].append(new_frac)
        recolored.append(new_cls)
    return recolored


DEMO_CLASSES_ALT = _with_palette(
    DEMO_CLASSES,
    {
        "Discovery": "#3B82B6",
        "Validation": "#D05545",
        "Reference": "#4C9B6B",
    },
)


TERMINI_DEMO_CLASSES_ALT = _with_palette(
    TERMINI_DEMO_CLASSES,
    {
        "semi_Nterm": "#7287FF",
        "specific": "#F2654F",
        "semi_Cterm": "#13BFA0",
    },
    ALT_MODIFICATION_COLORS,
)


CONTINENT_AGE_CLASSES = [
    {
        "name": "Asia",
        "color": "#2F6F9F",
        "fractions": [
            {
                "name": "population",
                "segments": {"0-14": 1120, "15-64": 3180, "65+": 450},
                "segment_colors": AGE_COLORS,
            }
        ],
    },
    {
        "name": "Africa",
        "color": "#C44536",
        "fractions": [
            {
                "name": "population",
                "segments": {"0-14": 610, "15-64": 835, "65+": 45},
                "segment_colors": AGE_COLORS,
            }
        ],
    },
    {
        "name": "Europe",
        "color": "#3F8F64",
        "fractions": [
            {
                "name": "population",
                "segments": {"0-14": 118, "15-64": 476, "65+": 150},
                "segment_colors": AGE_COLORS,
            }
        ],
    },
    {
        "name": "Americas",
        "color": "#8B5FBF",
        "fractions": [
            {
                "name": "population",
                "segments": {"0-14": 240, "15-64": 670, "65+": 130},
                "segment_colors": AGE_COLORS,
            }
        ],
    },
]


INCOME_GROUP_AGE_CLASSES = [
    {
        "name": "Low income",
        "color": "#C44536",
        "fractions": [
            {"name": "population", "segments": {"0-14": 240, "15-64": 310, "65+": 18}, "segment_colors": AGE_COLORS}
        ],
    },
    {
        "name": "Lower-middle",
        "color": "#D68910",
        "fractions": [
            {"name": "population", "segments": {"0-14": 760, "15-64": 1720, "65+": 145}, "segment_colors": AGE_COLORS}
        ],
    },
    {
        "name": "Upper-middle",
        "color": "#2F6F9F",
        "fractions": [
            {"name": "population", "segments": {"0-14": 690, "15-64": 2430, "65+": 410}, "segment_colors": AGE_COLORS}
        ],
    },
    {
        "name": "High income",
        "color": "#3F8F64",
        "fractions": [
            {"name": "population", "segments": {"0-14": 210, "15-64": 780, "65+": 260}, "segment_colors": AGE_COLORS}
        ],
    },
]


LAND_USE_CLASSES = [
    {
        "name": "Africa",
        "color": "#C44536",
        "fractions": [
            {
                "name": "land area",
                "segments": {"agriculture": 1160, "forest": 640, "urban": 38, "other": 1190},
                "segment_colors": LAND_USE_COLORS,
            }
        ],
    },
    {
        "name": "Asia",
        "color": "#2F6F9F",
        "fractions": [
            {
                "name": "land area",
                "segments": {"agriculture": 1650, "forest": 620, "urban": 90, "other": 870},
                "segment_colors": LAND_USE_COLORS,
            }
        ],
    },
    {
        "name": "Europe",
        "color": "#3F8F64",
        "fractions": [
            {
                "name": "land area",
                "segments": {"agriculture": 470, "forest": 360, "urban": 55, "other": 135},
                "segment_colors": LAND_USE_COLORS,
            }
        ],
    },
    {
        "name": "Americas",
        "color": "#8B5FBF",
        "fractions": [
            {
                "name": "land area",
                "segments": {"agriculture": 1220, "forest": 1580, "urban": 70, "other": 1130},
                "segment_colors": LAND_USE_COLORS,
            }
        ],
    },
]


HOUSEHOLD_BUDGET_CLASSES = [
    {
        "name": "Students",
        "color": "#2F6F9F",
        "fractions": [
            {
                "name": "monthly budget",
                "segments": {"housing": 620, "food": 260, "transport": 90, "health": 45, "leisure/savings": 165},
                "segment_colors": BUDGET_COLORS,
            }
        ],
    },
    {
        "name": "Families",
        "color": "#C44536",
        "fractions": [
            {
                "name": "monthly budget",
                "segments": {"housing": 1650, "food": 860, "transport": 520, "health": 310, "leisure/savings": 760},
                "segment_colors": BUDGET_COLORS,
            }
        ],
    },
    {
        "name": "Singles",
        "color": "#3F8F64",
        "fractions": [
            {
                "name": "monthly budget",
                "segments": {"housing": 980, "food": 390, "transport": 240, "health": 130, "leisure/savings": 520},
                "segment_colors": BUDGET_COLORS,
            }
        ],
    },
    {
        "name": "Retirees",
        "color": "#8B5FBF",
        "fractions": [
            {
                "name": "monthly budget",
                "segments": {"housing": 760, "food": 420, "transport": 120, "health": 360, "leisure/savings": 340},
                "segment_colors": BUDGET_COLORS,
            }
        ],
    },
]
