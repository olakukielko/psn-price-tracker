import requests
from bs4 import BeautifulSoup
import os

filename = 'track_games.txt'
#[TODO] update game prices as soon as program launches

def main():
    game_dict = read_from_file(filename)
    print_current_tracking(game_dict)
    view_menu(game_dict)

def view_menu(game_dict):
    query = ""
    while True:
        query = input("\nType 'track' + game name to start tracking, 'remove' to stop tracking, \n'view' to view current tracked games, 'q' to quit"+'\n\n')
        query = query.split(" ")
        if query[0] == "track":
            query_search(query[1], game_dict)
        elif query[0] =="remove":
            remove_tracking(game_dict)
        elif query[0] =="view":
            print_current_tracking(game_dict)
        elif query[0] == "q":
            exit()

def print_current_tracking(games):
    print("Currently tracked games:\n")
    for key in games:
        print(str(key) + ': ' + str(games[key]))
    print("\n")

def remove_tracking(games):
    temp_dict = {}
    count = 1
    for game in games:
        print("("+ str(count) + ") "+ str(game) + ': ' + str(games[game]))
        temp_dict[str(count)] = game
        count +=1
    response = input("Type the number of the game you want to remove")
    games.pop(temp_dict[response], None)
    save_to_file(games)

def query_search(query, game_dict):
    url1 = "https://store.playstation.com/en-us/search/"
    url2 = "?emcid=se-pi-147509"
    #query = "the sims 4"
    a = query
    to_url = ""
    query_format = a.replace(" ", "%20")
    URL = url1 + query_format + url2
    game_titles = []
    game_prices = []

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    bucket_div = soup.find("div", {"class": "bucket-row__container"})
    aa = list(soup.find_all("div", {"class": "grid-cell__title"}))
    bb = list(soup.find_all("h3", {"class": "price-display__price"}))
    for x in range(len(aa)):
        print('('+str(x+1)+') '+ aa[x].get_text().strip() + '\n'+ 'Price: '+ bb[x].get_text().strip() + '\n')
    response = int(input("Type the name of the game to start tracking. "))
    game_dict[aa[response-1].get_text().strip()] = bb[response-1].get_text().strip()
    save_to_file(game_dict)
    view_menu(game_dict)

def read_from_file(filename):
    game_dict = {}
    if os.stat(filename).st_size != 0:
        f = open(filename, "r")
        title = ""
        price = ""
        for line in f:
            if '[game_title]' in line:
                title = line[13:-1]
            elif '[game_price]' in line:
                price = line[13:-1]
            game_dict[title] = price
    return game_dict

def save_to_file(game_dict):
    f = open(filename, "w")
    for key in game_dict:
        f.write("[game_title] "+ str(key) + "\n[game_price] "+ str(game_dict[key])+"\n")

if __name__ == "__main__":
    main()