import glob
import json
import csv
import logging
import datetime
import sys
import dateutil.parser

from model import Event


class Parser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.list_file_result = glob.glob(self.filepath)
        self.file_event_cache = {}

    def list_files(self):
        return self.list_file_result

    def list_events(self):
        events = set()
        for json_file in self.list_files():
            new_events = self.get_events(json_file)
            events = events.union(new_events)
        return list(events)

    @staticmethod
    def _is_item_valid(item):
        if 'summary' in item and item['summary'] == 'CANCELLED' and item['status'] == 'cancelled':
            return False
        if 'attendees' in item:
            for attendee in item['attendees']:
                if 'self' in attendee and 'responseStatus' in attendee and attendee['responseStatus'] == 'declined':
                    return False
        return True

    @staticmethod
    def format_datetime(datetime_string):
        return dateutil.parser.parse(datetime_string).strftime('%Y-%m-%d %H:%M:%S')

    def parse_event(self, item):
        try:
            return Event(event_id=item['id'],
                         created=self.format_datetime(item['created']) if 'created' in item else None,
                         status=item['status'],
                         recurring_event_id=item['recurringEventId'] if 'recurringEventId' in item else None,
                         summary=item['summary'] if 'summary' in item else None,
                         updated=self.format_datetime(item['updated']),
                         start_date_time=self.format_datetime(item['start']['dateTime']),
                         end_date_time=self.format_datetime(item['end']['dateTime']),
                         organizer=item['organizer']['email'] if 'organizer' in item else None)
        except ValueError as err:
            logging.warning("Unable to parse event\n%s\n due to %s" % (item, err))

    def get_events(self, json_file):
        if json_file in self.file_event_cache:
            return self.file_event_cache[json_file]
        logging.debug("Parsing " + json_file)
        with open(json_file) as data_file:
            events = set()
            data = json.load(data_file)
            parsed_snapshot_datetime = Parser.parse_datetime_from_filename(json_file)
            snapshot_datetime_string = parsed_snapshot_datetime.strftime('%Y-%m-%d %H:%M:%S') if parsed_snapshot_datetime else None
            for item in data['items']:
                if self._is_item_valid(item):
                    event = self.parse_event(item)
                    if event:
                        event.snapshot_datetime = snapshot_datetime_string
                        events.add(event)
            self.file_event_cache[json_file] = events
            return events

    @staticmethod
    def parse_datetime_from_filename(filename):
        try:
            datetime_string = filename.split('_', 1)[1].split('.')[0]
            return datetime.datetime.strptime(datetime_string, '%Y-%m-%d_%H-%M')
        except ValueError, e:
            logging.warning("Can't parse date: %s" % e.message)
            return None

class Writer:
    def __init__(self):
        pass

    @staticmethod
    def write_events_as_csv_file(filename, events):
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['start_date_time', 'end_date_time', 'created', 'updated', 'event_id',
                             'recurring_event_id', 'summary', 'status', 'organizer', 'id', 'snapshot_datetime'])
            for event in events:
                summary = event.summary.encode('utf-8') if event.summary else ""
                writer.writerow([event.start_date_time, event.end_date_time, event.created, event.updated, event.event_id,
                                 event.recurring_event_id, summary, event.status, event.organizer, event.event_id, event.snapshot_datetime])

