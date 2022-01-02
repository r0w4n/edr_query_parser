from datetime import datetime

import pytest
from dateutil.parser import isoparse

from edr_query_parser import EDRQueryParser


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://somewhere.com/collections/my_collection/corridor?", "my_collection"),
        ("https://somewhere.com/v1/collections/collections/position?", "collections"),
        ("https://somewhere.com/collections/observations/position?", "observations"),
        ("https://somewhere.com/collections", "EDR URL must contain collections name"),
        (
            "https://somewhere.com/items/my_collection",
            "EDR URL must contain collections name",
        ),
        (
            "collections/my_collection",
            "EDR URL must contain collections name",
        ),
        (
            "/collections/observations/position?",
            "observations",
        ),
    ],
)
def test_collection_name(url, expected):
    try:
        edr_query = EDRQueryParser(url)
        assert edr_query.collection_name == expected
    except ValueError as raised_exception:
        assert str(raised_exception) == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://somewhere.com/collections/my_collection/position?", "position"),
        ("https://somewhere.com/collections/my_collection/radius?", "radius"),
        ("https://somewhere.com/collections/my_collection/area?", "area"),
        ("https://somewhere.com/collections/my_collection/cube?", "cube"),
        ("https://somewhere.com/collections/my_collection/trajectory?", "trajectory"),
        ("https://somewhere.com/collections/my_collection/corridor?", "corridor"),
        ("https://somewhere.com/collections/my_collection/items?", "items"),
        ("https://somewhere.com/collections/my_collection/locations?", "locations"),
        ("https://somewhere.com/collections/metar/locations/EGLL?", "locations"),
        ("https://somewhere.com/collections/metar/items/KIAD_2020-05-19T00Z?", "items"),
        (
            "https://somewhere.com/collections/metar/items/KIAD_2020-05-19T00Z/?",
            "items",
        ),
        (
            "https://somewhere.com/collections/my_collection/not_a_query_type?",
            "unsupported query type found in url",
        ),
        (
            "https://somewhere.com/collections/metar/instances/some_instance/radius?",
            "radius",
        ),
    ],
)
def test_query_type(url, expected):
    try:
        edr_query = EDRQueryParser(url)
        assert edr_query.query_type.value == expected
    except ValueError as raised_exception:
        assert str(raised_exception) == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://somewhere.com/collections/my_collection/position?", True),
        ("https://somewhere.com/collections/my_collection/radius?", False),
        ("https://somewhere.com/collections/my_collection/area?", False),
        ("https://somewhere.com/collections/my_collection/cube?", False),
        ("https://somewhere.com/collections/my_collection/trajectory?", False),
        ("https://somewhere.com/collections/my_collection/corridor?", False),
        ("https://somewhere.com/collections/my_collection/items?", False),
        ("https://somewhere.com/collections/my_collection/locations?", False),
        ("https://somewhere.com/collections/metar/locations/EGLL?", False),
        ("https://somewhere.com/collections/metar/items/KIAD_2020-05-19T00Z?", False),
        ("https://somewhere.com/collections/metar/items/KIAD_2020-05-19T00Z/?", False),
        (
            "https://somewhere.com/collections/metar/instances/some_instance/radius?",
            False,
        ),
        (
            "https://somewhere.com/collections/metar/instances/some_instance/position?",
            True,
        ),
    ],
)
def test_query_type_is_position(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.query_type.is_position == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://somewhere.com/collections/my_collection/position?", False),
        ("https://somewhere.com/collections/my_collection/radius?", True),
    ],
)
def test_query_type_is_radius(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.query_type.is_radius == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://somewhere.com/collections/my_collection/area?", True),
        ("https://somewhere.com/collections/my_collection/radius?", False),
        ("/collections/my_collection/radius?", False),
    ],
)
def test_query_type_is_area(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.query_type.is_area == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://somewhere.com/collections/my_collection/position?", False),
        ("https://somewhere.com/collections/my_collection/cube?", True),
    ],
)
def test_query_type_is_cube(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.query_type.is_cube == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://somewhere.com/collections/my_collection/position?", False),
        ("https://somewhere.com/collections/my_collection/trajectory?", True),
    ],
)
def test_query_type_is_trajectory(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.query_type.is_trajectory == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://somewhere.com/collections/my_collection/position?", False),
        ("https://somewhere.com/collections/my_collection/corridor?", True),
    ],
)
def test_query_type_is_corridor(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.query_type.is_corridor == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://somewhere.com/collections/my_collection/position?", False),
        ("https://somewhere.com/collections/my_collection/items?", True),
        ("https://somewhere.com/collections/my_collection/items/some-item", True),
    ],
)
def test_query_type_is_items(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.query_type.is_items == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://somewhere.com/collections/my_collection/position?", False),
        ("https://somewhere.com/collections/my_collection/locations?", True),
    ],
)
def test_query_type_is_locations(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.query_type.is_locations == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/metar/instances/some_instance/radius?",
            True,
        ),
        ("https://somewhere.com/collections/metar/locations/EGLL?", False),
    ],
)
def test_is_instances(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.is_instances == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/position?parameter-name=parameter1,parameter2",
            ["parameter1", "parameter2"],
        ),
        (
            "https://somewhere.com/collections/my_collection/position?parameter-name=parameter1",
            ["parameter1"],
        ),
        (
            "https://somewhere.com/collections/my_collection/position?parameter-name=parameter1,%20parameter2, parameter3",
            ["parameter1", "parameter2", "parameter3"],
        ),
        (
            "https://somewhere.com/collections/my_collection/position",
            "could not convert parameter to a list",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?parameter-name=&something=1",
            "could not convert parameter to a list",
        ),
        (
            "https://somewhere.com/collections/my_collection/locations/my_locations?parameter-name=parameter1",
            ["parameter1"],
        ),
        (
            "https://somewhere.com/collections/my_collection/locations/my_locations?",
            "could not convert parameter to a list",
        ),
    ],
)
def test_parameter_name(url, expected):
    try:
        edr_query = EDRQueryParser(url)
        assert edr_query.parameter_name.list == expected
    except ValueError as raised_exception:
        assert str(raised_exception) == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/items/my_item_id/",
            "my_item_id",
        ),
        ("https://somewhere.com/collections/my_collection/items/", None),
        ("https://somewhere.com/collections/my_collection/items", None),
        (
            "https://somewhere.com/collections/my_collection/items/my_item?parameter-name=&something=1",
            "my_item",
        ),
        ("https://somewhere.com/collections/my_collection/position", None),
    ],
)
def test_item_id(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.item_id == expected
    assert edr_query.items_id == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/locations/my_location/",
            "my_location",
        ),
        ("https://somewhere.com/collections/my_collection/locations/", None),
        ("https://somewhere.com/collections/my_collection/locations", None),
        (
            "https://somewhere.com/collections/my_collection/locations/my_location?parameter-name=&something=1",
            "my_location",
        ),
        ("https://somewhere.com/collections/my_collection/position", None),
    ],
)
def test_location_id(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.location_id == expected
    assert edr_query.locations_id == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/instances/my_instance/",
            "my_instance",
        ),
        ("https://somewhere.com/collections/my_collection/instances/", None),
        ("https://somewhere.com/collections/my_collection/instances", None),
        (
            "https://somewhere.com/collections/my_collection/instances/my_instance?parameter-name=&something=1",
            "my_instance",
        ),
        (
            "https://somewhere.com/collections/my_collection/my_collection/?parameter-name=&something=1",
            None,
        ),
    ],
)
def test_instance_id(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.instance_id == expected
    assert edr_query.instances_id == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/position?f=geoJson",
            "geoJson",
        ),
        (
            "https://somewhere.com/collections/my_collection/instances/?f=CoverageJSON",
            "CoverageJSON",
        ),
        ("https://somewhere.com/collections/my_collection/instances", None),
        ("https://somewhere.com/collections/my_collection/instances?f=", None),
    ],
)
def test_format_value(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.format.value == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://somewhere.com/collections/my_collection/position?crs=WGS84", "WGS84"),
        ("https://somewhere.com/collections/my_collection/instances", None),
        ("https://somewhere.com/collections/my_collection/instances?crs=", None),
    ],
)
def test_crs_value(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.crs.value == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/position?coords=POINT(0 51.48)",
            {"type": "Point", "coordinates": [0.0, 51.48]},
        ),
        (
            "https://somewhere.com/collections/my_collection/position?coords=MULTIPOINT((38.9 -77),(48.85 2.35),(39.92 116.38),(-35.29 149.1),(51.5 -0.1))",
            {
                "type": "MultiPoint",
                "coordinates": [
                    [38.9, -77.0],
                    [48.85, 2.35],
                    [39.92, 116.38],
                    [-35.29, 149.1],
                    [51.5, -0.1],
                ],
            },
        ),
    ],
)
def test_coords_wkt(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.coords.wkt == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://somewhere.com/collections/my_collection/position?z=12", 12),
        (
            "https://somewhere.com/collections/my_collection/position?z=All",
            "z can not be cast to float",
        ),
        ("https://somewhere.com/collections/my_collection/position?z=12.5", 12.5),
        (
            "https://somewhere.com/collections/my_collection/position?z=500,400",
            "z can not be cast to float",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?z=all",
            "z can not be cast to float",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?z=ALL",
            "z can not be cast to float",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?z=12,23,34",
            "z can not be cast to float",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?z=",
            "z can not be cast to float",
        ),
        (
            "https://somewhere.com/collections/my_collection/position",
            "z can not be cast to float",
        ),
    ],
)
def test_z_float(url, expected):
    try:
        edr_query = EDRQueryParser(url)
        assert edr_query.z.float == expected
    except ValueError as raised_exception:
        assert str(raised_exception) == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://somewhere.com/collections/my_collection/position?z=12/13", 12),
        (
            "https://somewhere.com/collections/my_collection/position?z=500,400",
            "unable to get z from value",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?z=All",
            "unable to get z from value",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?z=12,23,34",
            "unable to get z from value",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?z=",
            "unable to get z from value",
        ),
        (
            "https://somewhere.com/collections/my_collection/position",
            "unable to get z from value",
        ),
    ],
)
def test_z_interval_from(url, expected):
    try:
        edr_query = EDRQueryParser(url)
        assert edr_query.z.interval_from == expected
    except ValueError as raised_exception:
        assert str(raised_exception) == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://somewhere.com/collections/my_collection/position?z=12/13", 13),
        (
            "https://somewhere.com/collections/my_collection/position?z=500,400",
            "unable to get z to value",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?z=All",
            "unable to get z to value",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?z=12,23,34",
            "unable to get z to value",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?z=",
            "unable to get z to value",
        ),
        (
            "https://somewhere.com/collections/my_collection/position",
            "unable to get z to value",
        ),
    ],
)
def test_z_interval_to(url, expected):
    try:
        edr_query = EDRQueryParser(url)
        assert edr_query.z.interval_to == expected
    except ValueError as raised_exception:
        assert str(raised_exception) == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://somewhere.com/collections/my_collection/position?z=12", False),
        ("https://somewhere.com/collections/my_collection/position?z=all", True),
        ("https://somewhere.com/collections/my_collection/position?z=All", True),
        ("https://somewhere.com/collections/my_collection/position?z=ALL", True),
        ("https://somewhere.com/collections/my_collection/position?z=12,23,34", False),
        ("https://somewhere.com/collections/my_collection/position?z=", False),
        ("https://somewhere.com/collections/my_collection/position", False),
    ],
)
def test_z_is_all(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.z.is_all == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://somewhere.com/collections/my_collection/position?z=12/13", False),
        ("https://somewhere.com/collections/my_collection/position?z=500,400", True),
        ("https://somewhere.com/collections/my_collection/position?z=All", False),
        ("https://somewhere.com/collections/my_collection/position?z=12,23,34", True),
        ("https://somewhere.com/collections/my_collection/position?z=", False),
        ("https://somewhere.com/collections/my_collection/position", False),
    ],
)
def test_z_is_list(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.z.is_list == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/position?z=500,400",
            [500, 400],
        ),
        (
            "https://somewhere.com/collections/my_collection/position?z=12,23,34",
            [12, 23, 34],
        ),
        (
            "https://somewhere.com/collections/my_collection/position?z=23/45",
            "could not convert parameter to a list",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?z=",
            "could not convert parameter to a list",
        ),
        (
            "https://somewhere.com/collections/my_collection/position",
            "could not convert parameter to a list",
        ),
    ],
)
def test_z_list(url, expected):
    try:
        edr_query = EDRQueryParser(url)
        assert edr_query.z.list == expected
    except ValueError as raised_exception:
        assert str(raised_exception) == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://somewhere.com/collections/my_collection/position?z=12/13", True),
        ("https://somewhere.com/collections/my_collection/position?z=500/400", True),
        ("https://somewhere.com/collections/my_collection/position?z=All", False),
        ("https://somewhere.com/collections/my_collection/position?z=12,23,34", False),
        ("https://somewhere.com/collections/my_collection/position?z=", False),
        ("https://somewhere.com/collections/my_collection/position", False),
    ],
)
def test_z_is_interval(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.z.is_interval == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/position?coords=POINT(0 51.48)",
            [0.0, 51.48],
        ),
        (
            "https://somewhere.com/collections/my_collection/position?coords=MULTIPOINT((38.9 -77),(48.85 2.35),(39.92 116.38),(-35.29 149.1),(51.5 -0.1))",
            [
                [38.9, -77.0],
                [48.85, 2.35],
                [39.92, 116.38],
                [-35.29, 149.1],
                [51.5, -0.1],
            ],
        ),
        (
            "https://somewhere.com/collections/my_collection/position?coords=",
            "Coords can not be parsed by WKT",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?",
            "Coords can not be parsed by WKT",
        ),
    ],
)
def test_coords_coordinates(url, expected):
    try:
        edr_query = EDRQueryParser(url)
        assert edr_query.coords.coordinates == expected
    except ValueError as raised_exception:
        assert str(raised_exception) == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/position?coords=POINT(0 51.48)",
            "Point",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?coords=MULTIPOINT((38.9 -77),(48.85 2.35),(39.92 116.38),(-35.29 149.1),(51.5 -0.1))",
            "MultiPoint",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?",
            "Coords can not be parsed by WKT",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?coords=",
            "Coords can not be parsed by WKT",
        ),
    ],
)
def test_coords_coords_type(url, expected):
    try:
        edr_query = EDRQueryParser(url)
        assert edr_query.coords.coords_type == expected
    except ValueError as raised_exception:
        assert str(raised_exception) == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z",
            isoparse("2018-02-12T23:20:52Z"),
        ),
        (
            "https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00",
            isoparse("2019-09-07T15:50-04:00"),
        ),
        (
            "https://somewhere.com/collections/my_collection/position?datetime=not_a_date",
            "Datetime format not recognised",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?datetime=23/5/1920",
            "Datetime format not recognised",
        ),
    ],
)
def test_datetime_exact(url, expected):
    try:
        edr_query = EDRQueryParser(url)
        assert edr_query.datetime.exact == expected
    except ValueError as raised_exception:
        assert str(raised_exception) == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z/2018-03-12T23%3A20%3A52Z",
            True,
        ),
        (
            "https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00",
            True,
        ),
        (
            "https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z",
            False,
        ),
        (
            "https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00",
            False,
        ),
        ("https://somewhere.com/collections/my_collection/position", False),
    ],
)
def test_datetime_is_interval(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.datetime.is_interval == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z/2018-03-12T23%3A20%3A52Z",
            isoparse("2018-02-12T23:20:52Z"),
        ),
        (
            "https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00",
            isoparse("2019-09-07T15:50-04:00"),
        ),
        (
            "https://somewhere.com/collections/my_collection/position?datetime=not_a_date/2018-03-12T23%3A20%3A52Z",
            "Datetime format not recognised",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?datetime=3422-23423-234/2018-03-12T23%3A20%3A52Z",
            "Datetime format not recognised",
        ),
    ],
)
def test_datetime_interval_from(url, expected):
    try:
        edr_query = EDRQueryParser(url)
        assert edr_query.datetime.interval_from == expected
    except ValueError as raised_exception:
        assert str(raised_exception) == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z/2018-03-12T23%3A20%3A52Z",
            isoparse("2018-03-12T23:20:52Z"),
        ),
        (
            "https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00",
            isoparse("2019-09-07T15:50-05:00"),
        ),
        (
            "https://somewhere.com/collections/my_collection/position?datetime=2018-03-12T23%3A20%3A52Z/3422-23423-234",
            "Datetime format not recognised",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?",
            "Datetime format not recognised",
        ),
    ],
)
def test_datetime_interval_to(url, expected):
    try:
        edr_query = EDRQueryParser(url)
        assert edr_query.datetime.interval_to == expected
    except ValueError as raised_exception:
        assert str(raised_exception) == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/position?bbox=1,10,20,30",
            [1, 10, 20, 30],
        ),
        (
            "https://somewhere.com/collections/my_collection/position?bbox=1,10,20,a",
            "could not convert parameter to a list",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?bbox=",
            "could not convert parameter to a list",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?",
            "could not convert parameter to a list",
        ),
    ],
)
def test_bbox(url, expected):
    try:
        edr_query = EDRQueryParser(url)
        assert edr_query.bbox.list == expected
    except ValueError as raised_exception:
        assert str(raised_exception) == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/position?within=20&within-units=km",
            20,
        ),
        (
            "https://somewhere.com/collections/my_collection/position?within=30&within-units=km",
            30,
        ),
        (
            "https://somewhere.com/collections/my_collection/position?within=&within-units=km",
            None,
        ),
        (
            "https://somewhere.com/collections/my_collection/position?&within-units=km",
            None,
        ),
    ],
)
def test_within(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.within.value == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/position?within=20&within-units=km",
            "km",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?within=30&within-units=miles",
            "miles",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?within=30&within-units=",
            None,
        ),
        (
            "https://somewhere.com/collections/my_collection/position?within=30",
            None,
        ),
    ],
)
def test_within_units(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.within_units.value == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/position?datetime=..%2F2018-02-12T23%3A20%3A52Z",
            True,
        ),
        (
            "https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z%2F..",
            False,
        ),
        (
            "https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z",
            False,
        ),
        (
            "https://somewhere.com/collections/my_collection/position?",
            False,
        ),
    ],
)
def test_datetime_is_interval_open_start(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.datetime.is_interval_open_start == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/position?datetime=..%2F2018-02-12T23%3A20%3A52Z",
            False,
        ),
        (
            "https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z%2F..",
            True,
        ),
        (
            "https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z",
            False,
        ),
        (
            "https://somewhere.com/collections/my_collection/position",
            False,
        ),
    ],
)
def test_datetime_is_interval_open_end(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.datetime.is_interval_open_end == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z%2F..",
            isoparse("2018-02-12T23:20:52Z"),
        ),
        (
            "https://somewhere.com/collections/my_collection/position?datetime=..%2F2018-02-12T23%3A20%3A52Z",
            "datetime not an interval open end type",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z",
            "datetime not an interval open end type",
        ),
        (
            "https://somewhere.com/collections/my_collection/position",
            "datetime not an interval open end type",
        ),
    ],
)
def test_datetime_interval_open_end(url, expected):
    try:
        edr_query = EDRQueryParser(url)
        assert edr_query.datetime.interval_open_end == expected
    except ValueError as raised_exception:
        assert str(raised_exception) == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/position?datetime=..%2F2018-02-12T23%3A20%3A52Z",
            isoparse("2018-02-12T23:20:52Z"),
        ),
        (
            "https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z%2F..",
            "datetime not an interval open start type",
        ),
        (
            "https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z",
            "datetime not an interval open start type",
        ),
        (
            "https://somewhere.com/collections/my_collection/position",
            "datetime not an interval open start type",
        ),
    ],
)
def test_datetime_interval_open_start(url, expected):
    try:
        edr_query = EDRQueryParser(url)
        assert edr_query.datetime.interval_open_start == expected
    except ValueError as raised_exception:
        assert str(raised_exception) == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/items?next=token123",
            "token123",
        ),
        ("https://somewhere.com/collections/my_collection/items?next=", None),
        ("https://somewhere.com/collections/my_collection/items", None),
    ],
)
def test_next(url, expected):
    edr_query = EDRQueryParser(url)

    assert edr_query.next.value == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://somewhere.com/collections/my_collection/items?limit=100", 100),
        ("https://somewhere.com/collections/my_collection/items?limit=", None),
        ("https://somewhere.com/collections/my_collection/items", None),
    ],
)
def test_limit(url, expected):
    edr_query = EDRQueryParser(url)

    assert edr_query.limit.value == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/corridor?corridor-height=20",
            20,
        ),
        (
            "https://somewhere.com/collections/my_collection/corridor?corridor-height=30",
            30,
        ),
        (
            "https://somewhere.com/collections/my_collection/corridor?corridor-height=",
            None,
        ),
        (
            "https://somewhere.com/collections/my_collection/corridor",
            None,
        ),
    ],
)
def test_corridor_height(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.corridor_height.value == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/corridor?corridor-width=20",
            20,
        ),
        (
            "https://somewhere.com/collections/my_collection/corridor?corridor-width=30",
            30,
        ),
        (
            "https://somewhere.com/collections/my_collection/corridor?corridor-width=",
            None,
        ),
        (
            "https://somewhere.com/collections/my_collection/corridor",
            None,
        ),
    ],
)
def test_corridor_width(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.corridor_width.value == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/corridor?width-units=km",
            "km",
        ),
        (
            "https://somewhere.com/collections/my_collection/corridor/?width-units=m",
            "m",
        ),
        ("https://somewhere.com/collections/my_collection/corridor", None),
        (
            "https://somewhere.com/collections/my_collection/corridor/?width-units=",
            None,
        ),
    ],
)
def test_width_units(url, expected):
    edr_query = EDRQueryParser(url)
    assert edr_query.width_units.value == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://somewhere.com/collections/my_collection/corridor?height-units=km",
            "km",
        ),
        (
            "https://somewhere.com/collections/my_collection/corridor/?height-units=m",
            "m",
        ),
        ("https://somewhere.com/collections/my_collection/corridor", None),
        (
            "https://somewhere.com/collections/my_collection/corridor/?height-units=",
            None,
        ),
    ],
)
def test_height_units(url, expected):
    edr_query = EDRQueryParser(url)

    assert edr_query.height_units.value == expected


def test_datetime_interval_to_type():
    edr_query = EDRQueryParser(
        "https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z/2018-03-12T23%3A20%3A52Z",
    )

    assert isinstance(edr_query.datetime.interval_to, datetime)


def test_datetime_interval_from_type():
    edr_query = EDRQueryParser(
        "https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z/2018-03-12T23%3A20%3A52Z",
    )

    assert isinstance(edr_query.datetime.interval_from, datetime)


def test_datetime_exact_type():
    edr_query = EDRQueryParser(
        "https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00"
    )

    assert isinstance(edr_query.datetime.exact, datetime)


def test_datetime_interval_open_start_type():
    edr_query = EDRQueryParser(
        "https://somewhere.com/collections/my_collection/position?datetime=..%2F2018-02-12T23%3A20%3A52Z"
    )

    assert isinstance(edr_query.datetime.interval_open_start, datetime)


def test_datetime_interval_open_end_type():
    edr_query = EDRQueryParser(
        "https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z%2F.."
    )

    assert isinstance(edr_query.datetime.interval_open_end, datetime)


def test_coords_wkt_type():
    edr_query = EDRQueryParser(
        "https://somewhere.com/collections/my_collection/position?coords=POINT(0 51.48)"
    )

    assert isinstance(edr_query.coords.wkt, dict)


def test_coords_coords_type_type():
    edr_query = EDRQueryParser(
        "https://somewhere.com/collections/my_collection/position?coords=POINT(0 51.48)"
    )

    assert isinstance(edr_query.coords.coords_type, str)


def test_coords_coordinates_type():
    edr_query = EDRQueryParser(
        "https://somewhere.com/collections/my_collection/position?coords=POINT(0 51.48)"
    )

    assert isinstance(edr_query.coords.coordinates, list)


def test_z_interval_from_type():
    edr_query = EDRQueryParser(
        "https://somewhere.com/collections/my_collection/position?z=12/13"
    )

    assert type(edr_query.z.interval_from) == float
