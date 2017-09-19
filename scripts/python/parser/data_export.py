import csv
import datetime
import logging
import sys
from datetime import date

import dateutil.parser
import httplib2
from apiclient import discovery
from oauth2client import tools

import google_api

logging.basicConfig(format='%(asctime)s %(levelname)-5s %(filename)-12s %(message)s', level=logging.INFO, stream=sys.stdout)

try:
    import argparse

    parser = argparse.ArgumentParser(parents=[tools.argparser])
    args = parser.parse_args()
except ImportError:
    args = None

credentials = google_api.get_google_credentials(args)

http = credentials.authorize(httplib2.Http())
calendar_service = discovery.build('calendar', 'v3', http=http)

calendars = {
    "Room1": "room1@resource.calendar.google.com",
    "Room2": "room2@resource.calendar.google.com",
}

fields = 'accessRole,description,etag,' \
         'items(anyoneCanAddSelf,attendees,attendeesOmitted,colorId,created,creator,end,endTimeUnspecified,etag,gadget,guestsCanInviteOthers,' \
         'guestsCanModify,guestsCanSeeOtherGuests,htmlLink,iCalUID,id,location,locked,organizer,originalStartTime,privateCopy,recurrence,' \
         'recurringEventId,sequence,source,start,status,summary,transparency,updated,visibility),kind,nextPageToken,nextSyncToken,summary,' \
         'timeZone,updated'

headers = ['office', 'floor', 'conf', 'event_id', 'created', 'status', 'recurring_event_id', 'summary', 'updated', 'start_date_time', 'end_date_time',
           'organizer', 'organizer_name', 'creator', 'html_link']


def format_datetime(datetime_string):
    return dateutil.parser.parse(datetime_string).strftime('%Y-%m-%d %H:%M:%S')


def event_from_different_calendar(item):
    if 'attendees' in item:
        for attendee in item['attendees']:
            if 'self' in attendee and 'responseStatus' in attendee:
                if attendee['responseStatus'] == 'declined' or attendee['responseStatus'] == 'needsAction':
                    return True
    return False


def parse_event(item):
    if 'created' in item and item['created'].startswith('0000'):
        return
    if 'updated' not in item:
        return
    try:
        status = item['status']
        if event_from_different_calendar(item):
            return
        return [item['id'],
                format_datetime(item['created']) if 'created' in item else None,
                status,
                item['recurringEventId'] if 'recurringEventId' in item else None,
                item['summary'].encode('utf-8') if 'summary' in item else None,
                format_datetime(item['updated']),
                format_datetime(item['start']['dateTime']),
                format_datetime(item['end']['dateTime']),
                item['organizer']['email'] if 'organizer' in item else None,
                item['organizer']['displayName'].encode('utf-8') if 'organizer' in item and 'displayName' in item['organizer'] else None,
                item['creator']['email'] if 'creator' in item else None,
                item['htmlLink'] if 'htmlLink' in item else None]
    except (KeyError, ValueError) as err:
        logging.warning("Unable to parse event\n%s\n due to %s" % (item, err))


def write_events_as_csv_file(filename, array_list):
    logging.info('Exporting %d rows to %s' % (len(array_list), filename))
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(headers)
        for array in array_list:
            writer.writerow(array)


def retrieve_events(calendar_id, date_from, date_to, office, floor, conf_room_name, return_deleted, return_single):
    has_more_results = True
    next_page_token = None
    events = []
    while has_more_results:
        events_result = calendar_service.events().list(
            calendarId=calendar_id,
            maxResults=300,
            singleEvents=return_single,
            timeMin=date_from.strftime('%Y-%m-%d') + "T00:00:00-00:00",
            timeMax=date_to.strftime('%Y-%m-%d') + "T00:00:00-00:00",
            orderBy='startTime' if return_single else None,
            pageToken=next_page_token,
            fields=fields,
            showDeleted=return_deleted,
            showHiddenInvitations=True,
            timeZone='Europe/Warsaw').execute()
        if 'nextPageToken' in events_result:
            next_page_token = events_result['nextPageToken']
        else:
            has_more_results = False
        for item in events_result['items']:
            event = parse_event(item)
            if event:
                field_list = [office, floor, conf_room_name]
                field_list.extend(event)
                events.append(field_list)
    return events


def export_events(date_from, date_to, filename, return_single, return_deleted):
    rows = []
    for key, value in calendars.iteritems():
        logging.info("parsing %s", key)
        array = key.split('-')
        office_string = array[0]
        rows.extend(retrieve_events(calendar_id=value, date_from=date_from, date_to=date_to, office=office_string, floor=array[0] + '-' + array[1],
                                    conf_room_name=array[2], return_deleted=return_deleted,
                                    return_single=return_single))
    write_events_as_csv_file(filename, rows)

export_events(date.today() + datetime.timedelta(days=10), date.today() + datetime.timedelta(days=40),
              '../../data/calendar_grouped_confirmed.csv', False, False)

export_events(date.today() - datetime.timedelta(days=90), date.today() + datetime.timedelta(days=30),
              '../../data/calendar_data.csv', True, True)
