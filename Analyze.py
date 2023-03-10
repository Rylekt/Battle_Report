import requests
from bs4 import BeautifulSoup

def analyze_replay(url):
    # Extract replay data from the URL
    r = requests.get(url)
    #print(r)
    soup = BeautifulSoup(r.content, 'html.parser')
    #print("Line 9 ", soup) # HTML script
    replay_data = soup.find('script', {'class': 'log'})
    #print("Line 11", replay_data)  # None
    if replay_data is None:
        raise ValueError('Replay data not found on page')

    # Parse replay data and create nested array
    data_lines = replay_data.text.split('\n')
    players = {'p1': None, 'p2': None}
    pokemon = {'p1': [], 'p2': []}
    kos = {'p1': [], 'p2': []}
    fainted = {'p1': [], 'p2': []}
    for line in data_lines:
        if line.startswith('|player|p1|'):
            players['p1'] = line.split('|')[3]
        elif line.startswith('|player|p2|'):
            players['p2'] = line.split('|')[3]
        elif line.startswith('|poke|p1|'):
            pokemon['p1'].append(line.split('|')[2])
        elif line.startswith('|poke|p2|'):
            pokemon['p2'].append(line.split('|')[2])
        elif line.startswith('|faint|p1|'):
            fainted['p1'].append(line.split('|')[3])
        elif line.startswith('|faint|p2|'):
            fainted['p2'].append(line.split('|')[3])
        elif line.startswith('|-damage|p1|'):
            if line.split('|')[4] == '0 fnt':
                kos['p2'].append(line.split('|')[2])
        elif line.startswith('|-damage|p2|'):
            if line.split('|')[4] == '0 fnt':
                kos['p1'].append(line.split('|')[2])

    # Create nested array
    result = []
    result.append([players['p1']] + pokemon['p1'] + kos['p1'] + fainted['p1'])
    result.append([players['p2']] + pokemon['p2'] + kos['p2'] + fainted['p2'])
    print(result)
    return result

url = 'https://replay.pokemonshowdown.com/gen7ou-1807806725'
result = analyze_replay(url)
print(result)
