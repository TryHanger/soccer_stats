import requests
from bs4 import BeautifulSoup
from database.save_league import save_unknown_league
from fuzzywuzzy import process


def get_league_id_by_name(league_name, leagues_dict, threshold=80):
    league_mapping = {name: league['id'] for league in leagues_dict for name in league['name']}

    matches = process.extractOne(league_name, league_mapping.keys())
    
    if matches and matches[1] >= threshold:
        matched_name = matches[0]
        league_id = league_mapping[matched_name]
        print(f"✅ Найдена лига: '{matched_name}' (ID: {league_id}) с совпадением {matches[1]}%")
        print(league_id)
        return league_id
    else:
        print(f"⚠️ Лига '{league_name}' не найдена в словаре. Создаем новую лигу...")
        new_league_id = save_unknown_league(league_name)
        print(new_league_id)
        return new_league_id


def parse_league_info(league_id):
    url = f"https://soccer365.ru/competitions/{league_id}/"
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, "html.parser")

    if league_id == 903:  # ID Суперкубка
        
        # Заполняем пустыми значениями
        data = {
            "url_id": league_id,
            "league_name": "Суперкубок УЕФА",
            "country": None,
            "start_date": None,
            "end_date": None,
            "matches_played": None,
            "total_matches": None,
        }
    else:
        league_name = soup.find("h1", class_="profile_info_title").text.strip()
        try:
            country = soup.find("td", class_="params_key", string="Страна").find_next("td").span.text.strip()
        except AttributeError:
            country = None
        date_range = soup.find("td", class_="params_key", string="Дата").find_next("td").text.strip()
        start_date, end_date = date_range.split(" - ")
        matches_range = soup.find("td", class_="params_key", string="Сыграно").find_next("td").text.strip()
        matches_played, total_matches = matches_range.split(" из ")

        data = {
            "url_id": league_id,
            "league_name": league_name,
            "country": country,
            "start_date": start_date,
            "end_date": end_date,
            "matches_played": matches_played,
            "total_matches": total_matches,
        }

    return data

