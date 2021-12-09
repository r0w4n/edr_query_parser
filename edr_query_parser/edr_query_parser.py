from urllib.parse import urlsplit, parse_qs
from dateutil.parser import isoparse
from enum import Enum
from geomet import wkt


def format_date(date):
    try:
        return isoparse(date)
    except ValueError:
        raise ValueError('Datetime format not recognised')


class EDRQueryParser:
    def __init__(self, url):
        self.url_parts = list(filter(None, urlsplit(url).path.split('/')))
        self.query_parts = {str(key): ''.join(value) for key, value in parse_qs(urlsplit(url).query).items()}

    def _get_id(self, query_id):
        try:
            return self.url_parts[self.url_parts.index(query_id) + 1]
        except IndexError:
            return None

    @property
    def collection_name(self):
        try:
            return self.url_parts[self.url_parts.index('collections') + 1]
        except (ValueError, IndexError):
            raise ValueError('collection name not found in url')

    @property
    def query_type(self):
        return QueryTypes(self.is_instances, self.url_parts)

    @property
    def is_instances(self):
        return self.url_parts[self.url_parts.index('collections') + 2] == 'instances'

    @property
    def items_id(self):
        return self._get_id('items')

    @property
    def locations_id(self):
        return self._get_id('locations')

    @property
    def instances_id(self):
        return self._get_id('instances')

    @property
    def format(self):
        return Parameter(self.query_parts.get('f'))

    @property
    def coords(self):
        return Coords(self.query_parts.get('coords'))

    @property
    def crs(self):
        return Parameter(self.query_parts.get('crs'))

    @property
    def parameter_name(self):
        return ParameterWithList(self.query_parts.get('parameter-name'))

    @property
    def datetime(self):
        return DateTime(self.query_parts.get('datetime'))

    @property
    def z(self):
        return Z(self.query_parts.get('z'))

    @property
    def bbox(self):
        return ParameterWithFloatList(self.query_parts.get('bbox'))

    @property
    def within(self):
        return ParameterFloat(self.query_parts.get('within'))

    @property
    def within_units(self):
        return Parameter(self.query_parts.get('within-units'))

    @property
    def next(self):
        return Parameter(self.query_parts.get('next'))

    @property
    def limit(self):
        return ParameterInt(self.query_parts.get('limit'))


class Parameter:
    def __init__(self, value):
        self.value = value

    @property
    def is_set(self):
        return self.value is not None


class ParameterInt(Parameter):
    def __init__(self, value):
        super().__init__(value)
        self.value = int(value) if value else None


class ParameterFloat(Parameter):
    def __init__(self, value):
        super().__init__(value)
        self.value = float(value)


class ParameterWithList(Parameter):
    @property
    def list(self):
        try:
            return [parameter.strip(' ') for parameter in self.value.split(',')]
        except (ValueError, AttributeError):
            raise ValueError('could not convert parameter to a list')

    @property
    def is_list(self):
        return self.is_set and ',' in self.value


class ParameterWithFloatList(ParameterWithList):
    @property
    def list(self):
        try:
            return list(map(float, super().list))
        except ValueError:
            raise ValueError('could not convert parameter to a list')


class ParameterWithInterval(Parameter):
    def _split(self, index=None):
        if self.is_set and '/' in self.value:
            return self.value.split('/')[index]
        return None

    @property
    def is_interval(self):
        return self.value is not None and '/' in self.value

    @property
    def interval_from(self):
        return self._split(0)

    @property
    def interval_to(self):
        return self._split(1)


class DateTime(ParameterWithInterval):
    @property
    def interval_from(self):
        return format_date(super().interval_from)

    @property
    def interval_to(self):
        return format_date(super().interval_to)

    @property
    def exact(self):
        return format_date(self.value)

    @property
    def is_greater_than(self):
        return self.value.endswith('/..')

    @property
    def is_less_than(self):
        return self.value.startswith('../')

    @property
    def greater_than(self):
        if self.is_greater_than:
            return format_date(self.value.replace('/..', ''))
        raise ValueError('datetime not a greater than type')

    @property
    def less_than(self):
        if self.is_less_than:
            return format_date(self.value.replace('../', ''))
        raise ValueError('datetime not a less than type')


class Z(ParameterWithFloatList, ParameterWithInterval):
    @property
    def float(self):
        try:
            return float(self.value)
        except (TypeError, ValueError):
            raise ValueError('z can not be cast to float')

    @property
    def interval_from(self):
        try:
            return float(super().interval_from)
        except TypeError:
            raise ValueError('unable to get z from value')

    @property
    def interval_to(self):
        try:
            return float(super().interval_to)
        except TypeError:
            raise ValueError('unable to get z to value')

    @property
    def is_all(self):
        return self.is_set and self.value.lower() == 'all'


class Coords(Parameter):
    @property
    def wkt(self):
        return wkt.loads(self.value)

    @property
    def coords_type(self):
        return self.wkt['type']

    @property
    def coordinates(self):
        return self.wkt['coordinates']


class QueryTypes:
    QUERY_TYPES = Enum('query_type', 'position radius area cube trajectory corridor items locations')

    def __init__(self, is_instances, url_parts):
        try:
            if is_instances:
                self.query_type = self.QUERY_TYPES[url_parts[-1]].name
            else:
                self.query_type = self.QUERY_TYPES[url_parts[url_parts.index('collections') + 2]].name
        except KeyError:
            raise ValueError('unsupported query type found in url')

    @property
    def value(self):
        return self.query_type

    @property
    def is_position(self):
        return self.query_type == 'position'

    @property
    def is_radius(self):
        return self.query_type == 'radius'

    @property
    def is_area(self):
        return self.query_type == 'area'

    @property
    def is_cube(self):
        return self.query_type == 'cube'

    @property
    def is_trajectory(self):
        return self.query_type == 'trajectory'

    @property
    def is_corridor(self):
        return self.query_type == 'corridor'

    @property
    def is_items(self):
        return self.query_type == 'items'

    @property
    def is_locations(self):
        return self.query_type == 'locations'
