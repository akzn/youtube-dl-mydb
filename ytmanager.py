from __future__ import unicode_literals
import mariadb
import youtube_dl
import json
import time
# import TestPP
# from TestPP import TestPP
class YtManager:
    def __init__(self,url_list):

        #load config
        with open('config.json') as file:
            config = json.load(file)

        self.dbcon = mariadb.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
        )

        #param
        self.base_url = "https://www.youtube.com"
        self.playlist_url = url_list
        self.current_download_url_id = ""
        self.current_download_url = ""

    # 
    # get url basename from playlist
    # 
    def getUrlBasename(self):
        ydl = youtube_dl.YoutubeDL({'dump_single_json': 'True',
                                    'extract_flat' : 'True'})

        with ydl:
            result = ydl.extract_info(self.playlist_url,False)

        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries']
            return video
        else:
            return false
    #
    # save list to database
    #
    def insertListToDB(self):
        print(self.dbcon)
        mycursor = self.dbcon.cursor()
        query = "INSERT IGNORE INTO video_list set url_id=%(webpage_url_basename)s, title=%(title)s"

        list = self.getUrlBasename()

        for i, item in enumerate(list):
            urlBasename = list[i]['webpage_url_basename']
            print(urlBasename)

            val = (list[i])
            mycursor.execute(query,val)
            self.dbcon.commit()

            print(mycursor.rowcount, "record inserted.")
        
    #
    # Get video list from db which hasnt been downloaded yet
    #
    def getListUndownloadFromDB(self):
        mycursor = self.dbcon.cursor(dictionary=True)
        query = "select * from video_list where is_downloaded = 0"
        mycursor.execute(query)
        myresult = mycursor.fetchall()
        
        return myresult
    #
    # update is_downloaded
    #
    def updateDownloadedToDB(self):
        mycursor = self.dbcon.cursor()
        url_id = self.current_download_url_id
        query = "UPDATE video_list set is_downloaded=1 where url_id=%s"
        val=([url_id])
        mycursor.execute(query,val)
        self.dbcon.commit()
        print(mycursor.rowcount, "record updated.")

    
    # 
    # download video as mp3
    # 
    def download(self):
        class MyLogger(object):
            def debug(self, msg):
                pass

            def warning(self, msg):
                pass

            def error(self, msg):
                print(msg)


        def my_hook(d):
            if d['status'] == 'finished':
                print('Done downloading, now converting ...')
                self.updateDownloadedToDB()

            if d['status'] == 'downloading':
                print(d['filename'], d['_percent_str'], d['_eta_str'])


        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.cache.remove()
                ydl.add_post_processor(TestPP(None))
                ydl.download([self.current_download_url])
            except youtube_dl.DownloadError as error:
                pass

    def run(self):
        list_for_download = self.getListUndownloadFromDB()
        if list_for_download :
            print('queue for downloading found')
            for item in list_for_download:
                url = 'https://www.youtube.com/watch?v={}'.format(item["url_id"])
                self.current_download_url_id = item["url_id"]
                self.current_download_url = url
                print('Trying to download file...')
                time.sleep(1)
                self.download()
        else:
            print('no download queue, fetching playlist')
            self.insertListToDB()

    
YtManager = YtManager('https://www.youtube.com/playlist?list=PL75MU-kJCnQzlIRV6sgbikcWsjrzPpfMh')
YtManager.run()