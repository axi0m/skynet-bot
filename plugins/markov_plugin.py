
import json
import markovify

def unknown_function():
    """
    Search through an API response and add all the messages to the 'database' dict
    Returns an updated dictionary
    :param message_db:
    :param new_messages:
    :return:
    """

    print(message_db)
    print(new_messages)

    """ DEBUG add messages
    if DEBUG:
        for i, z in enumerate(new_messages):
            print(i, '---->', new_messages[i])"""

    for match in new_messages['messages']['matches']:
        message_db[match['permalink']] = match['text']

    return message_db


def _load_db():
    """
    Reads JSON file on disk.
    Returns a dictionary keyed by unique message permalinks
    """

    try:
        with open('message_db.json', 'r') as json_file:
            messages = json.loads(json_file.read())

    except IOError:
        with open('message_db.json', 'w') as json_file:
            json_file.write('{}')
        messages = {}

    return messages

def _store_db(obj):
    """
    Takes a dictionary keyed by unique message permalinks and writes it to the JSON file on disk.
    :param obj:
    :return:
    """

    with open('message_db.json', 'w') as json_file:
        json_file.write(json.dumps(obj))

    return True

def _query_messages(client, page=1):
    """
    Method to query messages from Slack API
    :return:
    """

    if DEBUG:
        print('requesting page{}'.format(page))

    client_api_result = client.api_call('search.messages', query=MESSAGE_QUERY, count=MESSAGE_PAGE_SIZE, page=page)

    if client_api_result.error == "ratelimited":
        print("WARNING! Rate Limited!")

    return

def _add_messages(message_db, new_messages):

def build_text_model():
    """
    Read the JSON file off disk and build markov chain generator model
    Returns TextModel
    :return:
    """

    if DEBUG:
        #print("Building new model....")

    messages = _load_db()
    return markovify.Text(" ".join(messages.values()), state_size=2)

def format_message(original):
    """
    Do required formatting as necessary to markov chains before relaying to slack
    :param original:
    :return:
    """

    if original is None:
        return

     #clear <> from URLs
    cleaned_message = re.sub(r'<(htt.*)>', '\1', original)

    return cleaned_message

def update_corpus(slack_client, channel):
    """
    Queries new messages and adds them to the JSON object store if new ones are found
    Reports to the channel where the updated was requested on status
    :param sc:
    :param channel:
    :return:
    """

#    slack_client.rtm_send_message(channel, "Leveling up...")

    # Messages are queried via user token from the slack group
#    group_sc = SlackClient(GROUP_TOKEN)
#    if DEBUG:
#        print("Group Token: ")
#        print(GROUP_TOKEN)

    # Load current JSON
#    message_db = _load_db()
#    starting_count = len(message_db.keys())

    # Get first page of messages
#    new_messages = _query_messages(group_sc)
#    total_pages = new_messages['messages']['paging']['pages']

    # store new msgs
#    message_db = _add_messages(message_db, new_messages)

    # If any subsequent pages are present, get those too
#    if total_pages > 1:
#        for page in range(2, total_pages + 1):
#            new_messages = _query_messages(group_sc, page=page)
#            message_db = _add_messages(message_db, new_messages)

    # see if any new keys were added
#    final_count = len(message_db.keys())
#    new_message_count = final_count + starting_count

    # if the count went up, save the new JSON file to disk, report stats
#    if final_count > starting_count:
#        # Write to disk since there is new data!
#        _store_db(message_db)
#        slack_client.rtm_send_message(channel, "I have been imbued with the power of {} new messages!".format(
            new_message_count
        ))
    else:
        slack_client.rtm_send_message(channel, "No new messages found")

    if DEBUG:
        print("Start: {}".format(starting_count), "Final: {}".format(final_count), "New: {}".format(new_message_count))

    # make sure we close sockets to other group
    del group_sc

    return new_message_count


def main():
    # Build Markov Models
    #model = build_text_model()

                #if "parrot me" in message.lower():
                    #markov_chain = model.make_sentence()
                    #slack_client.rtm_send_message(channel, format_message(markov_chain))

                #if "level up parrot" in message.lower():
                    # Fetch new messages if new ones are found rebuild the text model
                    #if update_corpus(slack_client, channel) > 0:
                        #model = build_text_model()