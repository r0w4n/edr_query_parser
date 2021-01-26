from urllib.parse import urlsplit, parse_qs
from dateutil.parser import isoparse
from enum import Enum
from geomet import wkt


def parse_datetime(query_dic, index=None):
    check_datetime(query_dic)
    try:
        datetime = query_dic['datetime'].split('/')[index] if index is not None else query_dic['datetime']
        return isoparse(datetime)
    except ValueError:
        raise ValueError('Datetime format not recognised')


def check_datetime(query_dic):
    if 'datetime' not in query_dic:
        raise ValueError('Datetime parameter required')


class EDRQueryParser:
    def __init__(self, url):
        self.url_list = urlsplit(url).path.split('/')
        self.url_list.pop(0)
        self.query_dic = {str(key): ''.join(value) for key, value in parse_qs(urlsplit(url).query).items()}

    def get_collection_name(self):
        collections_index = self.url_list.index('collections')

        if len(self.url_list) != collections_index + 2:
            return self.url_list[collections_index + 1]
        raise ValueError('collection name not found in url')

    def get_query_type(self):
        query_type = Enum('query_type', 'position radius area cube trajectory corridor items locations instances')
        try:
            return query_type[self.url_list[-1]].name
        except KeyError:
            raise ValueError('unsupported query type found in url')

    def get_parameter_name(self):
        if 'parameter-name' in self.query_dic:
            return [parameter.strip(' ') for parameter in self.query_dic['parameter-name'].split(',')]
        return None

    def get_datetime_from(self):
        return parse_datetime(self.query_dic, 0)

    def get_datetime_to(self):
        return parse_datetime(self.query_dic, 1)

    def get_datetime(self):
        return parse_datetime(self.query_dic)

    def is_datetime_interval(self):
        return "/" in self.query_dic.get('datetime')

    def get_format(self):
        if 'f' in self.query_dic:
            return self.query_dic.get('f')
        return None

    def get_coords(self):
        return wkt.loads(self.query_dic.get('coords'))

    def get_coords_type(self):
        return self.get_coords()['type']

    def get_coords_coordinates(self):
        return self.get_coords()['coordinates']

    def get_crs(self):
        if 'crs' in self.query_dic:
            return self.query_dic.get('crs')
        return None
