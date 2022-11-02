import os.path
import time
import redis
from threading import Thread

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



from google.oauth2 import service_account

\
r = redis.Redis(host='localhost', port=6379)

class UpdateSheet:
    def upload_data(self, data, form_id, form_link, sheet_name):


        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        range = sheet_name + "!A2"


        # SCOPES = ['https://www.googleapis.com/auth/sqlservice.admin']
        SERVICE_ACCOUNT_FILE = 'keys.json'

        creds = None
        creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        
        try:
            service = build('sheets', 'v4', credentials=creds)
            sheet = service.spreadsheets()
            request = sheet.values().append(spreadsheetId=form_link, range=range, valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body={"values":data}).execute()
            return (request)
        except HttpError as err:
            # if fails because of request limitation, store the data in redis
            # and start the backoff on a thread
            cache_data = {
                'link': form_link,
                'data': data
            }
            self.backoff(data, creds, form_link, sheet_name, 60, err)
            print(err)
            

    def backoff(self, data, creds, form_link, sheet_name, wait_time, err):
        error = err 
        
        # setting wait time for 60 seconds
        while (error != None):
            print(f'Waiting for {wait_time} seconds before attempting again')
            time.sleep(wait_time)
            error = None 
            try:
                SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
                range = sheet_name + "!A2"
                # SCOPES = ['https://www.googleapis.com/auth/sqlservice.admin']
                SERVICE_ACCOUNT_FILE = 'keys.json'

                service = build('sheets', 'v4', credentials=creds)
                sheet = service.spreadsheets()
                request = sheet.values().append(spreadsheetId=form_link, range=range, valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body={"values":data}).execute()
                return request 
            except HttpError as err:
                if (err.status_code == 429):
                    wait_time += 10
                
                



