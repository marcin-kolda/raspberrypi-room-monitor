import unittest

from parser.parser import Parser


class ParserTest(unittest.TestCase):
    def test_listing(self):
        files = Parser("./kr2*.json").list_files()
        self.assertEqual(2, len(files))

    def test_should_parse_event(self):
        events = Parser("./kr2*.json").list_events()
        self.assertEqual(2, len(events))
        self.assertEqual('test_should_parse_event', events[0].summary)

    def test_should_parse_private_event(self):
        events = Parser("./event_private.json").list_events()
        self.assertEqual(1, len(events))
        self.assertIsNone(events[0].summary)

    def test_should_filter_rejected_event(self):
        events = Parser("./event_rejected.json").list_events()
        self.assertEqual(1, len(events))
        self.assertEqual('ProperEvent', events[0].summary)

    def test_should_parse_date_from_filename(self):
        datetime = Parser.parse_datetime_from_filename("kr2-yellow_2016-07-20_15-51.json")
        self.assertEqual("2016-07-20 15:51:00", datetime.strftime('%Y-%m-%d %H:%M:%S'))
