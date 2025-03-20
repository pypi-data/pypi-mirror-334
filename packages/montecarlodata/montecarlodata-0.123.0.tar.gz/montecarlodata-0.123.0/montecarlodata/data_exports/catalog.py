from dataclasses import dataclass


@dataclass
class DataExport:
    name: str
    title: str
    description: str


DATA_EXPORT_CATALOG = [
    DataExport(
        name="ALL_MONITORS",
        title="All monitors",
        description="All monitors with aggregated properties, excluding deleted monitors.",
    ),
    DataExport(
        name="ALL_ASSETS",
        title="All assets",
        description="All assets with aggregated properties, excluding deleted assets.",
    ),
    DataExport(
        name="ALL_ALERTS",
        title="All alerts",
        description="All alerts in the last 90 days with aggregated properties.",
    ),
    DataExport(
        name="ALL_EVENTS",
        title="All events",
        description="All events in the last 90 days with aggregated properties.",
    ),
]
