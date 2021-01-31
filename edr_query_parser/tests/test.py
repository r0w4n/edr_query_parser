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
            self.assertEqual(edr.collection_name, test_dic['expected'])

    def test_get_collection_raise_exception(self):
        test_data = [
            {'url': 'https://somewhere.com/v1/collections/position?'},
            {'url': 'https://somewhere.com/collections/position?'},
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])

            with self.assertRaises(ValueError) as cm:
                edr.collection_name
            self.assertEqual(
                'collection name not found in url',
                str(cm.exception)
            )

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
            self.assertEqual(edr.query_type, test_dic['expected'])

    def test_get_query_type_raise_exception(self):
        test_data = [
            {'url': 'https://somewhere.com/collections/my_collection/not_a_query_type?'},
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])

            with self.assertRaises(ValueError) as cm:
                edr.query_type
            self.assertEqual(
                'unsupported query type found in url',
                str(cm.exception)
            )

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
            self.assertEqual(edr.parameter_name, test_dic['expected'])

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
            self.assertEqual(edr.datetime, test_dic['expected'])

    def test_get_date_raise_exception(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/position?datetime=not_a_date',
                'error_message': 'Datetime format not recognised'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?datetime=23/5/1920',
                'error_message': 'Datetime format not recognised'
            }
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            with self.assertRaises(ValueError) as error:
                edr.datetime
            self.assertEqual(str(error.exception), test_dic['error_message'])

    def test_get_date_from_raise_exception(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/position?datetime=not_a_date/2018-03-12T23%3A20%3A52Z',
                'error_message': 'Datetime format not recognised'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?datetime=3422-23423-234/2018-03-12T23%3A20%3A52Z',
                'error_message': 'Datetime format not recognised'
            }
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            with self.assertRaises(ValueError) as error:
                edr.datetime_from
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
            {
                'url': 'https://somewhere.com/collections/my_collection/position',
                'expected': False
            },
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.is_datetime_interval, test_dic['expected'])

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
            self.assertEqual(edr.datetime_from, test_dic['expected'])

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
            self.assertEqual(edr.datetime_to, test_dic['expected'])

    def test_get_datetime(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z',
                'expected': isoparse('2018-02-12T23:20:52Z')
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00',
                'expected': isoparse('2019-09-07T15:50-04:00')
            }
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.datetime, test_dic['expected'])

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
            self.assertEqual(edr.crs, test_dic['expected'])

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
            self.assertEqual(edr.format, test_dic['expected'])

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
            self.assertEqual(edr.coords, test_dic['expected'])

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
            self.assertEqual(edr.coords_type, test_dic['expected'])

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
            self.assertEqual(edr.coords_coordinates, test_dic['expected'])

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
            self.assertEqual(edr.locations_id, test_dic['expected'])

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
            self.assertEqual(edr.items_id, test_dic['expected'])

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
            self.assertEqual(edr.instances_id, test_dic['expected'])

    def test_is_z_interval(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=12/13',
                'expected': True
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=500/400',
                'expected': True
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=All',
                'expected': False
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=12,23,34',
                'expected': False
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=',
                'expected': False
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position',
                'expected': False
            },
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.is_z_interval, test_dic['expected'])

    def test_is_z_list(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=12/13',
                'expected': False
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=500,400',
                'expected': True
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=All',
                'expected': False
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=12,23,34',
                'expected': True
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=',
                'expected': False
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position',
                'expected': False
            },
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.is_z_list, test_dic['expected'])

    def test_get_z_list(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=12/13',
                'expected': 'unable to create z list'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=500,400',
                'expected': [500, 400]
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=All',
                'expected': 'unable to create z list'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=12,23,34',
                'expected': [12, 23, 34]
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=',
                'expected': 'unable to create z list'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position',
                'expected': 'unable to create z list'
            },
        ]

        for test_dic in test_data:
            try:
                edr = EDRQueryParser(test_dic['url'])
                self.assertEqual(edr.z_list, test_dic['expected'])
            except ValueError as raisedException:
                self.assertEqual(
                    test_dic['expected'],
                    str(raisedException)
                )

    def test_get_z(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=12',
                'expected': 12
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=All',
                'expected': 'z can not be cast to float'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=12.5',
                'expected': 12.5
            },

            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=500,400',
                'expected': 'z can not be cast to float'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=All',
                'expected': 'z can not be cast to float'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=all',
                'expected': 'z can not be cast to float'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=ALL',
                'expected': 'z can not be cast to float'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=12,23,34',
                'expected': 'z can not be cast to float'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=',
                'expected': 'z can not be cast to float'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position',
                'expected': 'z can not be cast to float'
            },
        ]

        for test_dic in test_data:
            try:
                edr = EDRQueryParser(test_dic['url'])
                self.assertEqual(edr.z, test_dic['expected'])
            except ValueError as raisedException:
                self.assertEqual(
                    test_dic['expected'],
                    str(raisedException)
                )


    def test_get_z_from(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=12/13',
                'expected': 12
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=500,400',
                'expected': 'unable to get z from value'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=All',
                'expected': 'unable to get z from value'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=12,23,34',
                'expected': 'unable to get z from value'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=',
                'expected': 'unable to get z from value'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position',
                'expected': 'unable to get z from value'
            },
        ]

        for test_dic in test_data:
            try:
                edr = EDRQueryParser(test_dic['url'])
                self.assertEqual(edr.z_from, test_dic['expected'])
            except ValueError as raisedException:
                self.assertEqual(
                    test_dic['expected'],
                    str(raisedException)
                )

    def test_get_z_to(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=12/13',
                'expected': 13
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=500,400',
                'expected': 'unable to get z to value'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=All',
                'expected': 'unable to get z to value'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=12,23,34',
                'expected': 'unable to get z to value'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=',
                'expected': 'unable to get z to value'
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position',
                'expected': 'unable to get z to value'
            },
        ]

        for test_dic in test_data:
            try:
                edr = EDRQueryParser(test_dic['url'])
                self.assertEqual(edr.z_to, test_dic['expected'])
            except ValueError as raisedException:
                self.assertEqual(
                    test_dic['expected'],
                    str(raisedException)
                )

    def test_is_z_all(self):
        test_data = [
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=12',
                'expected': False
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=all',
                'expected': True
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=All',
                'expected': True
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=ALL',
                'expected': True
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=12,23,34',
                'expected': False
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position?z=',
                'expected': False
            },
            {
                'url': 'https://somewhere.com/collections/my_collection/position',
                'expected': False
            },
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.is_z_all, test_dic['expected'])


if __name__ == '__main__':
    unittest.main()
