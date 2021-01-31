# Environmental Data Retrieval Query Parser
The [OGC API Environmental Data Retrieval](https://github.com/opengeospatial/ogcapi-environmental-data-retrieval) query parser makes it easy to parse and use the API query.

![Python package](https://github.com/r0w4n/edr_query_parser/workflows/Python%20package/badge.svg?branch=main)
![Upload Python Package](https://github.com/r0w4n/edr_query_parser/workflows/Upload%20Python%20Package/badge.svg)

# install
```shell
pip install edr-query-parser
```

# Usage
## Initiate
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&parameter-name=parameter1,'
                           'parameter2&f=geoJSON&crs=crs86&z=all')
```

## Get the collection name

```python
edr_query.collection_name
```

returns string of the requested collection

## Get the query type

```python
edr_query.query_type
```

returns string of the query type

## Get the requested output format

```python
edr_query.format
```

returns string of the requested output format

## Get the parameter names

```python
if edr_query.parameter_name is not None:
    print('SELECT ' + ",".join(edr_query.parameter_name) + ' from observations')
else:
    print('SELECT * from observations')
```

returns list of requested parameters

## Get the datetime

```python
if edr.is_datetime_interval:
    edr.datetime_from
    edr.datetime_to
else:
    edr.datetime.timestamp()  # e.g. gets the timestamp of the datetime
```

returns datetime object of the requested datetime

## Get the get coords type

```python
edr.coords_type
```
returns the well-know text coords type

## Get the coords coordinates

```python
edr.coords_coordinates
```

returns the well know text coordinates request

## Get the coords dictionary

```python
edr.coords
```

returns dictionary of the well known text query request


## Get the CRS

```python
edr.crs
```

returns string for the requested CRS

## Get instances id

```python
edr.instances_id
```

returns string of the instances id

## Get items id

```python
edr.items_id
```

returns string of the items id

## Get locations id

```python
edr.locations_id
```

returns string of the locations id

## Get z height

```python
edr.z
```

returns float of the height