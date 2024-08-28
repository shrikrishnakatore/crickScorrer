import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
import time

def get_live_matches():
    url = "https://www.espncricinfo.com/live-cricket-score"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    matches = soup.find_all('div', class_='card content-block league-scores-container')
    
    live_matches = []
    for match in matches:
        title = match.find('h2', class_='title').text.strip()
        teams = match.find_all('p', class_='name')
        if len(teams) == 2:
            match_info = f"{title}: {teams[0].text.strip()} vs {teams[1].text.strip()}"
            live_matches.append(match_info)
    
    return live_matches

def get_match_score(match_url):
    response = requests.get(match_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    score = soup.find('div', class_='score').text.strip()
    return score

def main():
    live_matches = get_live_matches()
    
    if not live_matches:
        print("No live matches found.")
        return

    print("Available live matches:")
    for i, match in enumerate(live_matches, 1):
        print(f"{i}. {match}")

    choice = int(input("Enter the number of the match you want to follow: ")) - 1
    
    if choice < 0 or choice >= len(live_matches):
        print("Invalid choice.")
        return

    selected_match = live_matches[choice]
    match_url = f"https://www.espncricinfo.com/live-cricket-score"

    toaster = ToastNotifier()
    
    while True:
        score = get_match_score(match_url)
        toaster.show_toast("Live Cricket Score", f"{selected_match}\n{score}", duration=10)
        time.sleep(60)  # Wait for 1 minute before the next update

if __name__ == "__main__":
    main()
