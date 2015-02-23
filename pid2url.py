import pandas as pd
import os
import urllib
import re


def make_url(pid):
    requestURL = 'http://wiki.ubc.ca/wiki?curid=' + str(pid)
    raw = urllib.urlopen(requestURL).read()

    match = re.search(r'(<title>).*(</title>)', raw).group()
    match = match.split(' -')[0].split('<title>')[1].replace(' ', '_')
    if 'Science' in match:
        url = 'http://wiki.ubc.ca/' + match
    else:
        url = ''
    return url


if __name__ == '__main__':
    if not os.path.exists('rating_pid.csv'):
        raise Exception('Require rating_pid.csv')

    df = pd.read_csv('rating_pid.csv')
    df['url'] = df['pageID'].apply(make_url)
    df = df[df.url != '']
    df.to_csv('rating_pid_url.csv')