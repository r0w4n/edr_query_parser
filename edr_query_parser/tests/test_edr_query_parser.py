import pytest
from edr_query_parser import EDRQueryParser
from dateutil.parser import isoparse


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/corridor?', 'my_collection'),
    ('https://somewhere.com/v1/collections/collections/position?', 'collections'),
    ('https://somewhere.com/collections/observations/position?', 'observations'),
    ('https://somewhere.com/collections', 'collection name not found in url'),
    ('https://somewhere.com/items/my_collection', 'collection name not found in url'),
])
def test_collection_name(url, expected):
    edr = EDRQueryParser(url)
    try:
        assert edr.collection_name == expected
    except ValueError as raisedException:
        assert str(raisedException) == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?', 'position'),
    ('https://somewhere.com/collections/my_collection/radius?', 'radius'),
    ('https://somewhere.com/collections/my_collection/area?', 'area'),
    ('https://somewhere.com/collections/my_collection/cube?', 'cube'),
    ('https://somewhere.com/collections/my_collection/trajectory?', 'trajectory'),
    ('https://somewhere.com/collections/my_collection/corridor?', 'corridor'),
    ('https://somewhere.com/collections/my_collection/items?', 'items'),
    ('https://somewhere.com/collections/my_collection/locations?', 'locations'),
    ('https://somewhere.com/collections/metar/locations/EGLL?', 'locations'),
    ('https://somewhere.com/collections/metar/items/KIAD_2020-05-19T00Z?', 'items'),
    ('https://somewhere.com/collections/metar/items/KIAD_2020-05-19T00Z/?', 'items'),
    ('https://somewhere.com/collections/my_collection/not_a_query_type?', 'unsupported query type found in url'),
    ('https://somewhere.com/collections/metar/instances/some_instance/radius?', 'radius'),
])
def test_query_type(url, expected):
    edr = EDRQueryParser(url)
    try:
        assert edr.query_type.value == expected
    except ValueError as raisedException:
        assert str(raisedException) == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?', True),
    ('https://somewhere.com/collections/my_collection/radius?', False),
    ('https://somewhere.com/collections/my_collection/area?', False),
    ('https://somewhere.com/collections/my_collection/cube?', False),
    ('https://somewhere.com/collections/my_collection/trajectory?', False),
    ('https://somewhere.com/collections/my_collection/corridor?', False),
    ('https://somewhere.com/collections/my_collection/items?', False),
    ('https://somewhere.com/collections/my_collection/locations?', False),
    ('https://somewhere.com/collections/metar/locations/EGLL?', False),
    ('https://somewhere.com/collections/metar/items/KIAD_2020-05-19T00Z?', False),
    ('https://somewhere.com/collections/metar/items/KIAD_2020-05-19T00Z/?', False),
    ('https://somewhere.com/collections/metar/instances/some_instance/radius?', False),
    ('https://somewhere.com/collections/metar/instances/some_instance/position?', True),
])
def test_query_type_is_position(url, expected):
    edr = EDRQueryParser(url)
    assert edr.query_type.is_position == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?', False),
    ('https://somewhere.com/collections/my_collection/radius?', True),
])
def test_query_type_is_radius(url, expected):
    edr = EDRQueryParser(url)
    assert edr.query_type.is_radius == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/area?', True),
    ('https://somewhere.com/collections/my_collection/radius?', False),
])
def test_query_type_is_area(url, expected):
    edr = EDRQueryParser(url)
    assert edr.query_type.is_area == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?', False),
    ('https://somewhere.com/collections/my_collection/cube?', True),
])
def test_query_type_is_cube(url, expected):
    edr = EDRQueryParser(url)
    assert edr.query_type.is_cube == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?', False),
    ('https://somewhere.com/collections/my_collection/trajectory?', True),
])
def test_query_type_is_trajectory(url, expected):
    edr = EDRQueryParser(url)
    assert edr.query_type.is_trajectory == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?', False),
    ('https://somewhere.com/collections/my_collection/corridor?', True),
])
def test_query_type_is_corridor(url, expected):
    edr = EDRQueryParser(url)
    assert edr.query_type.is_corridor == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?', False),
    ('https://somewhere.com/collections/my_collection/items?', True),
])
def test_query_type_is_items(url, expected):
    edr = EDRQueryParser(url)
    assert edr.query_type.is_items == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?', False),
    ('https://somewhere.com/collections/my_collection/locations?', True),
])
def test_query_type_is_locations(url, expected):
    edr = EDRQueryParser(url)
    assert edr.query_type.is_locations == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/metar/instances/some_instance/radius?', True),
    ('https://somewhere.com/collections/metar/locations/EGLL?', False),
])
def test_is_instances(url, expected):
    edr = EDRQueryParser(url)
    assert edr.is_instances == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?parameter-name=parameter1,parameter2',
     ['parameter1', 'parameter2']),
    ('https://somewhere.com/collections/my_collection/position?parameter-name=parameter1', ['parameter1']),
    ('https://somewhere.com/collections/my_collection/position?parameter-name=parameter1,%20parameter2, parameter3',
     ['parameter1', 'parameter2', 'parameter3']),
    ('https://somewhere.com/collections/my_collection/position', 'could not convert parameter to a list'),
    ('https://somewhere.com/collections/my_collection/position?parameter-name=&something=1',
     'could not convert parameter to a list'),
    ('https://somewhere.com/collections/my_collection/locations/my_locations?parameter-name=parameter1',
     ['parameter1']),
])
def test_parameter_name(url, expected):
    edr = EDRQueryParser(url)
    try:
        assert edr.parameter_name.list == expected
    except ValueError as raisedException:
        assert str(raisedException) == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/items/my_item_id/', 'my_item_id'),
    ('https://somewhere.com/collections/my_collection/items/', None),
    ('https://somewhere.com/collections/my_collection/items', None),
    ('https://somewhere.com/collections/my_collection/items/my_item?parameter-name=&something=1', 'my_item'),
])
def test_items_id(url, expected):
    edr = EDRQueryParser(url)
    assert edr.items_id == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/locations/my_location/', 'my_location'),
    ('https://somewhere.com/collections/my_collection/locations/', None),
    ('https://somewhere.com/collections/my_collection/locations', None),
    ('https://somewhere.com/collections/my_collection/locations/my_location?parameter-name=&something=1',
     'my_location'),
])
def test_locations_id(url, expected):
    edr = EDRQueryParser(url)
    assert edr.locations_id == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/instances/my_instance/', 'my_instance'),
    ('https://somewhere.com/collections/my_collection/instances/', None),
    ('https://somewhere.com/collections/my_collection/instances', None),
    ('https://somewhere.com/collections/my_collection/instances/my_instance?parameter-name=&something=1',
     'my_instance'),
])
def test_instances_id(url, expected):
    edr = EDRQueryParser(url)
    assert edr.instances_id == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?f=geoJson', 'geoJson'),
    ('https://somewhere.com/collections/my_collection/instances/?f=CoverageJSON', 'CoverageJSON'),
    ('https://somewhere.com/collections/my_collection/instances', None),
    ('https://somewhere.com/collections/my_collection/instances?f=', None),
])
def test_format_value(url, expected):
    edr = EDRQueryParser(url)
    assert edr.format.value == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?crs=WGS84', 'WGS84'),
    ('https://somewhere.com/collections/my_collection/instances', None),
    ('https://somewhere.com/collections/my_collection/instances?crs=', None),
])
def test_crs_value(url, expected):
    edr = EDRQueryParser(url)
    assert edr.crs.value == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?coords=POINT(0 51.48)',
     {'type': 'Point', 'coordinates': [0.0, 51.48]}),
    (
            'https://somewhere.com/collections/my_collection/position?coords=MULTIPOINT((38.9 -77),(48.85 2.35),(39.92 116.38),(-35.29 149.1),(51.5 -0.1))',
            {'type': 'MultiPoint',
             'coordinates': [[38.9, -77.0], [48.85, 2.35], [39.92, 116.38], [-35.29, 149.1], [51.5, -0.1]]})
])
def test_coords_wkt(url, expected):
    edr = EDRQueryParser(url)
    assert edr.coords.wkt == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?z=12', 12),
    ('https://somewhere.com/collections/my_collection/position?z=All', 'z can not be cast to float'),
    ('https://somewhere.com/collections/my_collection/position?z=12.5', 12.5),
    ('https://somewhere.com/collections/my_collection/position?z=500,400', 'z can not be cast to float'),
    ('https://somewhere.com/collections/my_collection/position?z=All', 'z can not be cast to float'),
    ('https://somewhere.com/collections/my_collection/position?z=all', 'z can not be cast to float'),
    ('https://somewhere.com/collections/my_collection/position?z=ALL', 'z can not be cast to float'),
    ('https://somewhere.com/collections/my_collection/position?z=12,23,34', 'z can not be cast to float'),
    ('https://somewhere.com/collections/my_collection/position?z=', 'z can not be cast to float'),
    ('https://somewhere.com/collections/my_collection/position', 'z can not be cast to float'),
])
def test_z_float(url, expected):
    edr = EDRQueryParser(url)
    try:
        assert edr.z.float == expected
    except ValueError as raisedException:
        assert str(raisedException) == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?z=12/13', 12),
    ('https://somewhere.com/collections/my_collection/position?z=500,400', 'unable to get z from value'),
    ('https://somewhere.com/collections/my_collection/position?z=All', 'unable to get z from value'),
    ('https://somewhere.com/collections/my_collection/position?z=12,23,34', 'unable to get z from value'),
    ('https://somewhere.com/collections/my_collection/position?z=', 'unable to get z from value'),
    ('https://somewhere.com/collections/my_collection/position', 'unable to get z from value'),
])
def test_z_interval_from(url, expected):
    edr = EDRQueryParser(url)
    try:
        assert edr.z.interval_from == expected
    except ValueError as raisedException:
        assert str(raisedException) == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?z=12/13', 13),
    ('https://somewhere.com/collections/my_collection/position?z=500,400', 'unable to get z to value'),
    ('https://somewhere.com/collections/my_collection/position?z=All', 'unable to get z to value'),
    ('https://somewhere.com/collections/my_collection/position?z=12,23,34', 'unable to get z to value'),
    ('https://somewhere.com/collections/my_collection/position?z=', 'unable to get z to value'),
    ('https://somewhere.com/collections/my_collection/position', 'unable to get z to value'),
])
def test_z_interval_to(url, expected):
    edr = EDRQueryParser(url)

    try:
        assert edr.z.interval_to == expected
    except ValueError as raisedException:
        assert str(raisedException) == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?z=12', False),
    ('https://somewhere.com/collections/my_collection/position?z=all', True),
    ('https://somewhere.com/collections/my_collection/position?z=All', True),
    ('https://somewhere.com/collections/my_collection/position?z=ALL', True),
    ('https://somewhere.com/collections/my_collection/position?z=12,23,34', False),
    ('https://somewhere.com/collections/my_collection/position?z=', False),
    ('https://somewhere.com/collections/my_collection/position', False),
])
def test_z_is_all(url, expected):
    edr = EDRQueryParser(url)
    assert edr.z.is_all == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?z=12/13', False),
    ('https://somewhere.com/collections/my_collection/position?z=500,400', True),
    ('https://somewhere.com/collections/my_collection/position?z=All', False),
    ('https://somewhere.com/collections/my_collection/position?z=12,23,34', True),
    ('https://somewhere.com/collections/my_collection/position?z=', False),
    ('https://somewhere.com/collections/my_collection/position', False),
])
def test_z_is_list(url, expected):
    edr = EDRQueryParser(url)
    assert edr.z.is_list == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?z=500,400', [500, 400]),
    ('https://somewhere.com/collections/my_collection/position?z=12,23,34', [12, 23, 34]),
    ('https://somewhere.com/collections/my_collection/position?z=23/45', 'could not convert parameter to a list'),
    ('https://somewhere.com/collections/my_collection/position?z=', 'could not convert parameter to a list'),
    ('https://somewhere.com/collections/my_collection/position', 'could not convert parameter to a list'),
])
def test_z_list(url, expected):
    edr = EDRQueryParser(url)

    try:
        assert edr.z.list == expected
    except ValueError as raisedException:
        assert str(raisedException) == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?z=12/13', True),
    ('https://somewhere.com/collections/my_collection/position?z=500/400', True),
    ('https://somewhere.com/collections/my_collection/position?z=All', False),
    ('https://somewhere.com/collections/my_collection/position?z=12,23,34', False),
    ('https://somewhere.com/collections/my_collection/position?z=', False),
    ('https://somewhere.com/collections/my_collection/position', False),
])
def test_z_is_interval(url, expected):
    edr = EDRQueryParser(url)
    assert edr.z.is_interval == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?coords=POINT(0 51.48)', [0.0, 51.48]),
    (
            'https://somewhere.com/collections/my_collection/position?coords=MULTIPOINT((38.9 -77),(48.85 2.35),(39.92 116.38),(-35.29 149.1),(51.5 -0.1))',
            [[38.9, -77.0], [48.85, 2.35], [39.92, 116.38], [-35.29, 149.1], [51.5, -0.1]]),
])
def test_coords_coordinates(url, expected):
    edr = EDRQueryParser(url)
    assert edr.coords.coordinates == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?coords=POINT(0 51.48)', 'Point'),
    (
            'https://somewhere.com/collections/my_collection/position?coords=MULTIPOINT((38.9 -77),(48.85 2.35),(39.92 116.38),(-35.29 149.1),(51.5 -0.1))',
            'MultiPoint'),
])
def test_coords_coords_type(url, expected):
    edr = EDRQueryParser(url)
    assert edr.coords.coords_type == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z',
     isoparse('2018-02-12T23:20:52Z')),
    ('https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00',
     isoparse('2019-09-07T15:50-04:00')),
    ('https://somewhere.com/collections/my_collection/position?datetime=not_a_date', 'Datetime format not recognised'),
    ('https://somewhere.com/collections/my_collection/position?datetime=23/5/1920', 'Datetime format not recognised'),
])
def test_datetime_exact(url, expected):
    edr = EDRQueryParser(url)

    try:
        assert edr.datetime.exact == expected
    except ValueError as raisedException:
        assert str(raisedException) == expected


@pytest.mark.parametrize("url, expected", [
    (
            'https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z/2018-03-12T23%3A20%3A52Z',
            True),
    ('https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00',
     True),
    ('https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z', False),
    ('https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00', False),
    ('https://somewhere.com/collections/my_collection/position', False),
])
def test_datetime_is_interval(url, expected):
    edr = EDRQueryParser(url)
    assert edr.datetime.is_interval == expected


@pytest.mark.parametrize("url, expected", [
    (
            'https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z/2018-03-12T23%3A20%3A52Z',
            isoparse('2018-02-12T23:20:52Z')),
    ('https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00',
     isoparse('2019-09-07T15:50-04:00')),
    ('https://somewhere.com/collections/my_collection/position?datetime=not_a_date/2018-03-12T23%3A20%3A52Z',
     'Datetime format not recognised'),
    ('https://somewhere.com/collections/my_collection/position?datetime=3422-23423-234/2018-03-12T23%3A20%3A52Z',
     'Datetime format not recognised'),
])
def test_datetime_interval_from(url, expected):
    edr = EDRQueryParser(url)

    try:
        assert edr.datetime.interval_from == expected
    except ValueError as raisedException:
        assert str(raisedException) == expected


@pytest.mark.parametrize("url, expected", [
    (
            'https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z/2018-03-12T23%3A20%3A52Z',
            isoparse('2018-03-12T23:20:52Z')),
    ('https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00',
     isoparse('2019-09-07T15:50-05:00')),
    ('https://somewhere.com/collections/my_collection/position?datetime=2018-03-12T23%3A20%3A52Z/3422-23423-234',
     'Datetime format not recognised'),
])
def test_datetime_interval_to(url, expected):
    edr = EDRQueryParser(url)

    try:
        assert edr.datetime.interval_to == expected
    except ValueError as raisedException:
        assert str(raisedException) == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?bbox=1,10,20,30', [1, 10, 20, 30]),
    (
            'https://somewhere.com/collections/my_collection/position?bbox=1,10,20,a',
            'could not convert parameter to a list'),
])
def test_bbox(url, expected):
    edr = EDRQueryParser(url)

    try:
        assert edr.bbox.list == expected
    except ValueError as raisedException:
        assert str(raisedException) == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?within=20&within-units=km', 20),
    (
            'https://somewhere.com/collections/my_collection/position?within=30&within-units=km', 30),
])
def test_within(url, expected):
    edr = EDRQueryParser(url)
    assert edr.within.value == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?within=20&within-units=km', "km"),
    (
            'https://somewhere.com/collections/my_collection/position?within=30&within-units=miles', "miles"),
])
def test_within_units(url, expected):
    edr = EDRQueryParser(url)
    assert edr.within_units.value == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?datetime=..%2F2018-02-12T23%3A20%3A52Z',
     True),
    ('https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z%2F..',
     False),
    ('https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z',
     False),
])
def test_datetime_is_less_than(url, expected):
    edr = EDRQueryParser(url)
    assert edr.datetime.is_less_than == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?datetime=..%2F2018-02-12T23%3A20%3A52Z',
     False),
    ('https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z%2F..',
     True),
    ('https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z',
     False)
])
def test_datetime_is_greater_than(url, expected):
    edr = EDRQueryParser(url)
    assert edr.datetime.is_greater_than == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z%2F..',
     isoparse('2018-02-12T23:20:52Z')),
    ('https://somewhere.com/collections/my_collection/position?datetime=..%2F2018-02-12T23%3A20%3A52Z',
     'datetime not a greater than type'),
    ('https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z',
     'datetime not a greater than type'),
])
def test_datetime_greater_than(url, expected):
    edr = EDRQueryParser(url)

    try:
        assert edr.datetime.greater_than == expected
    except ValueError as raisedException:
        assert str(raisedException) == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/position?datetime=..%2F2018-02-12T23%3A20%3A52Z',
     isoparse('2018-02-12T23:20:52Z')),
    ('https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z%2F..',
     'datetime not a less than type'),
    ('https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z',
     'datetime not a less than type'),
])
def test_datetime_less_than(url, expected):
    edr = EDRQueryParser(url)

    try:
        assert edr.datetime.less_than == expected
    except ValueError as raisedException:
        assert str(raisedException) == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/items?next=token123', 'token123'),
    ('https://somewhere.com/collections/my_collection/items?next=', None),
    ('https://somewhere.com/collections/my_collection/items', None)
])
def test_next(url, expected):
    edr = EDRQueryParser(url)

    assert edr.next.value == expected


@pytest.mark.parametrize("url, expected", [
    ('https://somewhere.com/collections/my_collection/items?limit=100', 100),
    ('https://somewhere.com/collections/my_collection/items?limit=', None),
    ('https://somewhere.com/collections/my_collection/items', None)
])
def test_limit(url, expected):
    edr = EDRQueryParser(url)

    assert edr.limit.value == expected

