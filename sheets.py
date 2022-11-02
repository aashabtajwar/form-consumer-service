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


from extension import logging


r = redis.Redis(host='localhost', port=6379)

class UpdateSheet:
    def upload_data(self, data, form_id, form_link, sheet_name):


        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        range = sheet_name + "!A2"

        SERVICE_ACCOUNT_FILE = 'keys.json'

        creds = None
        creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        
        try:
            service = build('sheets', 'v4', credentials=creds)
            sheet = service.spreadsheets()
            request = sheet.values().append(spreadsheetId=form_link, range=range, valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body={"values":data}).execute()
            # data upload successful
            logging.info('Uploaded Data to Google Sheets')
            print(request)
        except HttpError as err:
            # if fails because of request limitation, store the data in redis
            # and start the backoff on a thread
            
            # log -> quota limit reached, resolving with exponential backoff
            warning = ''
            if (err.status_code == 429):
                logging.warning('Google Sheets Quota Limit Reached. Trying to Resolve with Exponential Backoff')
                cache_data = {
                    'link': form_link,
                    'data': data
                }
                r.set(form_id, str(cache_data))
                self.backoff(data, creds, form_link, form_id, sheet_name, 60, err)
                print(err)
            
            else:
                # if an error occurs other than the one caused by Quota Limit
                # then log the error proceed to run the method again
                logging.warning(f'Error \n: {err}\nProceeding the to run the method again')
                self.upload_data(data, form_id, form_link, sheet_name)
                # otherwise,response may get lost

    def backoff(self, data, creds, form_link, form_id,sheet_name, wait_time, err):
        error = err 
        
        # setting wait time for 60 seconds
        while (error != None):
            print(f'Waiting for {wait_time} seconds before attempting again')
            time.sleep(wait_time)
            error = None 
            try:
                SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
                range = sheet_name + "!A2"
                SERVICE_ACCOUNT_FILE = 'keys.json'

                service = build('sheets', 'v4', credentials=creds)
                sheet = service.spreadsheets()
                request = sheet.values().append(spreadsheetId=form_link, range=range, valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body={"values":data}).execute()
                # the data is successfully uploaded to sheets
                # remove the this data from the cache
                r.delete(form_id)
                
                # log -> data upload successful
                logging.info('Data successfully uploaded after recovering from quota limit.')
                return request 
            except HttpError as err:
                # log -> failed, quota block has not been lifted yet, proceeding to wait and try again
                logging.warning('Upload failed. Quota Block has been not lifted yet. Proceding to wait and try again')
                if (err.status_code == 429):
                    wait_time += 10
                
                



