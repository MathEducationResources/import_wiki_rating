import pandas as pd
import os
import urllib
import re


def make_url(pid):
    requestURL = 'http://wiki.ubc.ca/wiki?curid=' + str(pid)
    if requestURL in known_urls.keys():
        # Memoization FTW!
        return known_urls[requestURL]
    else:
        raw = urllib.urlopen(requestURL).read()

        match = re.search(r'(<title>).*(</title>)', raw).group()
        match = match.split(' -')[0].split('<title>')[1].replace(' ', '_')
        if 'Science' in match:
            url = 'http://wiki.ubc.ca/' + match
        else:
            url = ''
        known_urls[requestURL] = url
    return url


if __name__ == '__main__':
    if not os.path.exists('rating_pid.csv'):
        raise Exception('Require rating_pid.csv')

    df = pd.read_csv('rating_pid.csv')
    known_urls = {}
    df['URL'] = df['pageID'].apply(make_url)
    df = df[df.URL != '']
    df.to_csv('rating_pid_url.csv', index=False)
