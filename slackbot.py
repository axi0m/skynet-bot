"""
Author: axi0m
Purpose: Slack Bot to help the slack admins
Acknowledgements:
https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
https://medium.com/@greut/a-slack-bot-with-pythons-3-5-asyncio-ad766d8b5d8f#.r6tx149q3
https://12factor.net/
https://gist.github.com/ckinsey/5777f03d2a775a04c43a96de6698cb77
https://hirelofty.com/blog/how-build-slack-bot-mimics-your-colleague/
"""

import time
import slack
import os
import sys

# Globals
DEBUG = True


@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']
    webclient = payload['web_client']
    text = data.get('text')
    channel_id = data['channel']
    thread_ts = data['ts']
    user = data['user']

    if 'Hello' in text:
        response = webclient.chat_postMessage(
            channel=channel_id,
            text="Hi <@{}>!".format(user),
            thread_ts=thread_ts,
        )
        print(response)
        assert response["ok"]

    else:
        print("[!] Waiting for commands...")


def verify_token():
    '''
    Verify our API token exists and is not None
    '''

    try:
        slack_token = os.environ.get('SLACK_API_TOKEN')
    except:
        raise Exception('[!] Unable to set API token')
        sys.exit(1)
    else:
        if slack_token is not None:
            print('[+] API token present and set')
            return slack_token
        else:
            raise Exception('[!] Unable to set API token')
            sys.exit(1)


def main():
    # Verify API Token
    slack_token = verify_token()
    slack_client = slack.RTMClient(token=slack_token)
    try:
        slack_client.start()
    except (KeyboardInterrupt, SystemExit):
        raise Exception("[!] Keyboard Interrupt Encounted - Program Exiting")
    except Exception as e:
        print("[!] Unhandled exception encountered: {}".format(e))


if __name__ == "__main__":
    main()
