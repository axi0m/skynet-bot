"""
Author: axi0m
Purpose: Slack Bot to help the slack admins
"""

import slack
import os
import time

'''
TODO:
Add logging module and debug/info logging
Add commands that'd be useful to have
Add plugins in plugins directory
Add more unit tests
'''

# 1 second delay for websocket connection to start and read events

WEBSOCKET_DELAY = 1


@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    '''
    Response to 'message' events from RTM API
    '''

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
        if response["error"] == "ratelimited":
            print("[!] Rate-limit exceeded: {}".format(response))
        if response["error"] == "account_inactive":
            print("[!] Bot account is inactive: {}".format(response))
        if response["error"] == "token_revoked":
            print("[!] API token has been revoked: {}".format(response))
        if response["error"] == "invalid_auth":
            print("[!] Invalid authentication: {}".format(response))
        assert response["ok"], "[!] Error returned from response"

    else:
        print("[!] Not a valid command...")


def verify_token():
    '''
    Verify our API token exists
    '''

    try:
        slack_token = os.environ.get('SLACK_API_TOKEN')
        return slack_token
    except (Exception, SystemExit) as e:
        print('[!] Unable to set API token: {}'.format(e))


def main():
    '''
    Main function. Verify token, create client, loop client on all events
    '''
    slack_token = verify_token()
    slack_client = slack.RTMClient(token=slack_token)

    while True:
        try:
            slack_client.start()
        except Exception as e:
            print("[!] Unhandled exception encountered: {}".format(e))
        time.sleep(WEBSOCKET_DELAY)


if __name__ == "__main__":
    main()
