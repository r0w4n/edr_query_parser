# Enviromental Data Retreval Query Parser
The OGC Enviromental Data Retreveal API query parser makes it easier to parse and use the API query.

## Example
### Intiate
```python
from edr_query_parser import EDRQueryParser

edr_query = EDRQueryParser('https://somewhere.com/collections/my_collection/position?coords=POINT(57.819 '
                           '-3.966)&datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00&parameter-name=parameter1,'
                           'parameter2&f=geoJSON&crs=crs86')
```

### Get the collection name
```python
print(edr_query.get_collection_name())
```

### Get the query type
```python
print(edr_query.get_query_type())
```

### Get the coords type
```python
print(edr_query.get_coords_type())
```

### Get the coords coordinates
```python
print(edr_query.get_coords_coordinates())
```

### Get the requested output format
```python
print(edr_query.get_format())
```
