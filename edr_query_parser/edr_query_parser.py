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

    def _get_split_parameter(self, parameter, index=None):
        if parameter in self.query_dic:
            if index is None:
                return self.query_dic[parameter]
            if parameter in self.query_dic and '/' in self.query_dic[parameter]:
                return self.query_dic[parameter].split('/')[index]
            return None
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
    def parameter_name(self):
        if 'parameter-name' in self.query_dic:
            return [parameter.strip(' ') for parameter in self.query_dic['parameter-name'].split(',')]
        return None

    @property
    def datetime_from(self):
        try:
            return isoparse(self._get_split_parameter('datetime', 0))
        except ValueError:
            raise ValueError('Datetime format not recognised')

    @property
    def datetime_to(self):
        try:
            return isoparse(self._get_split_parameter('datetime', 1))
        except ValueError:
            raise ValueError('Datetime format not recognised')

    @property
    def datetime(self):
        try:
            return isoparse(self._get_split_parameter('datetime'))
        except ValueError:
            raise ValueError('Datetime format not recognised')

    @property
    def is_datetime_interval(self):
        if 'datetime' in self.query_dic:
            return '/' in self.query_dic.get('datetime')
        return False

    @property
    def format(self):
        if 'f' in self.query_dic:
            return self.query_dic.get('f')
        return None

    @property
    def coords(self):
        return wkt.loads(self.query_dic.get('coords'))

    @property
    def coords_type(self):
        return self.coords['type']

    @property
    def coords_coordinates(self):
        return self.coords['coordinates']

    @property
    def crs(self):
        if 'crs' in self.query_dic:
            return self.query_dic.get('crs')
        return None

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
    def z(self):
        try:
            return float(self._get_split_parameter('z'))
        except (TypeError, ValueError):
            raise ValueError('z can not be cast to float')

    @property
    def z_list(self):
        try:
            return list(map(float, [parameter.strip(' ') for parameter in self.query_dic['z'].split(',')]))
        except (ValueError, KeyError):
            raise ValueError('unable to create z list')

    @property
    def z_from(self):
        try:
            return float(self._get_split_parameter('z', 0))
        except (ValueError, TypeError):
            raise ValueError('unable to get z from value')

    @property
    def z_to(self):
        try:
            return float(self._get_split_parameter('z', 1))
        except (ValueError, TypeError):
            raise ValueError('unable to get z to value')

    @property
    def is_z_interval(self):
        return 'z' in self.query_dic and'/' in self.query_dic.get('z')

    @property
    def is_z_list(self):
        return 'z' in self.query_dic and ',' in self.query_dic.get('z')

    @property
    def is_z_all(self):
        return 'z' in self.query_dic and self.query_dic['z'].lower() == 'all'
