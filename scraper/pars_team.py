import requests
from bs4 import BeautifulSoup
from config import HEADERS

'''
Изменить количество матчей, которые мы хотим получить
Возможно сделать параметром функции
'''
def get_team_matches(team_id):
    url = f"https://soccer365.ru/clubs/{team_id}/&tab=result_last"
    response = requests.get(url, headers=HEADERS)
        
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return []
  
    soup = BeautifulSoup(response.text, "html.parser")
    
    match_links = []
    
    matches = soup.find_all("div", class_="game_block")
    
    for match in matches:
        link = match.find("a", href=True)
        if link:
            match_links.append(f"https://soccer365.ru{link['href']}")
        if len(match_links) >= 20:
            break
    
    return match_links