from __future__ import unicode_literals
from ytmanager import YtManager
from dbmanager import DbManager
import time
import json
from pathlib import Path
class YtPlaylistMan():    

    def __init__(self):
        # load config
        path = Path(__file__).parent.absolute()
        configpath = '{}/config.json'.format(path)
        with open(configpath) as file:
            config = json.load(file)
        
        #param
        self.playlist_url = config['playlist-url']
        self.current_download_url_id = ""
        self.current_download_url = ""
        # self.dbmanager = DbManager()

    def run(self):
        # get url
        print('fetching playlist...')
        url_list = YtManager(self).getUrlBasename(self.playlist_url)
        time.sleep(1)
        print('Inserting playlist item to database...')
        DbManager().insertListToDB(url_list)


        list_for_download = DbManager().getListUndownloadFromDB()
        if list_for_download :
            print('queue for downloading found')
            for item in list_for_download:
                url = 'https://www.youtube.com/watch?v={}'.format(item["url_id"])
                self.current_download_url_id = item["url_id"]
                self.current_download_url = url
                print('Trying to download file...')
                time.sleep(1)
                try:
                    YtManager(url).download()
                    DbManager().updateDownloadedToDB(item["url_id"])
                except:
                    print('failed to download')
        else:
            print('no download queue')
            


YtPlaylistMan = YtPlaylistMan()
YtPlaylistMan.run()