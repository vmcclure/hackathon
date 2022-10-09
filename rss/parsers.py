import json

from rabbit import RABBIT

r = RABBIT()

def text_parser(url):
    global r
    try:
        r.push_uploaded_tag(json.dumps({"cmd":"text", "url":url}))
    except:
        r = RABBIT()
        r.push_uploaded_tag(json.dumps({"cmd": "text", "url": url}))
    return []
def img_parser(url):
    global r
    try:
        r.push_uploaded_tag(json.dumps({"cmd":"img", "url":url}))
    except:
        r = RABBIT()
        r.push_uploaded_tag(json.dumps({"cmd": "img", "url": url}))
    return []
