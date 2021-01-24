import unittest
from edr_query_parser import EDRQueryParser
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
            {'url': 'https://somewhere.com/collections/my_collection/instances?', 'expected': 'instances'}
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
            {'url': 'https://somewhere.com/collections/my_collection/position?parameter-name=parameter1,parameter2',
             'expected': ['parameter1', 'parameter2']},
            {'url': 'https://somewhere.com/collections/my_collection/position?parameter-name=parameter1',
             'expected': ['parameter1']},
            {
                'url': 'https://somewhere.com/collections/my_collection/position?parameter-name=parameter1,%20parameter2, parameter3',
                'expected': ['parameter1', 'parameter2', 'parameter3']},
            {'url': 'https://somewhere.com/collections/my_collection/position', 'expected': None},
            {'url': 'https://somewhere.com/collections/my_collection/position?parameter-name=&something=1',
             'expected': None},
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.get_parameter_name(), test_dic['expected'])

    def test_get_date(self):
        test_data = [
            {'url': 'https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z',
             'expected': isoparse('2018-02-12T23:20:52Z')},
            {'url': 'https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00',
             'expected': isoparse('2019-09-07T15:50-04:00')},
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.get_datetime(), test_dic['expected'])

    def test_get_date_raise_exception(self):
        test_data = [
            {'url': 'https://somewhere.com/collections/my_collection/position?datetime=not_a_date',
             'error_message': 'Datetime format not recognised'},
            {'url': 'https://somewhere.com/collections/my_collection/position?datetime=23/5/1920',
             'error_message': 'Datetime format not recognised'},
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            with self.assertRaises(ValueError) as error:
                edr.get_datetime()
            self.assertEqual(str(error.exception), test_dic['error_message'])

    def test_get_date_missing_raise_exception(self):
        test_data = [
            {'url': 'https://somewhere.com/collections/my_collection/position?datetime=',
             'error_message': 'Datetime parameter required'},
            {'url': 'https://somewhere.com/collections/my_collection/position?someparameter=yes',
             'error_message': 'Datetime parameter required'},
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            with self.assertRaises(ValueError) as error:
                edr.get_datetime()
            self.assertEqual(str(error.exception), test_dic['error_message'])

    def test_is_date_interval(self):
        test_data = [
            {'url': 'https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z/2018-03-12T23%3A20%3A52Z',
             'expected': True},
            {'url': 'https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00',
             'expected': True},
            {'url': 'https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z',
             'expected': False},
            {'url': 'https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00',
             'expected': False},
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.is_datetime_interval(), test_dic['expected'])

    def test_get_datetime_from(self):
        test_data = [
            {'url': 'https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z/2018-03-12T23%3A20%3A52Z',
             'expected': isoparse('2018-02-12T23:20:52Z')},
            {'url': 'https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00',
             'expected': isoparse('2019-09-07T15:50-04:00')},
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.get_datetime_from(), test_dic['expected'])

    def test_get_datetime_to(self):
        test_data = [
            {'url': 'https://somewhere.com/collections/my_collection/position?datetime=2018-02-12T23%3A20%3A52Z/2018-03-12T23%3A20%3A52Z',
             'expected': isoparse('2018-03-12T23:20:52Z')},
            {'url': 'https://somewhere.com/collections/my_collection/position?datetime=2019-09-07T15:50-04:00/2019-09-07T15:50-05:00',
             'expected': isoparse('2019-09-07T15:50-05:00')},
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.get_datetime_to(), test_dic['expected'])

    def test_get_crs(self):
        test_data = [
            {'url': 'https://somewhere.com/collections/my_collection/position?crs=WGS84',
             'expected': 'WGS84'},
            {'url': 'https://somewhere.com/collections/my_collection/position', 'expected': None},
            {'url': 'https://somewhere.com/collections/my_collection/position?parameter-name=&something=1',
             'expected': None},
        ]

        for test_dic in test_data:
            edr = EDRQueryParser(test_dic['url'])
            self.assertEqual(edr.get_crs(), test_dic['expected'])

if __name__ == '__main__':
    unittest.main()
