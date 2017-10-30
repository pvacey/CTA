#!/usr/bin/python
"""No Ice Guy comments "Nice." on posts """
import requests
import requests.auth

def reddit_login():
    """Function to log into Reddit"""
    try:
        client_auth = requests.auth.HTTPBasicAuth(
            'dB7dGPEQ9WmQ0A', 'aB9NZYuvYCYLe2--da_I45v9p70')
        post_data = {"grant_type": "password",
                     "username": "no_ice_guy", "password": "dogpoop"}
        headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}
        response = requests.post("https://www.reddit.com/api/v1/access_token",
                                 auth=client_auth, data=post_data, headers=headers)
        access_token = dict(response.json())['access_token']
    except requests.exceptions.RequestException as error:
        print error
        exit()

    headers = {"Authorization": "bearer {}".format(
        access_token), "User-Agent": "NoIceBot/0.1 by dj_bulbasaur"}
    response = requests.get("https://reddit.com/api/me.json", headers=headers)

    return response.ok


if __name__ == '__main__':
    print reddit_login()
