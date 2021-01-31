from urllib.parse import urlsplit, parse_qs
from dateutil.parser import isoparse
from enum import Enum
from geomet import wkt

class EDRQueryParser:
    def __init__(self, url):
        self.url_list = urlsplit(url).path.split('/')
        self.url_list.pop(0)
        self.url_list = list(filter(None, self.url_list))
        self.query_dic = {str(key): ''.join(value) for key, value in parse_qs(urlsplit(url).query).items()}

    def _get_id(self, query_id):
        if self.query_type == query_id:
            collections_index = self.url_list.index(query_id)
            if len(self.url_list) > collections_index + 1:
                return self.url_list[collections_index + 1]
        return None

    def _get_parameter(self, parameter):
        if parameter in self.query_dic:
            return self.query_dic[parameter]
        return None

    @property
    def collection_name(self):
        collections_index = self.url_list.index('collections')

        if len(self.url_list) != collections_index + 2:
            return self.url_list[collections_index + 1]
        raise ValueError('collection name not found in url')

    @property
    def query_type(self):
        query_type = Enum('query_type', 'position radius area cube trajectory corridor items locations instances')
        collections_index = self.url_list.index('collections')
        try:
            return query_type[self.url_list[collections_index + 2]].name
        except KeyError:
            raise ValueError('unsupported query type found in url')

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
        return Parameter(self._get_parameter('f'))

    @property
    def coords(self):
        return Coords(self._get_parameter('coords'))

    @property
    def crs(self):
        return Parameter(self._get_parameter('crs'))

    @property
    def parameter_name(self):
        return ParameterWithList(self._get_parameter('parameter-name'))

    @property
    def datetime(self):
        return DateTime(self._get_parameter('datetime'))

    @property
    def z(self):
        return Z(self._get_parameter('z'))


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


class ParameterWithInterval(Parameter):

    def _split(self, index=None):
        if self.is_set:
            if '/' in self.value:
                return self.value.split('/')[index]
            return None
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
        try:
            return isoparse(super().interval_from)
        except ValueError:
            raise ValueError('Datetime format not recognised')

    @property
    def interval_to(self):
        try:
            return isoparse(super().interval_to)
        except ValueError:
            raise ValueError('Datetime format not recognised')

    @property
    def exact(self):
        try:
            return isoparse(self.value)
        except ValueError:
            raise ValueError('Datetime format not recognised')


class Z(ParameterWithList, ParameterWithInterval):
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

    @property
    def list(self):
        try:
            return list(map(float, super().list))
        except ValueError:
            raise ValueError('could not convert parameter to a list')


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
