from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from pokemon import Pokemon

base_url = 'https://pokemondb.net'
pokemon_list = []


# The pokémon's japanese name is in the 8th position of a th list. So, in some cases there's no japanese name yet (Gen
# VII pokémon) and is set to be 'None'.
def get_japanese_name(tr_list):
    return tr_list[-1].td.text if len(tr_list) > 7 else 'None'


# Each pokémon can have 1 or 2 types, so it's necessary to validate it.
def get_pokemon_types(a_list):
    types = a_list[0].text
    if len(a_list) > 1:
        types = types + ', ' + a_list[1].text
    return types


# Each pokémon can have 1 or 2 abilities and 0 or 1 hidden abilities.
def get_pokemon_abilities(a_list):
    abilities = ''
    for a in a_list:
        abilities = abilities + a.text + ', '
    return abilities[:-2]


# Each pokémon can have gender or not.
def get_pokemon_gender_ratio(span_list):
    gender = 'Genderless'
    if len(span_list) == 2:
        gender = span_list[0].text + ', ' + span_list[1].text
    return gender


# Each pokémon can have 1 or 2 egg groups, but I don't know why in some cases they don't have any.
def get_pokemon_egg_groups(a_list):
    egg_groups = 'Undiscovered'
    if len(a_list) > 0:
        egg_groups = a_list[0].text
        egg_groups = egg_groups + (', ' + a_list[1].text if len(a_list) > 1 else '')
    return egg_groups


# Makes a request to each pokémon url and then parses they information.
def get_pokemon(pokemon_url):
    request = Request(pokemon_url, headers={'User-Agent': 'Mozilla/52.0'})
    soup_object = BeautifulSoup(urlopen(request).read(), 'html.parser').body.article
    pokemon_info_div = soup_object.contents[11].contents[3].contents[1].contents[1]
    pokedex_data_tr_list = pokemon_info_div.contents[3].contents[3].find_all('tr')
    training_and_breeding_div_list = pokemon_info_div.contents[5].contents[1].find_all('div')
    training_div_tr_list = training_and_breeding_div_list[0].find_all('tr')
    breeding_div_tr_list = training_and_breeding_div_list[1].find_all('tr')

    pokemon_name = soup_object.contents[1].text
    pokemon_japanese_name = get_japanese_name(pokedex_data_tr_list)
    pokemon_species = pokedex_data_tr_list[2].td.text
    pokemon_pokedex_number = pokedex_data_tr_list[0].strong.text
    pokemon_image_path = pokemon_info_div.contents[1].img['src']
    pokemon_types = get_pokemon_types(pokedex_data_tr_list[1].td.find_all('a'))
    pokemon_abilities = get_pokemon_abilities(pokedex_data_tr_list[5].td.find_all('a'))
    pokemon_gender_ratio = get_pokemon_gender_ratio(breeding_div_tr_list[1].td.find_all('span'))
    pokemon_catch_rate = training_div_tr_list[1].td.text
    pokemon_egg_groups = get_pokemon_egg_groups(breeding_div_tr_list[0].td.find_all('a'))
    # For some reason this string is accompanied by \t and \n.
    pokemon_hatch_time = breeding_div_tr_list[2].td.text.replace("\t", "").replace("\n", "")
    pokemon_height = pokedex_data_tr_list[3].td.text
    pokemon_weight = pokedex_data_tr_list[4].td.text
    pokemon_base_happiness = training_div_tr_list[2].td.text
    pokemon_leveling_rate = training_div_tr_list[4].td.text
    return Pokemon(pokemon_name, pokemon_japanese_name, pokemon_species, pokemon_pokedex_number, pokemon_image_path,
                   pokemon_types, pokemon_abilities, pokemon_gender_ratio, pokemon_catch_rate, pokemon_egg_groups,
                   pokemon_hatch_time, pokemon_height, pokemon_weight, pokemon_base_happiness, pokemon_leveling_rate)


# This is the Web Crawler, it gets the url of each pokémon.
def iterate(list_url):
    cont = 1
    request = Request(list_url, headers={'User-Agent': 'Mozilla/52.0'})
    soup_object = BeautifulSoup(urlopen(request).read(), 'html.parser').body.article.contents[9]
    pokemon_span_list = soup_object.find_all('span')
    for pokemon_span in pokemon_span_list:
        pokemon_list.append(get_pokemon(base_url + pokemon_span.a['href']))
        print('#' + str(cont) + ' Obtained')
        cont += 1


# Writes the pokémon list in a new archive.
def write_file():
    file = open('pokemondb.txt', 'w', encoding='utf-8')
    for pokemon in pokemon_list:
        print(pokemon.to_string())
        file.write(pokemon.to_string() + "\n")
    file.close()


def main():
    iterate(base_url + '/pokedex/national')
    write_file()

main()
