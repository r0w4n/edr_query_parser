# Environmental Data Retrieval Query Parser
The [OGC API Environmental Data Retrieval](https://github.com/opengeospatial/ogcapi-environmental-data-retrieval) query parser makes it easy to parse and use the API query.

![Python package and update to PyPi](https://github.com/r0w4n/edr_query_parser/workflows/Python%20package%20and%20update%20to%20PyPi/badge.svg)

# install
```shell
pip install edr-query-parser
```

# Usage

## EDR Collection Name Example
```python
from edr_query_parser import EDRQueryParser
edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?parameter-name=param1,param2&coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&f=geoJSON&crs=84&z=500/400')

select = 'SELECT * FROM ' + edr_query.collection_name

print(select) # SELECT * FROM my_collection
```

## EDR Query Type Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?parameter-name=param1,param2&coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&f=geoJSON&crs=84&z=500/400')

if edr_query.is_instances:
    print(edr_query.instances_id)
else:
    print(edr_query.query_type) # position
```

## EDR coords Example
The EDR query parser returns a [WKT](https://github.com/geomet/geomet) object
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&parameter-name=parameter1,'
                           'parameter2&f=geoJSON&crs=84&z=all')

select = 'SELECT * FROM observations'

if edr_query.coords.is_set:
    if edr_query.coords.coords_type == 'Point':
        select += ' WHERE NEAREST_NEIGHBOUR(' + str(edr_query.coords.coordinates[0]) + ',' + str(edr_query.coords.coordinates[0]) + ')'

print(select) # SELECT * FROM observations WHERE NEAREST_NEIGHBOUR(57.819,-3.966)
```

## EDR parameter-name Example
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&parameter-name=parameter1,'
                           'parameter2&f=geoJSON&crs=84&z=all')
select = 'SELECT '
if edr_query.parameter_name.is_set:
    select += ','.join(edr_query.parameter_name.list)
else:
    select += '*'
    
select += ' FROM observations'

print(select) # SELECT parameter1, parameter2 FROM observations'
```

## EDR datetime Example
The EDR query parser returns a [dateutil](http://labix.org/python-dateutil) object
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&parameter-name=parameter1,'
                           'parameter2&f=geoJSON&crs=84&z=all')

select = 'SELECT * FROM observations'

if edr_query.datetime.is_set:
    if edr_query.datetime.is_interval:
        select += ' date BETWEEN ' + str(edr_query.datetime.interval_from.timestamp()) + ' AND ' + str(edr_query.datetime.interval_to.timestamp())
    elif edr_query.datetime.is_greater_than:
        select += ' date >= ' + str(edr_query.datetime.interval_from.timestamp()) + ' AND ' + str(edr_query.datetime.interval_to.timestamp())
    elif edr_query.datetime.is_less_than:
        select += ' date <= ' + str(edr_query.datetime.interval_from.timestamp()) + ' AND ' + str(edr_query.datetime.interval_to.timestamp())
    else:
        select += ' date = ' + str(edr_query.datetime.exact.timestamp()) + ')'

print(select) # SELECT * FROM observations date BETWEEN 1567885800.0 AND 1567889400.0
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

select = 'SELECT * FROM observations'

if edr_query.z.is_set:
    if edr_query.z.is_interval:
        select += ' height BETWEEN ' + str(edr_query.z.interval_from) + ' AND ' + str(edr_query.z.interval_to)
    if edr_query.z.is_list:
        select += ' height IN (' + ','.join(map(str, edr_query.z.list)) + ')'

print(select) # SELECT * FROM observations height BETWEEN 12.0 AND 240.0
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

## EDR Pagination Limit Parameter Examples
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/items?limit=100')

print(edr_query.limit.value) # 100
```

## EDR Pagination Next Parameter Examples
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/items?next=token123')

print(edr_query.next.value) # "token123"
```