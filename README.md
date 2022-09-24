
## YOUTUBE PLAYLIST MANAGER

My noob attempt to save my youtube playlist to database.

Because sometimes youtube video got removed or set to private.
  
for now only basic function is available
* save playlist to db
* download playlist to local path

### Requirement
1. youtube-dl python module
2. mariadb python module
3. mysql-server

### Usage
1. restore scheme.sql to mysql server
2. make config.json from config.json.example
3. edit config.json to your server configuration
4. run index.py
