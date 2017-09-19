from parser import Parser, Writer
import datetime
from snapshot_parser import SnapshotParser
import logging
import sys
from datetime import date

logging.basicConfig(format='%(asctime)s %(levelname)-5s %(filename)-12s %(message)s', level=logging.INFO, stream=sys.stdout)

try:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="File path pattern to directory with calendar JSON data (e.g. calendar-raw/*.json)")
    parser.add_argument("output_filepath", help="Output file path (e.g. events.csv)")
    args = parser.parse_args()
except ImportError:
    args = None

d1 = date(2016, 5, 30)
d2 = date.today()
delta = d2 - d1
date_list = [(d1 + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]

date_list = filter(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').isoweekday() in range(1, 6), date_list)

print date_list

events = []
parser = SnapshotParser(args.filepath)
for date in date_list:
    events.extend(parser.merge_snapshots(date))

    Writer.write_events_as_csv_file(args.output_filepath, events)
