import json
import matplotlib.pyplot as plt
from os.path import join
import pandas as pd
import requests


def fetch():
    name = 'us-counties.csv'
    url = ('https://raw.githubusercontent.com/nytimes/'
           'covid-19-data/master/us-counties.csv')
    r = requests.get(url)
    with open(name, 'wb') as f:
        f.write(r.content)
    return name


def read(file):
    return pd.read_csv(file)


def extract_counties(df):
    d = {}
    for index, row in df.iterrows():
        if row.state not in d:
            d[row.state] = []
        if row.county not in d[row.state]:
            d[row.state].append(row.county)
    return d


def select_county(df, county, state):
    return df[(df.county == county) & (df.state == state)]


def process_county(c):
    d = pd.DataFrame(columns=['date', 'cases', 'new_cases', 'deaths'])
    d.date = c.date
    d.cases = c.cases
    d.deaths = c.deaths
    d.new_cases = c.cases - c.cases.shift(1)
    d.iloc[0, d.columns.get_loc('new_cases')] = 0
    return d


def plot_county(df, county, state):
    prefix = join('app-engine', 'static', 'images')
    title = ('Covid-19 in %s, %s\nSee https://github.com/rscohn2/covid-county'
             ' for code and data source' % (county, state))
    c = process_county(select_county(df, county, state))
    ax = c.plot('date', 'cases', title=title, rot=45)
    c.plot('date', 'deaths', ax=ax)
    p = c.plot('date', 'new_cases', secondary_y=True, ax=ax, rot=45)
    p.get_figure().savefig(join(prefix, '%s:%s.png' % (county, state)),
                           bbox_inches='tight')
    plt.close()


def get_plots():
    states_path = join('app-engine', 'static', 'jsondata', 'counties.json')
    df = read(fetch())
    states = extract_counties(df)
    for s in states:
        states[s].sort()
    with open(states_path, 'w') as fout:
        json.dump(states, fout, indent=1, sort_keys=True)
    for s in states:
        for c in states[s]:
            print('%s, %s' % (c, s))
            plot_county(df, c, s)
            break
        break


def main():
    get_plots()


main()
