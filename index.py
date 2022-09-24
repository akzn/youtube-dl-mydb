from __future__ import unicode_literals
from ytmanager import YtManager
from dbmanager import DbManager
import time

class YtPlaylistMan():    

    def __init__(self,url_list):
        #param
        self.base_url = "https://www.youtube.com"
        self.playlist_url = url_list
        self.current_download_url_id = ""
        self.current_download_url = ""
        # self.dbmanager = DbManager()

    def run(self):
        # get url
        print('fetching playlist')
        url_list = YtManager(self).getUrlBasename(self.playlist_url)
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
            

YtPlaylistMan = YtPlaylistMan('https://www.youtube.com/playlist?list=PL75MU-kJCnQzlIRV6sgbikcWsjrzPpfMh')
# YtPlaylistMan = YtPlaylistMan("https://www.youtube.com/playlist?list=PL75MU-kJCnQx82DQiTQRDKuZoajexibEs")
YtPlaylistMan.run()