import urllib.request
local_filename, headers = urllib.request.urlretrieve('http://python.org/', filename='filename')
html = open(local_filename)
html.close()