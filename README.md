# OGC Environmental Data Retrieval Query Parser
The [OGC API Environmental Data Retrieval](https://github.com/opengeospatial/ogcapi-environmental-data-retrieval) query parser makes it easy to parse and use the API query.

[![PyPI](https://img.shields.io/pypi/v/edr-query-parser)](https://pypi.org/project/edr-query-parser/)
![PyPI - License](https://img.shields.io/pypi/l/edr-query-parser)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/edr-query-parser)
[![Sonar Quality Gate](https://img.shields.io/sonar/quality_gate/r0w4n_edr_query_parser?server=https%3A%2F%2Fsonarcloud.io)](https://sonarcloud.io/summary/new_code?id=r0w4n_edr_query_parser)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Codecov](https://img.shields.io/codecov/c/github/r0w4n/edr_query_parser)](https://app.codecov.io/gh/r0w4n/edr_query_parser)

# Install
```shell
pip install edr-query-parser
```

# Usage

## Collection Name Example
```python
from edr_query_parser import EDRQueryParser
edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?parameter-name=param1,param2&coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&f=geoJSON&crs=84&z=500/400')

print(edr_query.collection_name) #my_collection
```

## Query Type Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?parameter-name=param1,param2&coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&f=geoJSON&crs=84&z=500/400')

if edr_query.is_instances:
    print(edr_query.instances_id)
else:
    print(edr_query.query_type.is_position) # True
    print(edr_query.query_type.is_radius) # False
    print(edr_query.query_type.is_locations) # False
    print(edr_query.query_type.is_corridor) # False
    print(edr_query.query_type.is_area) # False
    print(edr_query.query_type.is_trajectory) # False
    print(edr_query.query_type.is_cube) # False
    print(edr_query.query_type.is_items) # False
    print(edr_query.query_type.value) # position
```

## location ID Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/locations/aberdeen?parameter-name='
                            'param1,param2&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&f=geoJSON&crs=84&z=500/400')

if edr_query.query_type.is_locations:
    print(edr_query.locations_id) #aberdeen

```

## coords Example
The EDR query parser returns a [WKT](https://github.com/geomet/geomet) object
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&parameter-name=parameter1,'
                           'parameter2&f=geoJSON&crs=84&z=all')

if edr_query.coords.is_set:
    print(edr_query.coords.coords_type) # Point
    if edr_query.coords.coords_type == 'Point':
        print(edr_query.coords.coordinates[0]) # 57.819
        print(edr_query.coords.coordinates[1]) # -3.966
        
```

## parameter-name Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&parameter-name=parameter1,'
                           'parameter2&f=geoJSON&crs=84&z=all')
if edr_query.parameter_name.is_set:
    print(edr_query.parameter_name.list) # [parameter1, parameter2]
```

## datetime Example
The EDR query parser returns a [dateutil](http://labix.org/python-dateutil) object

```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&parameter-name=parameter1,'
                           'parameter2&f=geoJSON&crs=84&z=all')

if edr_query.datetime.is_set:
    if edr_query.datetime.is_interval:
        print(edr_query.datetime.interval_from.timestamp(), edr_query.datetime.interval_to.timestamp())
    elif edr_query.datetime.is_interval_open_end:
        print(edr_query.datetime.interval_open_end.timestamp())
    elif edr_query.datetime.is_interval_open_start:
        print(edr_query.datetime.interval_open_start.timestamp())
    else:
        print(edr_query.datetime.exact.timestamp())

```
## f Parameter Example

```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?parameter-name=param1,param2&coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&f=geoJSON&crs=84&z=500/400')

print(edr_query.format.value) # geoJSON
```

## z Parameter Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&parameter-name=parameter1,'
                           'parameter2&f=geoJSON&crs=84&z=12/240')

if edr_query.z.is_set:
    if edr_query.z.is_interval:
        print(edr_query.z.interval_from, edr_query.z.interval_to)
    if edr_query.z.is_list:
        print(edr_query.z.interval_from, edr_query.z.list)

```

## crs Parameter Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&parameter-name=parameter1,'
                           'parameter2&f=geoJSON&crs=84&z=12/240')

print(edr_query.crs.value) # 84
```

## bbox Parameter Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/items/some_item/?bbox=12,13,20,21')

print(edr_query.bbox.list) # [12.0, 13.0, 20.0, 21.0]
```

## Pagination limit Parameter Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/items?limit=100')

print(edr_query.limit.value) # 100
```

## Pagination next Parameter Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/items?next=token123')

print(edr_query.next.value) # "token123"
```

## corridor-height Parameter Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/corridor?corridor-height=12&corridor-width=5')

print(edr_query.corridor_height.value) # "12"
```

## corridor-width Parameter Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/corridor?corridor-height=12&corridor-width=5')

print(edr_query.corridor_width.value) # "5"
```

## width-units Parameter Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/corridor?width-units=km')

print(edr_query.width_units.value) # "km"
```

## height-units Parameter Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/corridor?height-units=km')

print(edr_query.height_units.value) # "km"
```

## within Parameter Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/radius?within=10&within-units=km')

print(edr_query.within.value) # "10"
```

## within-units Parameter Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/radius?within=10&within-units=km')

print(edr_query.within_units.value) # "km"
```