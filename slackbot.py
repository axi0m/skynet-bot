"""
Author: axi0m
Purpose: Slack Bot to help the slack admins
"""

import slack
import os
import time
import sys
from shodan import Shodan

'''
TODO: Only respond to messages when @'ed. Look for if text contains  to isolate that
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
    user = data.get('user')
    message_type = data.get('subtype')
    bot_id = data.get('bot_id')

    # Check to ensure text is not None
    if text is None:
        print(f"[!] Message is empty")
        return None

    # Check to ensure our user object exists
    if user is None or user is '':
        print(f"[!] Message user field is empty or None")
        return None
    
    # Ignore messages from the Bot itself
    if message_type == 'bot_message':
        print(f"[!] Message is from bot, ignoring")
        return None
    
    # Ignore messages hwere bot_id exists
    if bot_id is not None:
        print(f"[!] Message includes bot_id in data dictionary")
        return None

    if 'hello' in text.lower():
        response = webclient.chat_postMessage(
            channel=channel_id,
            text=f"Hi <@{user}>!",
            thread_ts=thread_ts
        )
        if response["error"] == "ratelimited":
            print(f"[!] Rate-limit exceeded: {response}")
            sys.exit(1)
        if response["error"] == "account_inactive":
            print(f"[!] Bot account is inactive: {response}")
            sys.exit(1)
        if response["error"] == "token_revoked":
            print(f"[!] API token has been revoked: {response}")
            sys.exit(1)
        if response["error"] == "invalid_auth":
            print(f"[!] Invalid authentication: {response}")
            sys.exit(1)
        if response["error"] == "not_authed":
            print(f"[!] Request was not authenticated: {response}")
            sys.exit(1)
        assert response["ok"], "[!] Error returned from response"

    if 'help' in text.lower():
        response = webclient.chat_postMessage(
                channel=channel_id,
                text=f"Here is some help, I support the following commands: Help, Hello",
                thread_ts=thread_ts)
        assert response["ok"], "[!] Error returned from response"

    if 'shodan' in text.lower():

        # Split on space in message
        split_ip = text.split(' ')

        # Post message about checking Shodan
        response = webclient.chat_postMessage(
            channel=channel_id,
            text=f"Checking Shodan for IPv4 Address: {split_ip[2]}",
            thread_ts=thread_ts)
        assert response["ok"], "[!] Error returned from response"

        # Pass IP to Shodan function
        results = shodan_check_ipinfo(split_ip[2])

        # Post results of Shodan API search
        response = webclient.chat_postMessage(
            channel=channel_id,
            text=f"Results from Shodan are: {results}",
            thread_ts=thread_ts)
        assert response["ok"], "[!] Error returned from response"

def shodan_check_ipinfo(ipaddr):
        '''
        Gather IP information for supplied IP address from Shodan API
        '''

        shodan_token = verify_shodan_token()
        if shodan_token is not None:
            shodan_client = Shodan(shodan_token)
            ipinfo = shodan_client.host(ipaddr)
            filtered_output = ipinfo.get('ports')
        return filtered_output


def verify_slack_token():
    '''
    Verify our API token exists
    '''

    slack_token = os.environ.get('SLACK_API_TOKEN')

    if slack_token is None:
        print(f"[!] API token is missing for Slack, exiting...")
        sys.exit(1)
    return slack_token


def verify_shodan_token():
    '''
    Verify our Shodan API token exists
    '''

    shodan_token = os.environ.get('SHODAN_API_KEY')
    
    if shodan_token is None:
        print(f"[!] API token is missing for Shodan, exiting...")
        sys.exit(1)
    return shodan_token

def main():
    '''
    Main function. Verify token, create client, loop client on all events
    '''
    slack_token = verify_slack_token()
    if slack_token is not None:
        slack_client = slack.RTMClient(token=slack_token)

    try:
        while True:
            slack_client.start()
            time.sleep(WEBSOCKET_DELAY)
    except KeyboardInterrupt:
        print(f"[!] KeyboardInterrupt has been caught")
        sys.exit(0)


if __name__ == "__main__":
    main()
