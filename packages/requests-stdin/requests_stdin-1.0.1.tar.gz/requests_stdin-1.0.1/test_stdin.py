import requests_stdin
import requests

s = requests.Session()
s.mount("stdin://", requests_stdin.StdinAdapter())
import sys
import io


def test_request():
    sys.stdin = io.StringIO("some_text")
    assert s.get("stdin://some_text").text == "some_text"


if __name__ == "__main__":
    print("one")
