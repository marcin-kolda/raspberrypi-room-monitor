import logging
import os

from oauth2client import tools
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage

SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_google_credentials(args):
    flow = flow_from_clientsecrets('client_secrets.json', scope=SCOPES)

    credentials_filename = 'calendar_credentials.json'

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, credentials_filename)

    storage = Storage(credential_path)
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, args)
        logging.info("Google credentials created successfully")
    else:
        logging.info("Google credentials loaded successfully from %s" % credentials_filename)
    return credentials
