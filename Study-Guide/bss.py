import requests
import bs4

def getname():
    game_id = 1000
    url = 'https://www.boardgamegeek.com/xmlapi/boardgame/' + str(game_id)
    result = requests.get(url)
    soup = bs4.BeautifulSoup(result.text, features='lxml')

    return soup.find('maxplayers').text

def id_main():
    game_id = 1000
    url = 'https://www.boardgamegeek.com/xmlapi/boardgame/' + str(game_id)
    result = requests.get(url)
    soup = bs4.BeautifulSoup(result.text, features='lxml')

    return soup

# The function that will take the number and make something out of it 
def display_id():
    id_1 = id_main()
    name = id_1.find('name').text
    min = id_1.find('minplayers').text
    max = id_1.find('maxplayers').text
    age = id_1.find('age').text
    
    return 'The name is {} with the max players of {} and the min players of {} age reccomended is {}'.format(
            name, max, min, age
    )