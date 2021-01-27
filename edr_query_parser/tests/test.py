import unittest
from edr_query_parser.edr_query_parser import EDRQueryParser
from dateutil.parser import isoparse


class TestEDRQueryParserMethods(unittest.TestCase):
    def test_get_collection(self):
        test_data = [
            {'url': 'https://somewhere.com/collections/my_collection/corridor?', 'expected': 'my_collection'},
            {'url': 'https://somewhere.com/collections/collections/position?', 'expected': 'collections'},
            {'url': 'https://somewhere.com/collections/observations/position?', 'expected': 'observations'},
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.get_collection_name(), test_dic['expected'])

    def test_get_collection_raise_exception(self):
        test_data = [
            {'url': 'https://somewhere.com/v1/collections/position?'},
            {'url': 'https://somewhere.com/collections/position?'},
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertRaises(ValueError, edr.get_collection_name)

    def test_get_query_type(self):
        test_data = [
            {'url': 'https://somewhere.com/collections/my_collection/position?', 'expected': 'position'},
            {'url': 'https://somewhere.com/collections/my_collection/radius?', 'expected': 'radius'},
            {'url': 'https://somewhere.com/collections/my_collection/area?', 'expected': 'area'},
            {'url': 'https://somewhere.com/collections/my_collection/cube?', 'expected': 'cube'},
            {'url': 'https://somewhere.com/collections/my_collection/trajectory?', 'expected': 'trajectory'},
            {'url': 'https://somewhere.com/collections/my_collection/corridor?', 'expected': 'corridor'},
            {'url': 'https://somewhere.com/collections/my_collection/items?', 'expected': 'items'},
            {'url': 'https://somewhere.com/collections/my_collection/locations?', 'expected': 'locations'},
            {'url': 'https://somewhere.com/collections/my_collection/instances?', 'expected': 'instances'},
            {'url': 'https://somewhere.com/collections/metar/locations/EGLL?', 'expected': 'locations'},
            {'url': 'https://somewhere.com/collections/metar/items/KIAD_2020-05-19T00Z?', 'expected': 'items'},

        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.get_query_type(), test_dic['expected'])

    def test_get_query_type_raise_exception(self):
        test_data = [
            {'url': 'https://somewhere.com/collections/my_collection/not_a_query_type?'},
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertRaises(ValueError, edr.get_query_type)

    def test_get_parameter_name(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/position?parameter-name=parameter1,parameter2',
                'expected': ['parameter1', 'parameter2']
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?parameter-name=parameter1',
                'expected': ['parameter1']
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?parameter-name=parameter1,%20parameter2, parameter3',
                'expected': ['parameter1', 'parameter2', 'parameter3']
            },
            {'url': 'https://somewhere.com/collections/my_collection/position', 'expected': None},
            {
                'url': 'https://somewhere.com/collections/my_collection/position?parameter-name=&something=1',
                'expected': None
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/locations/my_locations?parameter-name=parameter1',
                'expected': ['parameter1']
            },
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.get_parameter_name(), test_dic['expected'])

    def test_get_date(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z',
                'expected': isoparse('2018-02-12T23:20:52Z')
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00',
                'expected': isoparse('2019-09-07T15:50-04:00')
            },
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.get_datetime(), test_dic['expected'])

    def test_get_date_raise_exception(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/position?datetime=not_a_date',
                'error_message': 'Datetime format not recognised'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?datetime=23/5/1920',
                'error_message': 'Datetime format not recognised'
            },
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            with self.assertRaises(ValueError) as error:
                edr.get_datetime()
            self.assertEqual(str(error.exception), test_dic['error_message'])

    def test_get_date_missing_raise_exception(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/position?datetime=',
                'error_message': 'Datetime parameter required'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?someparameter=yes',
                'error_message': 'Datetime parameter required'
            },
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            with self.assertRaises(ValueError) as error:
                edr.get_datetime()
            self.assertEqual(str(error.exception), test_dic['error_message'])

    def test_is_date_interval(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z/2018-03-12T23%3A20%3A52Z',
                'expected': True},
            {
                'url': 'https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00',
                'expected': True
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z',
                'expected': False
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00',
                'expected': False
            },
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.is_datetime_interval(), test_dic['expected'])

    def test_get_datetime_from(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z/2018-03-12T23%3A20%3A52Z',
                'expected': isoparse('2018-02-12T23:20:52Z')
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00',
                'expected': isoparse('2019-09-07T15:50-04:00')
            },
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.get_datetime_from(), test_dic['expected'])

    def test_get_datetime_to(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z/2018-03-12T23%3A20%3A52Z',
                'expected': isoparse('2018-03-12T23:20:52Z')
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00',
                'expected': isoparse('2019-09-07T15:50-05:00')
            },
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.get_datetime_to(), test_dic['expected'])

    def test_get_crs(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/position?crs=WGS84',
                'expected': 'WGS84'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position', 'expected': None
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?parameter-name=&something=1',
                'expected': None
            },
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.get_crs(), test_dic['expected'])

    def test_get_format(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/position?f=geoJson',
                'expected': 'geoJson'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?parameter-name=&something=1&f=CoverageJSON',
                'expected': 'CoverageJSON'},
            {
                'url': 'https://somewhere.com/collections/my_collection/position?parameter-name=&something=1',
                'expected': None
            },
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.get_format(), test_dic['expected'])

    def test_get_coords(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/position?coords=POINT(0 51.48)',
                'expected': {'type': 'Point', 'coordinates': [0.0, 51.48]}
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?coords=MULTIPOINT((38.9 -77),(48.85 2.35),(39.92 116.38),(-35.29 149.1),(51.5 -0.1))',
                'expected': {'type': 'MultiPoint',
                             'coordinates': [[38.9, -77.0], [48.85, 2.35], [39.92, 116.38], [-35.29, 149.1],
                                             [51.5, -0.1]]}
            },
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.get_coords(), test_dic['expected'])

    def test_get_coords_type(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/position?coords=POINT(0 51.48)',
                'expected': 'Point'},
            {
                'url': 'https://somewhere.com/collections/my_collection/position?coords=MULTIPOINT((38.9 -77),(48.85 2.35),(39.92 116.38),(-35.29 149.1),(51.5 -0.1))',
                'expected': 'MultiPoint'
            },
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.get_coords_type(), test_dic['expected'])

    def test_get_coords_coordinates(self):
        test_data = [
            {'url': 'https://somewhere.com/collections/my_collection/position?coords=POINT(0 51.48)',
             'expected': [0.0, 51.48]},
            {
                'url': 'https://somewhere.com/collections/my_collection/position?coords=MULTIPOINT((38.9 -77),(48.85 2.35),(39.92 116.38),(-35.29 149.1),(51.5 -0.1))',
                'expected': [[38.9, -77.0], [48.85, 2.35], [39.92, 116.38], [-35.29, 149.1], [51.5, -0.1]]
            },
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.get_coords_coordinates(), test_dic['expected'])

    def test_get_location_id(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/locations/my_location_id/',
                'expected': 'my_location_id'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/locations/', 'expected': None
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/locations', 'expected': None
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/locations/my_locations?parameter-name'
                       '=&something=1',
                'expected': 'my_locations'
            },
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.get_locations_id(), test_dic['expected'])

    def test_get_location_id(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/items/my_item_id/',
                'expected': 'my_item_id'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/items/', 'expected': None
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/items', 'expected': None
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/items/my_item?parameter-name'
                       '=&something=1',
                'expected': 'my_item'
            },
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.get_items_id(), test_dic['expected'])

    def test_get_instances_id(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/instances/my_instances/',
                'expected': 'my_instances'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/instances/', 'expected': None
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/instances', 'expected': None
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/instances/my_instances?parameter-name'
                       '=&something=1',
                'expected': 'my_instances'
            },
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.get_instances_id(), test_dic['expected'])


if __name__ == '__main__':
    unittest.main()
