from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import pprint
import io
import fileinput


class google_dr:
    @staticmethod
    def get_url(names):
        pp = pprint.PrettyPrinter(indent=4)

        SCOPES = ['https://www.googleapis.com/auth/drive']
        SERVICE_ACCOUNT_FILE = 'Driving-lessons-bot-31272fcd366b.json'

        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)

        results = {}
        res=[]
        prom = {}

        for name in names:
            name = str(name) + "_.png"
            prom = service.files().list(
                pageSize=1000,
                fields="nextPageToken, files(id )",
                q=f"name contains '{name}'").execute()
            #pp.pprint(results['files'][0])
            res += prom['files']
        print(res)

    @staticmethod
    def edit():
        filename ='111.txt'
        with open(f'C:/Users/andre/PycharmProjects/driving_lesson_bot/scripts/{filename}') as file_in:
            text = file_in.read()

        text = text.replace(",)", "")

        with open(f'C:/Users/andre/PycharmProjects/driving_lesson_bot/scripts/{filename}', "w") as file_out:
            file_out.write(text)

        text = text.replace("(", "")

        with open(f'C:/Users/andre/PycharmProjects/driving_lesson_bot/scripts/{filename}', "w") as file_out:
            file_out.write(text)

    @staticmethod
    def edit_():
        filename = '222'
        with open(f'C:/Users/andre/PycharmProjects/driving_lesson_bot/scripts/{filename}') as file_in:
            text = file_in.read()

        text = text.replace("}", "")

        with open(f'C:/Users/andre/PycharmProjects/driving_lesson_bot/scripts/{filename}', "w") as file_out:
            file_out.write(text)

        text = text.replace("{'id':", "")

        with open(f'C:/Users/andre/PycharmProjects/driving_lesson_bot/scripts/{filename}', "w") as file_out:
            file_out.write(text)

google_dr.edit_()

#n=['7.1.2', '7.1.3', '7.1.4', '7.2.1', '7.2.2', '7.2.3', '7.2.4', '7.2.5', '7.2.6', '7.3.1', '7.3.2', '7.3.3', '7.4.1', '7.4.2', '7.4.3', '7.4.4', '7.4.5', '7.4.6', '7.4.7', '7.5.1', '7.5.2', '7.5.3', '7.5.4', '7.5.5', '7.5.6', '7.5.7', '7.5.8', '7.6.1', '7.6.2', '7.6.3', '7.6.4', '7.6.5', '7.7', '7.8', '7.9', '7.10', '7.11', '7.12', '7.13', '7.14', '7.15', '7.16', '7.17', '7.18', '7.19', '7.20', '7.21.1', '7.21.2', '7.21.3', '7.21.4', '7.22', '7.1.1']
#google_dr.get_url(n)
