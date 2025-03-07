import requests
from bs4 import BeautifulSoup
from database.save_league import get_id_by_url, get_id_by_name
from database.save_league import save_league, save_name_league
from utils.leagues_loader import save_league_json

def save_in_dict(data, leagues_dict):
    new_league = {"id": data["url_id"], "name": data["league_name"], "tier": 1}
    leagues_dict.append(new_league)
    return leagues_dict
    
def find_league_id(league_id, leagues_dict):
    for url_id_league in leagues_dict:
        url_id = url_id_league.get("id")       
        if url_id == league_id:
            try:
                id_in_db = get_id_by_url(league_id)
            except Exception as e:
                print(f"❌ Ошибка при получении id для {league_id}: {e}")            
            if id_in_db:
                return id_in_db, leagues_dict
            else:
                try:
                    data = parse_league_info(league_id)
                    id_in_db = save_league(data)
                    return id_in_db, leagues_dict
                except Exception as e:
                    print(f"❌ Ошибка при сохранении лиги в бд для {league_id}: {e}")
    try:
    # Парсим информацию о лиге
        try:
            data = parse_league_info(league_id)
        except Exception as e:
            print(f"❌ Ошибка при парсинге лиги {league_id}: {e}")
            return None, leagues_dict

        # Сохраняем лигу в базу данных
        try:
            id_in_db = save_league(data)
        except Exception as e:
            print(f"❌ Ошибка при сохранении лиги в БД для {league_id}: {e}")
            id_in_db = None

        # Сохраняем данные в JSON
        try:
            save_league_json(data)
        except Exception as e:
            print(f"❌ Ошибка при сохранении лиги в JSON для {league_id}: {e}")

        # Обновляем словарь с лигами
        try:
            leagues_dict = save_in_dict(data, leagues_dict)
        except Exception as e:
            print(f"❌ Ошибка при сохранении лиги в словарь для {league_id}: {e}")

        # Возвращаем ID и обновлённый словарь
        return id_in_db, leagues_dict

    except Exception as e:
        print(f"❌ Общая ошибка при обработке лиги {league_id}: {e}")
        return None, leagues_dict

def parse_league_info(league_id):
    url = f"https://soccer365.ru/competitions/{league_id}/"
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        # Пробуем найти стандартный заголовок
        league_name_tag = soup.find("h1", class_="profile_info_title")
        league_name = league_name_tag.text.strip() if league_name_tag else None

        # Если стандартное название не найдено — берем из selectbox-label
        if not league_name:
            name_box = soup.find("div", class_="breadcrumb")
            if name_box:
                league_name = name_box.find("span", class_="selectbox-label").text
            
        if not league_name:
            header_box = soup.find("div", class_="block_header")
            if header_box:
                header_title = header_box.find("h2")
                if header_title:
                    full_name = header_title.text.strip()
                    league_name = full_name.split(",")[0].strip()
                    
        # Пытаемся найти страну
        country_tag = soup.find("td", class_="params_key", string="Страна")
        country = country_tag.find_next("td").span.text.strip() if country_tag else None
        
        # Даты
        date_range_tag = soup.find("td", class_="params_key", string="Дата")
        if date_range_tag:
            date_range = date_range_tag.find_next("td").text.strip()
            start_date, end_date = date_range.split(" - ")
        else:
            start_date, end_date = None, None
        
        # Сыгранные матчи
        matches_range_tag = soup.find("td", class_="params_key", string="Сыграно")
        if matches_range_tag:
            matches_range = matches_range_tag.find_next("td").text.strip()
            matches_played, total_matches = matches_range.split(" из ")
        else:
            matches_played, total_matches = None, None

    except Exception as e:
        print(f"⚠️ Ошибка парсинга лиги {league_id}: {e}")
        
        # Если вообще все сломалось, возвращаем минимальные данные
        league_name = f"Неизвестная лига {league_id}"
        country = None
        start_date = None
        end_date = None
        matches_played = None
        total_matches = None

    # Собираем результат
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