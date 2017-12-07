#!/bin/python

"""Script to get PR(Pull Request) statistics from GitHub
Usage:
    pr-stats [options] <user> <repo>
    User name and password could be defined in config file or promted from stdin
    -a, --after:                Show PR opened after this date
    -b, --before:               Show PR opened before this date
    -c, --comments:             Show number of comments created
    -cb, --closed-by:           Show user who closed
    -dwc, --day-of-week-closed: Show day of the week closed
    -dwo, --day-of-week-opened: Show day of the week opened
    -d, --days:                 Show number of days opened
    -h, --help:                 Show that information
    -ob, --opened-by:           Show user who opened
    -s, --statistic:            Show statistics
    -v, --version:              Show version info
"""

import ConfigParser
from datetime import datetime
from getpass import getpass
import logging
import re
from sys import argv
import requests


config = ConfigParser.RawConfigParser()
config.read('config.conf')
user_name = config.get('general', 'User')
password = config.get('general', 'Password')
version = config.get('general', 'version')
log_level = config.get('general', 'log_level')
log_path = config.get('general', 'log_path')

argv.pop(0)
opt_matcher = re.compile("-(\S+)")
options = filter(opt_matcher.match, argv)
user_matcher = re.compile("[^-]\S+")
user_input = filter(user_matcher.match, argv)


def print_version():
    return "Current version %s" % version


def help_info():
    return '''Usage:
    pr-stats [options] <user> <repo>

    -a, --after:                Show PR opened after this date
    -b, --before:               Show PR opened before this date
    -c, --comments:             Show number of comments created
    -cb, --closed-by:           Show user who closed
    -dwc, --day-of-week-closed: Show day of the week closed
    -dwo, --day-of-week-opened: Show day of the week opened
    -d, --days:                 Show number of days opened
    -h, --help:                 Show that information
    -ob, --opened-by:           Show user who opened
    -s, --statistic:            Show statistics
    -v, --version:              Show version info

    '''

if '--version' in options:
    print print_version()
    quit(0)
if '-h' in options or '--help' in options:
    print help_info()
    quit(0)

if not user_name:
    user_name = raw_input("Please enter GitHub username: ")
if not password:
    password = getpass(prompt="Please enter GitHub password: ")

try:
    owner = user_input[0]
    repo = user_input[1]
except Exception:
    print help_info()

logging.basicConfig(format='%(asctime)s %(message)s', filename=log_path, level=log_level)


all_url = 'https://api.github.com/repos/' + owner + '/' + repo + '/pulls?state=all'
closed_url = 'https://api.github.com/repos/' + owner + '/' + repo + '/pulls?state=closed'
opened_url = 'https://api.github.com/repos/' + owner + '/' + repo + '/pulls?state=open'


def read_pages(url):
    def next_page(links):
        r = requests.get(links['next']['url'], auth=(user_name, password))
        output = []
        if 'next' in r.links.keys():
            output = next_page(r.links)
        return r.json() + output
    r = requests.get(url, auth=(user_name, password))
    output = []
    if r.links:
        output = (next_page(r.links))
    return r.json() + output


def calculate(array, property):
    count = 0
    for x in array:
        if x[property]:
            count += 1
    return count


def ps_days_opened(array):
    d = {}
    for x in array:
        date_str = x['created_at']
        d.update({x['title'] : datetime.now() - datetime.strptime(date_str[:-1], '%Y-%m-%dT%H:%M:%S')})
    return d


def number_of_comments(array):
    d = {}
    for x in array:
        pr_num = str(x['number'])
        url = 'https://api.github.com/repos/' + owner +'/' + repo + '/pulls/' + pr_num + '/comments'
        pr_comments = read_pages(url)
        d.update({x['title']: len(pr_comments)})
    return d


def day_of_the_week(array, property):
    d = {}
    calendar = {"0": "Monday", "1": "Tuesday", "2": "Wednesday", "3": "Thursday",
                "4": "Friday", "5": "Saturday", "6": "Sunday"}
    for x in array:
        date_str = x[property]
        weekday = datetime.strptime(date_str[:-1], '%Y-%m-%dT%H:%M:%S').weekday()
        d.update({x['title']: calendar[str(weekday)]})
    return d


def labels(array):
    d = {}
    for x in array:
        r = requests.get('https://api.github.com/repos/' + owner + '/' + repo + '/issues/' + str(x['number']),
                         auth=(user_name, password))
        if r.json()['labels']:
            d.update({x['title']: r.json()['labels'][0]['name']})
    return d


def closed_by(array):
    d = {}
    for x in array:
        r = requests.get('https://api.github.com/repos/' + owner + '/' + repo + '/issues/' + str(x['number']), auth=(user_name, password))
        if r.json()['closed_by']['login']:
            d.update({x['title'] : r.json()['closed_by']['login']})
    return d


def opened_by(array):
    d = {}
    for x in array:
        r = requests.get('https://api.github.com/repos/' + owner + '/' + repo + '/issues/' + str(x['number']), auth=(user_name, password))
        if r.json()['user']['login']:
            d.update({x['title'] : r.json()['user']['login']})
    return d


def remove_before_date(array, date):
    l = []
    for x in array:
        pr_date_str = x['created_at']
        pr_date = datetime.strptime(pr_date_str[:-1], '%Y-%m-%dT%H:%M:%S')
        if not pr_date <= date:
            l.append(x)
    return l


def remove_after_date(array, date):
    l = []
    for x in array:
        pr_date_str = x['created_at']
        pr_date = datetime.strptime(pr_date_str[:-1], '%Y-%m-%dT%H:%M:%S')
        if pr_date >= date:
            l.append(x)
    return l


def nice_print(dct):
    print "----------------------------------------------------------"
    max_width = max(map(len, dct))
    for k, v in dct.iteritems(): print "{0:<{width}} - {1:<{width}}".format(k, v, width=max_width)


def shift_if_needed(array):
    if '-b' in options or '--before' in options:
        mydate = datetime.strptime(raw_input("Enter date [dd-mm-yy HH:MM]: "), '%d-%m-%y %H:%M')
        return remove_before_date(array, mydate)
    elif '-a' in options or '--after' in options:
        mydate = datetime.strptime(raw_input("Enter date [dd-mm-yy HH:MM]: "), '%d-%m-%y %H:%M')
        return remove_before_date(array, mydate)
    return array

if '-s' in options or '--statistic' in options:
    all_pr = read_pages(all_url)
    print "Closed pull requests in {0} repositoy: {1}".format(repo, calculate(all_pr, 'closed_at'))
    print "Merged pull requests in {0} repositoy: {1}".format(repo, calculate(all_pr, 'merged_at'))
if '-d' in options or '--days' in options:
    open_pr = read_pages(opened_url)
    nice_print(ps_days_opened(shift_if_needed(open_pr)))
if '-c' in options or '--comments' in options:
    open_pr = read_pages(opened_url)
    nice_print(number_of_comments(shift_if_needed(open_pr)))
if '-dwo' in options or '--day-of-week-opened' in options:
    open_pr = read_pages(opened_url)
    nice_print(day_of_the_week(shift_if_needed(open_pr), 'created_at'))
if '-dwc' in options or '--day-of-week-closed' in options:
    closed_pr = read_pages(closed_url)
    nice_print(day_of_the_week(shift_if_needed(closed_pr), 'closed_at'))
if '-l' in options or '--lables' in options:
    open_pr = read_pages(opened_url)
    nice_print(labels(shift_if_needed(open_pr)))
if '-cb' in options or '--closed-by' in options:
    closed_pr = read_pages(closed_url)
    nice_print(closed_by(shift_if_needed(closed_pr)))
if '-ob' in options or '--opened-by' in options:
    all_pr = read_pages(all_url)
    nice_print(opened_by(shift_if_needed(all_pr)))
