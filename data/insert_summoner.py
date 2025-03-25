import pymysql
import sys
sys.path.append('riot_api')
from riot_api import get_puuid

# Database connection settings
DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PASSWORD = 'Soccer152431!'  # Replace with your actual password
DB_NAME = 'baronclash'

def insert_summoner(game_name, tag_line):
    # Fetch PUUID from Riot API
    puuid = get_puuid(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key=RGAPI-e402ca78-38eb-4bc5-a38d-6ce9e7b84a36")
    if not puuid:
        print("Failed to retrieve PUUID.")
        return
    
    # Connect to MySQL database
    try:
        connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        cursor = connection.cursor()
        
        # Insert summoner data
        insert_query = """
        INSERT INTO summoners (summoner_name, puuid)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE summoner_name=VALUES(summoner_name)
        """
        cursor.execute(insert_query, (game_name, puuid))
        connection.commit()
        print(f"Summoner '{game_name}#{tag_line}' inserted/updated successfully.")
    
    except pymysql.MySQLError as e:
        print(f"MySQL Error: {e}")
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    game_name = input("Enter game name: ")
    tag_line = input("Enter tag line: ")
    insert_summoner(game_name, tag_line)
