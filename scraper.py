import requests
import time
import pandas as pd
import json
from datetime import date, datetime, timedelta
from database import create_database, insert_event, save, close
import sqlite3

# Get last date from database
def get_last_date_from_database():
    conn = sqlite3.connect("data/sports_events_test.db")
    cursor = conn.cursor()
    query = "SELECT event_date FROM events WHERE winner IS NULL ORDER BY event_date ASC LIMIT 1"
    cursor.execute(query)
    last_date = cursor.fetchone()[0]
    if last_date:
        print(f"Last date is {last_date}")
        return last_date
    else:
        print("No events found in the database.")
        return False
    conn.close()
    

league_id = "4416"
season = "2026"
last_date = get_last_date_from_database()

# Create the start date of the API call 
if last_date:
    start_date = datetime.strptime(last_date, "%Y-%m-%d").date()
else:
    start_date = date(date.today().year, 3, 1)

# Add 7 days to the end date
end_date = date.today() + timedelta(days=7)

current_date = start_date
last_request = 0
all_events = []

# loop through dates while current date is less than end date
def pull_data_from_api():
    global current_date
    while current_date <= end_date:
        
        date_str = current_date.strftime("%Y-%m-%d")

        url = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={date_str}&l={league_id}"
        
        try:

            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()

            events = data.get("events")
            
            if events:
                print(f"{date_str}: Found {len(events)} events")

                for event in events:
                    home_score = event.get("intHomeScore")
                    away_score = event.get("intAwayScore")

                    if home_score is not None:
                        home_score = int(home_score)

                    if away_score is not None:
                        away_score = int(away_score)

                    winner = None

                    if home_score is not None and away_score is not None:
                        if home_score > away_score:
                            winner = 1 # Home win
                        elif away_score > home_score:
                            winner = 0 # Away win
                        else:
                            winner = 2 # Draw

                    clean_event = {
                        "event_id": event["idEvent"],
                        "season": int(event["strSeason"]),
                        "round": int(event["intRound"]),
                        "event_date": event["dateEvent"],
                        "event_time": event["strTime"],
                        "home_team": event["strHomeTeam"],
                        "away_team": event["strAwayTeam"],
                        "home_score": home_score,
                        "away_score": away_score,
                        "venue": event["strVenue"],
                        "status": event["strStatus"],
                        "winner": winner
                    }
                    insert_event(clean_event) # insert clean event data into database
                
            else:
                print(f"{date_str}: No events")
                
        except requests.exceptions.RequestException as e:
            print(f"{date_str}: Unexpected error - {e}")
        
        # iterate through dates
        current_date += timedelta(days=1)
        # sleep for 2 seconds after API call to prevent rate limiting
        time.sleep(2)
    
    save() # commit changes to database
    close() # close database connection
#print(f"\nTotal events collected: {len(all_events)}")
