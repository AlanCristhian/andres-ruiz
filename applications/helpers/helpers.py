from framework.config import Config
from framework import helpers

import re


def remove_leftover_new_lines(text):
    """Remove all leftover new lines character of an text. Also remove the new
    lines if it has after than another character. Too remove the new lines
    characters if it is at the end of the text string.
    """
    if text is None:
        return ''
    # normalize the new line in all text
    newLineNormalized = text.replace('\r', '\n')
    # set just one new line character per paragraph
    oneNewLine = re.compile('\n+').sub('\n', newLineNormalized)
    # remove the first new line character
    if oneNewLine[0] == '\n':
        oneNewLine = oneNewLine[1:]
    # remove the last new line character
    if oneNewLine[-1] == '\n':
        oneNewLine = oneNewLine[:-1]
    return oneNewLine


def paragraph_filter(text):
    """wraps all paragraph labeled <p>"""
    # set all paragraph as item of the list
    paragraphList = remove_leftover_new_lines(text).split('\n')
    # wraps all paragraph with the <p> label
    result = []
    for paragraph in paragraphList:
        result = result + ['<p>' + paragraph + '</p>']
    # join all paragraph and return it
    return ''.join(result)


def fix_edit_url(url):
    """Add the **shared ssl user name** if is an https protocol and the
    sharedSSL variable is enabled in the applications/settings.py config file.
    """
    if helpers.get_protocol() == 'https' and Config().enableSharedSSL:
        return '~andresru/' + url
    else:
        return url

def remove_user_name(url):
    return url.replace('~andresru/', '')