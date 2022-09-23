from __future__ import unicode_literals
import mariadb
import youtube_dl
import json

mydb = mariadb.connect(
  host="localhost",
  user="root",
  password="",
  database="youtube_dl_mydb"
)

# 
# download video as mp3
# 
def download(url):
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
            updateDownloadedToDB(d)
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
            ydl.download([url])
        except youtube_dl.DownloadError as error:
            pass

# 
# get url basename from playlist
# 
def getUrlBasename(url):
    ydl = youtube_dl.YoutubeDL({'dump_single_json': 'True',
                                'extract_flat' : 'True'})

    with ydl:
        result = ydl.extract_info(url,False)

    if 'entries' in result:
        
    # Can be a playlist or a list of videos
        video = result['entries']
        return video;

#
# save list to database
#
def insertListToDB(url):
    print(mydb)
    mycursor = mydb.cursor()
    query = "INSERT IGNORE INTO video_list set url_id=%(webpage_url_basename)s"

    list = getUrlBasename(url)

    for i, item in enumerate(list):
        urlBasename = list[i]['webpage_url_basename']
        print(urlBasename)

        val = (list[i])
        mycursor.execute(query,val)
        mydb.commit()

        print(mycursor.rowcount, "record inserted.")


# insertListToDB('https://www.youtube.com/playlist?list=PL75MU-kJCnQzk5Uxn6szElwsI31wzPmXS')

#
# update is_downloaded
#
def updateDownloadedToDB(d):
    print(mydb)
    mycursor = mydb.cursor()
    query = "UPDATE video_list set is_downloaded=1 where url_id=%(webpage_url_basename)s"
    # val=(d)
    print(d)
    # mycursor.execute(query,val)
    # mydb.commit()
    print(mycursor.rowcount, "record updated.")

#
# Get video list from db which hasnt been downloaded yet
#
def getListUndownloadFromDB():
    print(mydb)
    mycursor = mydb.cursor(dictionary=True)
    query = "select * from video_list where is_downloaded = 0"
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    
    return myresult
       

#
# MAIN PROGRAM
#
list_for_download = getListUndownloadFromDB()
if list_for_download :
    for item in list_for_download:
        url = 'https://www.youtube.com/watch?v={}'.format(item["url_id"])
        print(url)
        download(url)
else:
    print('no download queue, fetching playlist')
    insertListToDB('https://www.youtube.com/playlist?list=PL75MU-kJCnQzk5Uxn6szElwsI31wzPmXS')