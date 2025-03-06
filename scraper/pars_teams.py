import requests
from bs4 import BeautifulSoup

def get_teams(league_id):
    url = f"https://soccer365.ru/competitions/{league_id}/"
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    club_links = soup.select('td a[rel="nofollow"]')

    # Извлечение ID клубов
    club_ids = []
    for link in club_links:
        href = link['href']
        club_id = href.split('/')[-2]  # Берем предпоследний элемент из URL
        club_ids.append((link.text, club_id))
        
    return club_ids