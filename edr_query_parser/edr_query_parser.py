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
    QUERY_TYPES = Enum('query_type', 'position radius area cube trajectory corridor items locations')

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
        if len(self.url_parts) != self.url_parts.index('collections') + 2:
            return self.url_parts[self.url_parts.index('collections') + 1]
        raise ValueError('collection name not found in url')

    @property
    def query_type(self):
        try:
            if self.is_instances:
                return self.QUERY_TYPES[self.url_parts[-1]].name
            return self.QUERY_TYPES[self.url_parts[self.url_parts.index('collections') + 2]].name
        except KeyError:
            raise ValueError('unsupported query type found in url')

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


class Parameter:
    def __init__(self, value):
        self.value = value

    @property
    def is_set(self):
        return self.value is not None


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
        try:
            return self._split(0)
        except (ValueError, TypeError):
            raise ValueError('unable to get interval from value')

    @property
    def interval_to(self):
        try:
            return self._split(1)
        except (ValueError, TypeError):
            raise ValueError('unable to get interval to value')


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
