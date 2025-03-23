import requests

api_key = "RGAPI-e402ca78-38eb-4bc5-a38d-6ce9e7b84a36"
game_name = "genji1524"
tag_line = "NA1"
account_url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key={api_key}"

def get_puuid(account_url):
    response = requests.get(account_url)
    if response.status_code == 200:
        return response.json().get("puuid")
    else:
        print(f"Failed to get PUUID: {response.status_code}, {response.text}")
        return None

def get_match_data(puuid, api_key, region="americas"):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching match data: {response.status_code}")
        return None

def get_match_details(match_id, api_key, region="americas"):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching match details: {response.status_code}")
        return None

if __name__ == "__main__":
    # Get PUUID from Riot account
    puuid = get_puuid(account_url)

    if puuid:
        # Get match IDs using PUUID
        match_ids = get_match_data(puuid, api_key)
        
        if match_ids:
            # Fetch match details for each match ID (limit to 5 matches for example)
            for match_id in match_ids[:1]:
                match_details = get_match_details(match_id, api_key)
                if match_details:
                    print(f"Match Details: {match_details}")
        else:
            print("No match data found.")
    else:
        print("PUUID retrieval failed.")
