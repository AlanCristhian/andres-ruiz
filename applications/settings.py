# This module only contains some variables that are used to set some
# default behaviors framework.

# They are in the folder applications because it will be modified by the
# user.
config = {
    # Set "production: false" while developing. If production is false
    # the browser shows the error message of scripts.
    "production": False

    # Set Warnings false if you do not want displayed in the test.
    # ,"warnings": True

    # Set consolelog to true if test this from the terminal
    ,"consolelog": False

    # The folder where place the database file and every statics
    # files of the web page such as images, videos and music.
    ,"databaseFolder": "database/"

    # the folder where place all directories for each article
    ,"filesFolder": "database/files"

    # The default database engine used by framework.
    # Current database systems supported: sqlite3
    ,"databaseEngine": "sqlite3"

    # The default file that stores the data
    ,"databaseFile": "models.db"

    # The name of the cookie to manage user sessions
    ,"cookieName": "andres_norberto_ruiz_session_id"

    # Lifetime of the user session. The valid unites are:
    # seconds, minutes, hours, days, wheeks, months and years
    ,"timeSession": "7 days"

    # manage the protocol
    ,'enableHTTPS': False

    # The route that causes a redirect to https.
    ,"securePath": "\/admin\/"

    # Set it to true if you has an shared ssl hosting.
    # Please uncomment the correct lines into .htacces file.
    ,"enableSharedSSL": False

    # The route with the shared ssl path.
    # Please uncomment the correct lines into .htacces file.
    ,"sharedSSLDomain": "andres.dev"
    # The shared ssl user name with the bar (/)
    ,'sharedSSLUser': "/~andresru"
    ,"sharedSSLPath": "andres.dev/~andresru"

    ,"expirationDate": 0

    # Defaul image size to responsive responses
    ,"image": {
        "small": 360
        ,"medium": 480
        ,"large": 720
        ,"extralarge": 1080
    }
    ,"imageSample": {
        "small": 252
        ,"medium": 336
        ,"large": 504
        ,"extralarge": 756
    }
    ,"thumbnail": {
        "small": 45
        ,"medium": 120
        ,"large": 180
        ,"extralarge": 270
    }
    ,"minWidth": {
        "small": 360
        ,"medium": 480
        ,"large": 720
        ,"extralarge": 1080
    }
    # remember that you should change the style.less file if you
    # change the "imageIndex" key.
    ,"imageIndex": {
        "small": 144
        ,"medium": 192
        ,"large": 288
        ,"extralarge": 432
    }

    # Here is defined the JPG compression quality for sencha.io
    ,"JPGQuality": 90
}