from collections import OrderedDict
from parser import Parser
import logging


class SnapshotParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.parser = Parser(self.filepath)

    def merge_snapshots(self, date_filter):
        files = self.parser.list_files()
        logging.info("Filtering events for %s" % date_filter)
        snapshot = {}
        last_day_to_be_parsed = False
        for json_file in files:
            if last_day_to_be_parsed and date_filter not in json_file:
                break
            events = self.parser.get_events(json_file)
            new_snapshot = self.transform_event_set_to_map(self.filter_events(events, date_filter=date_filter))
            self._update(snapshot, new_snapshot, snapshot_time=Parser.parse_datetime_from_filename(json_file))
            if date_filter in json_file:
                last_day_to_be_parsed = True
        return OrderedDict(sorted(snapshot.items())).values()

    @staticmethod
    def filter_events(events, date_filter):
        for event in events:
            if date_filter in event.start_date_time:
                yield event

    @staticmethod
    def transform_event_set_to_map(event_set):
        event_map = {}
        for event in event_set:
            if event.start_date_time in event_map:
                if event.status == 'confirmed':
                    #logging.info("Overriding meeting '%s', start: %s, from %s to %s" % (
                    #    event.summary, event.start_date_time, event_map[event.start_date_time].status, event.status))
                    event_map[event.start_date_time] = event
                #else:
                    #logging.info("Ignoring meeting '%s', start: %s, existing status: %s, new: %s" % (
                    #    event.summary, event.start_date_time, event_map[event.start_date_time].status, event.status))
            else:
                event_map[event.start_date_time] = event

        return event_map

    def _update(self, snapshot, new_snapshot, snapshot_time):
        for key, value in snapshot.iteritems():
            if key not in new_snapshot:
                if value.status != 'moved':
                    value.status = 'moved'
                    value.snapshot_datetime = snapshot_time
            else:
                new_value = new_snapshot[key]
                if not new_value.__eq__(value):
                    snapshot[key] = new_value
        for key, value in new_snapshot.iteritems():
            if key not in snapshot:
                snapshot[key] = value
