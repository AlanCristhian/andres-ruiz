import cgi
import html
import os
import re

from framework import config


rareLetters = (
    # Bocales con acento
    ('á', 'a'),
    ('é', 'e'),
    ('í', 'i'),
    ('ó', 'o'),
    ('ú', 'u'),
    # Bocales con acento grave
    ('à', 'a'),
    ('è', 'e'),
    ('ì', 'i'),
    ('ò', 'o'),
    ('ù', 'u'),
    # Bocales con acento circunflejo
    ('â', 'a'),
    ('ê', 'e'),
    ('î', 'i'),
    ('ô', 'o'),
    ('û', 'u'),
    # Bocles con diéresis
    ('ä', 'a'),
    ('ë', 'e'),
    ('ï', 'i'),
    ('ö', 'o'),
    ('ü', 'u'),
    # Consonantes
    ('ñ', 'ni')
)


def url_filter(string):
    # Pone todo en minúsculas
    string = string.lower()
    # Reemplaza las bocales con signos diacríticos a bocales sin esos signos
    for rare, know in rareLetters:
        string = string.replace(rare, know)
    # elimina los espacios al final
    string = re.compile('\s+$').sub('', string)
    # Reemplaza los espacios por guiones bajos
    string = re.compile('\s+').sub('-', string)
    # Reemplaza los operadores por nada
    string = re.compile('[^\-\sa-zA-Z0-9]*').sub('', string)
    # Elimina los caracteres raros al final
    string = re.compile('[^\sa-zA-Z0-9]+$').sub('', string)
    return string


# XSS defenses
def HTMLEscape(s, quote=True):
    return html.escape(s, quote)


# set to http or https automatic
def set_absolute_path(path, environ=os.environ, config=config.Config()):
    if environ.get('HTTPS'):
        if config.enableSharedSSL:
            return 'https://' + config.sharedSSLPath + '/' + str(path)
        else:
            return 'https://' + config.serverName + '/' + str(path)
    else:
        return 'http://' + config.serverName + '/' + str(path)


# HPP defense
def get_field_storage():
    storage = cgi.FieldStorage()
    try:
        data = {key: storage[key].value for key in storage}
        # data = dict(storage)
    except Exception as e:
        if config.production:
            data = {}
        else:
            raise e
    return data