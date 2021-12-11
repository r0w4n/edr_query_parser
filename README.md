# OGC Environmental Data Retrieval Query Parser
The [OGC API Environmental Data Retrieval](https://github.com/opengeospatial/ogcapi-environmental-data-retrieval) query parser makes it easy to parse and use the API query.

![PyPI](https://img.shields.io/pypi/v/edr-query-parser)
![PyPI - License](https://img.shields.io/pypi/l/edr-query-parser)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/edr-query-parser)
![Sonar Quality Gate](https://img.shields.io/sonar/quality_gate/r0w4n_edr_query_parser?server=https%3A%2F%2Fsonarcloud.io)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fr0w4n%2Fedr_query_parser.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fr0w4n%2Fedr_query_parser?ref=badge_shield)

# Install
```shell
pip install edr-query-parser
```

# Usage

## EDR Collection Name Example
```python
from edr_query_parser import EDRQueryParser
edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?parameter-name=param1,param2&coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&f=geoJSON&crs=84&z=500/400')

print(edr_query.collection_name) #my_collection
```

## EDR Query Type Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?parameter-name=param1,param2&coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&f=geoJSON&crs=84&z=500/400')

if edr_query.is_instances:
    print(edr_query.instances_id)
else:
    print(edr_query.query_type.is_position) # True
    print(edr_query.query_type.is_radius) # False
    print(edr_query.query_type.value) # position
```

## EDR location ID Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/locations/aberdeen?parameter-name='
                            'param1,param2&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&f=geoJSON&crs=84&z=500/400')

if edr_query.is_locations:
    print(edr_query.locations_id) #aberdeen

```

## EDR coords Example
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

## EDR parameter-name Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&parameter-name=parameter1,'
                           'parameter2&f=geoJSON&crs=84&z=all')
if edr_query.parameter_name.is_set:
    print(edr_query.parameter_name.list) # [parameter1, parameter2]
```

## EDR datetime Example
The EDR query parser returns a [dateutil](http://labix.org/python-dateutil) object
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&parameter-name=parameter1,'
                           'parameter2&f=geoJSON&crs=84&z=all')

if edr_query.datetime.is_set:
    if edr_query.datetime.is_interval:
        print(edr_query.datetime.interval_from.timestamp(), edr_query.datetime.interval_to.timestamp())
    elif edr_query.datetime.is_greater_than:
        print(edr_query.datetime.interval_to.timestamp())
    elif edr_query.datetime.is_less_than:
        print(edr_query.datetime.interval_from.timestamp())
    else:
        print(edr_query.datetime.exact.timestamp())

```
## EDR f Parameter Example

```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?parameter-name=param1,param2&coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&f=geoJSON&crs=84&z=500/400')

print(edr_query.format.value) # geoJSON
```

## EDR z Parameter Example
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

## EDR crs Parameter Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&parameter-name=parameter1,'
                           'parameter2&f=geoJSON&crs=84&z=12/240')

print(edr_query.crs.value) # 84
```

## EDR bbox Parameter Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/items/some_item/?bbox=12,13,20,21')

print(edr_query.bbox.list) # [12.0, 13.0, 20.0, 21.0]
```

## EDR Pagination Limit Parameter Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/items?limit=100')

print(edr_query.limit.value) # 100
```

## EDR Pagination Next Parameter Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/items?next=token123')

print(edr_query.next.value) # "token123"
```

## EDR  Parameter Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/items?next=token123')

print(edr_query.next.value) # "token123"
```


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fr0w4n%2Fedr_query_parser.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fr0w4n%2Fedr_query_parser?ref=badge_large)