import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def main():
    acc = get_acc_name()
    command = input('Here is list of information that you can get about user:\n1. Number of friends\n2. List of friends'
                    '\n3. Location of friends\n4. Description of any friend\n\nPlease, enter a command number: ')
    data = read_data(get_json_data(acc))

    if command == '1':
        print(data['n_of_friends'])
    elif command == '2':
        for u in data['friends']:
            print(u)
    elif command == '3':
        for u in data['locations']:
            print('{}: {}'.format(u[0], u[1]))
    elif command == '4':
        for u in data['descriptions']:
            print('{}: {}'.format(u[0], u[1]))


def get_acc_name():
    while True:
        print('')
        acc = input('Enter Twitter Account:')
        if len(acc) > 1:
            return acc
        else:
            break


def get_json_data(acc):
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acc, 'count': '5'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    js = json.loads(data)
    # headers = dict(connection.getheaders())
    return js


def read_data(js):
    data_dict = dict()
    data_dict['n_of_friends'] = len(js['users'])
    data_dict['friends'] = []
    data_dict['locations'] = []
    data_dict['descriptions'] = []
    for u in js['users']:
        data_dict['friends'].append(u['name'])
        data_dict['locations'].append((u['screen_name'], u['location']))
        data_dict['descriptions'].append((u['name'], u['description']))
    return data_dict

if __name__ == '__main__':
    main()
