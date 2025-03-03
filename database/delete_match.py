import sqlite3
from config import DB_PATH

def delete_oldest_match(match_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Удаление матча по ID
        cursor.execute("DELETE FROM matches WHERE id_match = ?", (match_id,))
        
        # Сохраняем изменения
        conn.commit()
        print(f"Матч {match_id} удалён из базы данных")

    except sqlite3.Error as e:
        print(f"Ошибка при удалении матча {match_id}: {e}")

    finally:
        conn.close()