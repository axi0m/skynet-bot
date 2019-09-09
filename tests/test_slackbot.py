import re
from slackbot import verify_token


mock_token = 'xoxb-63453559156-670321563755-lJRai9S0j6vE42bkRmFZG58W'
mock_payload = {
    'text': 'Hello'
}

def test_verify_token(token=mock_token):
    assert re.match('^xoxb-[0-9]{11}-[0-9]{12}-[a-zA-z0-9]{24}$', token)