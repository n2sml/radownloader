import re
from typing import List
import requests
from bs4 import BeautifulSoup

class Game:
    """ Classe que modela um jogo.
    """
    def __init__(self, name, keyword, url):
        self.name = name
        self.keyword = keyword
        self.url = url

    name: str
    keyword: str
    url: str

def simplify(text: str, main_region: str = "USA", extension: str = "ZIP"):
    """ Retorna a String simplificada, sem caracteres especiais e informações dispensáveis.
    Args:
        text (str): O nome do jogo, contendo informações de região, versão, disco, idiomas...
        main_region (str, optional): A região do jogo a ser filtrada. Defaults to "USA".
        extension (str, optional): A extensão do arquivo do jogo. Defaults to "ZIP".
    Returns:
        str: O nome do jogo simplificado
    """

    REGEX_VERSION = r"\(V([0-9].[0-9])\w+\)"
    REGEX_REGIONS = r"\(([A-Z][A-Z],)+([A-Z][A-Z])\)"
    REGEX_DISCS = r"\(DISC +[0-9]\)"

    RESERVED_NAMES = ["WALT", "DISNEYS", "DISNEY", "PIXAR"]
    RESERVED_CHARS = ["|", ":", "&", ",", ".", "/",
                      "'", "-", "!", "(", ")", "[", "]", " "]

    EMPTY = ""

    # Remover nome alternativo (Exemplo: Digimon World 2003 | Digimon World 3)
    text = text.split("|")[0]

    # Trazer artigo para início do nome (Exemplo: Bugs Life, A)
    if len(text.split(",")) > 1:
        text = text.split(",")[1] + text.split(",")[0]

    # Substituindo algarismos romanos por números (Exemplo: Final Fantasy VIII)
    text = text.replace("IX",   "9")
    text = text.replace("VIII", "8")
    text = text.replace("VII",  "7")
    text = text.replace("IV",   "4")
    text = text.replace("III",  "3")
    text = text.replace("II",   "2")

    # Aplicando Regex
    # Regex para remover versão (Exemplo: )
    text = text.replace(REGEX_VERSION, EMPTY)
    # Regex para remover versão (Exemplo: Vib-Ribbon (Europe) (En,Fr,De,Es,It).zip)
    text = text.replace(REGEX_REGIONS, EMPTY)
    # Regex para remover descrição do disco (Exemplo: Tales of Destiny II (USA) (Disc 1))
    text = text.replace(REGEX_DISCS,   EMPTY)

    # Transformando em maiúsculas
    text = text.upper()

    # Removendo as extensões mais comuns - .zip e .7z
    text = text.replace("ZIP", EMPTY)
    text = text.replace("7Z",  EMPTY)

    # Substituindo "2nd" por "Second" (Exemplo: Vigilante 8: 2nd Offense)
    text = text.replace("2ND", "SECOND")

    # Permitindo apenas a versão com a região selecionada
    text = text.replace(main_region, EMPTY)

    # Removendo a extensão do arquivo
    text = text.replace(extension, EMPTY)

    # Removendo palavras reservadas (Exemplo: Disney's Hercules Action Game)
    for value in RESERVED_NAMES:
        text = text.replace(value, EMPTY)

    # Removendo caracteres especiais (Exemplo: King of Fighters '98, The: Dream Match Never Ends)
    for value in RESERVED_CHARS:
        text = text.replace(value, EMPTY)

    return text

def filter_invalid_links(links: List) -> List :
    """Filtra quais dos itens são links válidos

    Args:
        links (List): Uma lista com todos os links

    Returns:
        List: Uma lista apenas com itens válidos
    """
    valid_links = []
    
    for item in links:
        if is_valid_name(item.text): valid_links.append(item)

    return valid_links   

def is_valid_name(name: str) -> bool:
    """Verifica se o nome de um jogo é válido.

    Args:
        name (str): Nome do jogo

    Returns:
        bool: Se o jogo é válido
    """
    REGEX_HOMEBREW = "~\w+~"
    REGEX_SUBSET   = "\[([a-zA-Z \-]+)\]"
    URL_CONTENTS   = "View Contents"
    URL_DIRECTORY  = " Go to parent directory"

    match_homebrew  = len(re.findall(REGEX_HOMEBREW, name)) > 0
    match_subset    = len(re.findall(REGEX_SUBSET, name)) > 0
    match_contents  = URL_CONTENTS in name
    match_directory = URL_DIRECTORY in name

    if not match_homebrew and not match_subset and not match_contents and not match_directory:
        return True
    else: return False


def get_elements_by_url(html_url: str, query_selector: str) -> List[str]:
    """ Retorna os elementos html a partir de uma requisição.
    Args:
        html_url (str): URL da página dos jogos
        query_selector (str): Query Selector que serve de filtro para retornar apenas os nomes
    Returns:
        List[str]: Uma lista contendo os nomes dos jogos
    """
    
    html = requests.get(html_url).text
    soup = BeautifulSoup(html, 'html.parser')

    return soup.select(query_selector)
   
def get_elements_by_array(html_url_array: List[str], query_selector: str) -> List[str]:
    """ Retorna os elementos html a partir de série de requisições
    Args:
        html_url_array (List[str]): Lista contendo URLs das páginas dos jogos
        query_selector (str): Query Selector que serve de filtro para retornar apenas os nomes

    Returns:
        List[str]: Uma lista contendo os nomes dos jogos
    """

    list = []
    for value in html_url_array:
        list.append(get_elements_by_url(value, query_selector))

    return list

def create_game_by_element(element, url_domain="") -> Game:
    """ Cria um objeto do tipo Game a partir de um elemento HTML.
    Args:
        element (): Elemento HTML.
        url_domain (str, optional): Domínio da URL.

    Returns:
        Game: Um objeto do tipo Game.
    """
    name    = element.text
    keyword = simplify(element.text)
    url     = url_domain + element['href']

    return Game(name, keyword, url)   

def convert_elements_to_games(elements: List, url_domain: str='') -> List[Game]: 
    elements = filter_invalid_links(elements)
    return [create_game_by_element(element, url_domain) for element in elements]


def get_miss_and_match(achievements_game_list: List[Game], archives_game_list: List[Game]):
    miss_list  = []
    match_list = []
    found = False

    for achievementGame in achievements_game_list:
        found = False
        for j, archiveGame in enumerate(archives_game_list):
            if not found:
                if j == len(archives_game_list) - 1 and not found:
                    print("Jogo não encontrado: " + achievementGame.keyword)       
                    miss_list.append(achievementGame)
                if achievementGame.keyword == archiveGame.keyword:
                    found = True
                    print("Jogo encontrado: " + archiveGame.keyword)
                    match_list.append(archiveGame)

    print("complete")