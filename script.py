#!/usr/bin/env python3

"""
This script parses a Holberton School web page project
and creates the neccesary files and folders
in your current working directory
given the user id and password of the Holberton intranet,
Created by Joshua Hernandez from Holberton COL-cohort 9.
"""

from getpass import getpass
from sys import argv
import requests
import re
import os

AUTH_REGEX = 'name="authenticity_token" value=.{90}'
PARSE_REGEX = 'File: <code>.*<\/code>'
TITLE_REGEX = '<title>.*<\/title>'
LOGIN_URL = 'https://intranet.hbtn.io/auth/sign_in'

def authenticate(id, pwd):
    """ authenticates into Holberton intranet
    in order to scrap the project page
    """
    s = requests.Session()
    match = re.search(AUTH_REGEX, str(s.get(LOGIN_URL).content, 'utf-8'))
    auth_token = None
    if match:
        auth_token = match.group()[33:-1]
    else:
        print("<ERROR>: Couldn't authenticate to " + LOGIN_URL)
        exit(1)
    response = s.post(
            LOGIN_URL,
            data = {
                    'utf8':'✓',
                    'authenticity_token': auth_token,
                    'user[login]': id,
                    'user[password]': pwd,
                    'user[remember_me]': '0',
                    'commit':'Log in'
                }
            )
    return s

def parse_project_page(cont):
    """ parse the project page in search of
    the files name """
    matches = re.findall(PARSE_REGEX, str(cont, 'utf-8'))
    count = 0
    if matches:
        for match in matches:
            file_name = match[12:-7]
            files = file_name.split(",")
            for f in files:
                f = f.strip()
                if "/" in f:
                    try:
                        os.makedirs(os.path.dirname(f))
                    except OSError:
                        pass
                    name = f.split("/")[-1]
                    if len(name):
                        open(f, "a")
                        count += 1
                else:
                    open(f, "a")
                    count += 1
                print("Created {}".format(f))
    if count:
        match = re.search(TITLE_REGEX, str(cont, 'utf-8'))
        if match:
            f = open("README.md", "w")
            f.write(match.group()[7:-8])
            f.close()
            count += 1
            print("Created README.md")
    return count

if __name__ == '__main__':
    if len(argv) != 2:
        print("USAGE: ./script <url>")
        exit(1)
    url = argv[1]
    id = input("Enter your Holberton School id: ")
    pwd = getpass()
    s = authenticate(id, pwd)
    response = s.get(url).content
    if len(response) < 4550:
        print("<ERROR>: Unable to authenticate, wrong id or password")
        exit(1)
    else:
        print("==========================")
        print("Authenticated successfully")
        print("==========================")

    count = parse_project_page(response)

    if count:
        print("================")
        print("Created {} files".format(count))
        print("================")
        print("******************************************")
        print("** THANKS FOR USING THIS AWESOME SCRIPT **")
        print("******************************************")
    else:
        print("No file names found.")
        print("Are you sure <{}> is a Holberton project page?".format(url))
