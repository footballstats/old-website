from requests import get
from bs4 import BeautifulSoup
import json


class scrape_table:

    def __init__(self,index):
        request = get('https://en.wikipedia.org/wiki/2018%E2%80%9319_Premier_League')
        soup = BeautifulSoup(request.text,'html.parser')

        self.table = soup.find_all('table', class_='wikitable')[index]
        self.players = self.table.find_all('tr')[1:]

    
    def remove(self, s):
        s = s.strip()
        s = s.strip('\n')
        return s


    def is_int(self, string):
        try:
            int(string)
            return True
        except:
            return False


    def get_list(self):
        data = []

        for player in self.players:
            stats = player.find_all('td')
            stats = [self.remove(i.text) for i in stats]
            try:
                img = player.find_all('img')[0]
            except IndexError:
                break
            stats.append(img['alt'])
            stats.append(img['src'])
            data.append(stats)
            
            
        for i in data:
            if self.is_int(i[0]):
                del i[0]
            if self.is_int(i[2]):
                goals = i[2]
            else:
                i.insert(2,int(goals))
                
        return data


    def get_dict(self):
        x = self.get_list()
        return {i[0]: (i[1],i[2],i[3],i[4]) for i in x}


goals = scrape_table(5)
assists = scrape_table(7)
goals_assists = [goals.get_dict(), assists.get_dict()]

with open('epl.json', 'w') as f:
    json.dump(goals_assists, f, indent=2)

print('Complete')
input()