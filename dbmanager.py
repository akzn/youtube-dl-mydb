from __future__ import unicode_literals
import mariadb
import json
from ytmanager import YtManager

class DbManager:
    def __init__(self):
        #load config
        with open('config.json') as file:
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
        query = "INSERT IGNORE INTO video_list set url_id=%(webpage_url_basename)s, title=%(title)s"

        # list = YtManager(self).getUrlBasename()
        list = url_list

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
    def updateDownloadedToDB(self,current_download_url_id):
        mycursor = self.dbcon.cursor()
        url_id = current_download_url_id
        query = "UPDATE video_list set is_downloaded=1 where url_id=%s"
        val=([url_id])
        mycursor.execute(query,val)
        self.dbcon.commit()
        print(mycursor.rowcount, "record updated.")