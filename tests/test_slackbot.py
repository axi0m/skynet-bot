import re
from slackbot import verify_token


def test_verify_token():
    token = verify_token()
    regex = '^xoxb-[0-9]{11}-[0-9]{12}-[a-zA-z0-9]{24}$'
    assert re.match(regex, token) is not None
