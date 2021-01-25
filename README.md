# Enviromental Data Retreval Query Parser
The OGC Enviromental Data Retreveal API query parser makes it easier to parse and use the API query.

## Example
### Initiate
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&parameter-name=parameter1,'
                           'parameter2&f=geoJSON&crs=crs86')
```

### Get the collection name
```python
edr_query.get_collection_name()
```

### Get the query type
```python
edr_query.get_query_type())
```

### Get the coords type
```python
edr_query.get_coords_type()
```

### Get the coords coordinates
```python
edr_query.get_coords_coordinates()
```

### Get the requested output format
```python
edr_query.get_format()
```

### Get the datetime
```python
if edr.is_datetime_interval():
    edr.get_datetime_from()
    edr.get_datetime_to()
else:
    edr.get_datetime()
```

### Get the get coords type
```python
edr.get_coords_type()
```

### Get the coords coorinates
```python
edr.get_coords_coordinates()
```

### Get the coords dictionary
```python
edr.get_coords_dic()
```
