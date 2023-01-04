import pytest

from util import *

def test_simplify():
    assert simplify("Yu-Gi-Oh! Forbidden Memories") == "YUGIOHFORBIDDENMEMORIES"
    assert simplify("Warcraft II: The Dark Saga") == "WARCRAFT2THEDARKSAGA"
    assert simplify("Spyro 2: Ripto's Rage! | Spyro 2: Gateway to Glimmer") == "SPYRO2RIPTOSRAGE" 
    assert simplify("Final Fantasy VIII") == "FINALFANTASY8" 

def test_create_game_by_element_achievement():
    URL_ACHIEVEMENTS = "https://retroachievements.org/gameList.php?c=21"
    QUERY_SELECTOR_ACHIEVEMENTS = ".table-wrapper td.w-full a"

    result =  get_elements_by_url(URL_ACHIEVEMENTS, QUERY_SELECTOR_ACHIEVEMENTS)[54]
    game = create_game_by_element(result)

    game_mock = Game("God of War", "GODOFWAR", "https://retroachievements.org/game/2782")
    assert game == game_mock

def test_create_game_by_element_archive():
    URL_ARCHIVES = "https://archive.org/download/redumpSonyPlaystation2UsaGames2018Aug01/"
    QUERY_SELECTOR_ARCHIVES = ".directory-listing-table a"

    result =  get_elements_by_url(URL_ARCHIVES, QUERY_SELECTOR_ARCHIVES)[150]
    game = create_game_by_element(result, URL_ARCHIVES)

    game_mock = Game("'Armored Core 2 (USA).7z'", simplify("'Armored Core 2 (USA).7z'"), "https://archive.org/download/redumpSonyPlaystation2UsaGames2018Aug01/Armored%20Core%202%20%28USA%29.7z")
    assert game == game_mock


def test_get_miss_and_match():
    URL_ACHIEVEMENTS = "https://retroachievements.org/gameList.php?c=21/"
    QUERY_SELECTOR_ACHIEVEMENTS = ".table-wrapper td.w-full a"


    URL_ARCHIVES_ARRAY = ['https://archive.org/download/redump.psx', 'https://archive.org/download/redump.psx.p2', 'https://archive.org/download/redump.psx.p3', 'https://archive.org/download/redump.psx.p4']
    QUERY_SELECTOR_ARCHIVES = ".directory-listing-table a"

    response_achievements = get_elements_by_url(URL_ACHIEVEMENTS, QUERY_SELECTOR_ACHIEVEMENTS)
    response_archives     = get_elements_by_array(URL_ARCHIVES_ARRAY, QUERY_SELECTOR_ARCHIVES)

 

    testing = get_miss_and_match(achievements_game_list, archives_game_list)

    print(testing)


