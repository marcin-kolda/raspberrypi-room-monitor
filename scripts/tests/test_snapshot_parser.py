import unittest

from parser.snapshot_parser import SnapshotParser


class SnapshotParserTest(unittest.TestCase):
    def test_should_parse_event(self):
        events = SnapshotParser("./event_postponed*.json").merge_snapshots('2016-06-18')
        self.assertEqual(2, len(events))
        self.assertEqual('Test 10', events[0].summary)
        self.assertEqual('moved', events[0].status)
        self.assertEqual('Test 11 - green', events[1].summary)
        self.assertEqual('cancelled', events[1].status)

    def test_should_ignore_overwritten_events(self):
        events = SnapshotParser("./event_overwritten*.json").merge_snapshots('2016-06-27')
        self.assertEqual(1, len(events))
        self.assertEqual("confirmed_meeting", events[0].summary)
        self.assertEqual('confirmed', events[0].status)

    def test_should_not_override_snapshot_date(self):
        events = SnapshotParser("./kr2-yellow*.json").merge_snapshots('2016-06-01')
        self.assertEqual(1, len(events))
        self.assertEqual("2016-06-01 00:00:00", events[0].snapshot_datetime)


        # don't update summary if removed

        # ignore overwritten events