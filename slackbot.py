"""
Author: axi0m
Purpose: Slack Bot to help the slack admins
"""

import slack
import os

'''
TODO:
1. Add function to test for inactive account - https://api.slack.com/methods/rtm.start/test
2. Add logging module and debug/info logging
3. Add HTTP 429 code handling in case we're rate limited, see Slack RTM API docs
4. Add commands that'd be useful to have
'''


@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']
    webclient = payload['web_client']
    text = data.get('text')
    channel_id = data['channel']
    thread_ts = data['ts']
    user = data['user']

    if 'Hello' in text:
        print('DEBUG: Bot consumed the message')
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
        return slack_token
    except (Exception, SystemExit) as e:
        print('[!] Unable to set API token: {}'.format(e))


def main():
    slack_token = verify_token()
    slack_client = slack.RTMClient(token=slack_token)

    try:
        slack_client.start()
    except Exception as e:
        print("[!] Unhandled exception encountered: {}".format(e))


if __name__ == "__main__":
    main()
