import argparse
import bs4
import json
import requests

parser = argparse.ArgumentParser(description='TDF 2016 DATA SCRAPER')
parser.add_argument('stage', type=int, nargs=1, help='What stage?')
args = parser.parse_args()

stage = args.stage[0]
statistics_url = 'https://www.holdet.dk/da/tour-de-france-2016/statistics/'
data = []

for page in xrange(0,8):
    # Page number as parameter
    params = '?page='+str(page)
    # Request the page
    page = requests.get(statistics_url + str(stage) + params)
    # Initiate parser
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    # Grab table rows
    rows = soup.select('tbody > tr')

    for row in rows:
        # Grab all column entries
        cols = row.select('td')

        # Helper: strip newlines
        F = lambda str: "0" if str.lstrip().rstrip() == "-" else str.lstrip().rstrip()

        # Grab data for each rider
        rider = {}
        rider['id'] = cols[0].get_text()
        rider['name'] = cols[1].select('a')[0].get_text()
        rider['team'] = cols[1].select('div')[0].get_text()[:-9]
        rider['value'] = int(F(cols[2].get_text()).replace('.', ''))
        rider['growth'] = int(F(cols[3].get_text()).replace('.', ''))
        rider['growth_tot'] = int(F(cols[4].get_text()).replace('.', ''))
        rider['gc'] = int(F(cols[5].get_text()))
        rider['sprint'] = int(F(cols[6].get_text()))
        rider['mountain'] = int(F(cols[7].get_text()))
        rider['stage'] = int(F(cols[8].get_text()))
        rider['sprint_points'] = int(F(cols[9].get_text()))
        rider['mountain_points'] = int(F(cols[10].get_text()))
        rider['popularity'] = float(F(cols[11].get_text())[:-1].replace(',', '.'))
        rider['trend'] = float(F(cols[12].get_text()))
        
        # SAVE
        data.append(rider)


with open(str(stage) + ".json", "w") as file:
    file.write(json.dumps(data))