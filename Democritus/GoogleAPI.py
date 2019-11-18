from __future__ import print_function
import csv

from googleapiclient import discovery
from google.oauth2 import service_account

from UFA_Democritus.settings import BASE_DIR, SITE_URL

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = BASE_DIR + '/Democritus-36f51d28620d.json'

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = discovery.build('drive', 'v3', credentials=credentials)


def delete_poll(sender, instance, *args, **kwargs):
    drive_service.files().delete(fileId=instance.id).execute()


def create_new_poll(poll, update):
    print(poll.id)
    file_metadata = {
        'name': 'Democritus: New Poll - ' + poll.question_text,
        'description': 'Go to ' + SITE_URL + ' to engage in democracy!',
        'mimeType': 'application/vnd.google-apps.drive-sdk',
        'id': poll.id,
        'writersCanShare': 'true',
        'copyRequiresWriterPermission': 'true',
        'appProperties': {
            "question_text": poll.question_text,
            "poll_type": poll.poll_type,
            "options": poll.options,
            "end_date": str(poll.end_date)
        }
    }

    if update:
        del file_metadata['id']
        nfile = drive_service.files().update(fileId=poll.id, body=file_metadata, fields='id').execute()
    else:
        nfile = drive_service.files().create(body=file_metadata, fields='id').execute()
    file_id = nfile.get('id')
    print('File ID: %s' % file_id)

    def callback(request_id, response, exception):
        if exception:
            # Handle error
            print(exception)
        else:
            print("Permission Id: %s" % response.get('id'))

    batch = drive_service.new_batch_http_request(callback=callback)
    for row in csv_iter(poll.student_list):
        for email in row:
            print("sharing with " + email)
            user_permission = {
                'type': 'user',
                'role': 'reader',
                'emailAddress': email
            }
            batch.add(drive_service.permissions().create(
                fileId=file_id,
                sendNotificationEmail=False,
                body=user_permission,
                fields='id',
            ))
    batch.execute()


def csv_iter(self):
    return csv.reader([self.document.read().decode("utf-8")])


def csv_to_list(self):
    return list(csv.reader([self.document.read().decode("utf-8")]))[0]


def generate_id():
    return drive_service.files().generateIds(count=1, space='drive').execute().get('ids')[0]
