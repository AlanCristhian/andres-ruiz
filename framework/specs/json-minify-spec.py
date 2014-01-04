import json # requires Python 2.6+ to run testsimport os
import os
import sys


# change directroy for import my libraries
os.chdir('../..')
currentDirectory = os.getcwd()
sys.path.append(currentDirectory)
sys.path.append(currentDirectory + '/framework')

from framework import JSONMinify

def test_json(s):
    return json.loads(JSONMinify.minify(s))

test1 = '''// this is a JSON file with comments
{
"foo": "bar",    // this is cool
"bar": [
    "baz", "bum", "zam"
],
/* the rest of this document is just fluff
in case you are interested. */
"something": 10,
"else": 20
}

/* NOTE: You can easily strip the whitespace and comments 
from such a file with the JSON.minify() project hosted 
here on github at http://github.com/getify/JSON.minify 
*/
'''

test1_res = '''{"foo":"bar","bar":["baz","bum","zam"],"something":10,"else":20}'''

test2 = '''
{"/*":"*/","//":"",/*"//"*/"/*/"://
"//"}

'''
test2_res = '''{"/*":"*/","//":"","/*/":"//"}'''

test3 = r'''/*
this is a 
multi line comment */{

"foo"
:
"bar/*"// something
,    "b\"az":/*
something else */"blah"

}
'''
test3_res = r'''{"foo":"bar/*","b\"az":"blah"}'''

test4 = r'''{"foo": "ba\"r//", "bar\\": "b\\\"a/*z", 
"baz\\\\": /* yay */ "fo\\\\\"*/o" 
}
'''
test4_res = r'''{"foo":"ba\"r//","bar\\":"b\\\"a/*z","baz\\\\":"fo\\\\\"*/o"}'''

assert test_json(test1) == json.loads(test1_res),'Failed test 1'
assert test_json(test2) == json.loads(test2_res),'Failed test 2'
assert test_json(test3) == json.loads(test3_res),'Failed test 3'
assert test_json(test4) == json.loads(test4_res),'Failed test 4'
if __debug__: # Don't print passed message if the asserts didn't run
    print('Passed all tests')