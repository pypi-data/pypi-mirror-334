import requests_text
import requests

s = requests.Session()
s.mount("text://", requests_text.TextAdapter())


def test_request():
    assert s.get("text://some_text").text == "some_text"
