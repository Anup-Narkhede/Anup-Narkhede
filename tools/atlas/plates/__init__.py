"""Plate registry. Each builder takes a Theme and returns a list of Plates."""
from . import delivery, exhibits, finale, hero, planes, seals, sections, signal, strata

PLATES = {
    "hero": lambda t: [hero.build(t)],
    "delivery": lambda t: [delivery.build(t)],
    "planes": lambda t: [planes.build(t)],
    "strata": lambda t: [strata.build(t)],
    "sections": sections.build_all,
    "exhibits": exhibits.build_all,
    "seals": seals.build_all,
    "signal": lambda t: [signal.build(t)],
    "finale": lambda t: [finale.build(t)],
}
