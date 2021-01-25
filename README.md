# Environmental Data Retrieval Query Parser
The OGC Environmental Data Retrieval API query parser makes it easier to parse and use the API query.

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

returns string of the requested collection

### Get the query type
```python
edr_query.get_query_type())
```

returns string of the query type

### Get the requested output format
```python
edr_query.get_format()
```

returns string of the requested output format

### Get the paramter names
```python
edr_query.get_parameter_name()
```

returns list of requested parameters

### Get the datetime
```python
if edr.is_datetime_interval():
    edr.get_datetime_from()
    edr.get_datetime_to()
else:
    edr.get_datetime()
```

returns datetime object of the requested datetime

### Get the get coords type
```python
edr.get_coords_type()
```
return the well know text coords type

### Get the coords coorinates
```python
edr.get_coords_coordinates()
```

return the well know text coordinates request

### Get the coords dictionary
```python
edr.get_coords_dic()
```

returns dictionary of the well known text query request


### Get the CRS
```python
edr.get_crs()
```

return string for the requested CRS
