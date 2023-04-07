from __future__ import unicode_literals
import mariadb
import json
from pathlib import Path
class DbManager:
    def __init__(self):
        #load config
        path = Path(__file__).parent.absolute()
        configpath = '{}/config.json'.format(path)
        with open(configpath) as file:
            config = json.load(file)

        self.dbcon = mariadb.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
        )
    
    #
    # save list to database
    #
    def insertListToDB(self,url_list):
        mycursor = self.dbcon.cursor()
        query = "INSERT IGNORE INTO video_list(url_id,title) values(%(id)s,%(title)s)"
        # query = "INSERT IGNORE INTO video_list set url_id=%(id)s, title=%(title)s"

        list = url_list

        for i, item in enumerate(list):
            if list is not None:
                urlBasename = list[i]['id'] if list is not None else None
                print(urlBasename)
                val = (list[i])
                mycursor.execute(query,val)
                self.dbcon.commit()
                print(mycursor.rowcount, "record inserted.")
            else:
                print('no data, skipped')

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
    def updateDownloadedToDB(self,current_download_url_id):
        mycursor = self.dbcon.cursor()
        url_id = current_download_url_id
        query = "UPDATE video_list set is_downloaded=1 where url_id=%s"
        val=([url_id])
        mycursor.execute(query,val)
        self.dbcon.commit()
        print(mycursor.rowcount, "record updated.")