from state import State
import os 
from colorama import Fore

def scene_content(file_name):
    """retrieves the line contained in the file for the scene

    Args:
        file_name (str): the name of the file with extension .ffscene

    Returns:
        str: the string contained in the file 
    """
    content = ""
    tmp = file_name.split(".")
    extension =  tmp[-1]
    if extension == "ffscene":
        with open(file_name) as my_file:
            content = my_file.readline()
    return content

def game_attribut(file_name):
    """retrieves the lines contained in the file for the attributs

    Args:
        file_name (str): the name of the file with extension .txt

    Returns:
        list[str]: a list of all attributes and their values
    """
    
    list_content = []
    tmp = file_name.split(".")
    extension = tmp[-1]
    if extension == "txt":
        with open(file_name, "r") as my_file:
            content = my_file.readlines()
            for line in content:
                line = line.strip()
                list_content.append(line)
    return list_content

def show_menu():
    """print the menu"""
    print("\033[%d;%dH" % (1, 1))  # reposition the cursor
    menu = [["-------------------MENU------------------"],
            ["                 Controls                "],
            [" mouvements   player1:     player2:      "],
            [" move left    - q          - left arrow  "],
            [" move right   - d          - right arrow "],
            [" jump left    - a          - l           "],
            [" jump right   - e          - m           "],
            [" attack       - z          - o           "],
            [" block        - s          - p           "],
            ["                                         "],
            ["- f load new scene - g save current scene"],
            ["- v quit the game  - b resume the game   "],]
    
    for i in menu:
        print(i)

def clear_terminal():
    """clears everything on the terminal """
    if os.name == "nt":  # if on windows
        os.system("cls")
    elif os.name == "posix":  # if on  linux
        os.system("clear")

def attribut(list_content):
    """adds all necessary attributes to a dictionary

    Args:
        list_content (str): a list of all attributes and their values

    Returns:
        dict: contains all attributes as keys and their values
    """
    dict_attribut = {}
    for elem in list_content:
        tmp = elem.split(":")
        if tmp[0] == "" or tmp[1] == "":
            continue
        if tmp[0] != "file":
            dict_attribut[tmp[0]] = int(tmp[1])
        else:
            dict_attribut[tmp[0]] = tmp[1]
    return dict_attribut

def look_enemy(attacker, player):
    """Check if the attacking player is facing the second player

    Args:
        attacker (Player): attacking player
        player (Player): the second player

    Returns:
        bool: True if the attacking player is facing the second player, otherwise False
    """
    if ((attacker.get_pos()[1] < player.get_pos()[1] and attacker.co_orientation == 1)  # if the attacking player is on the left of the second player and he is facing right
        or (attacker.get_pos()[1] > player.get_pos()[1] and attacker.co_orientation == 0)):  # or if the attacking player is on the right of the second player and he is facing left
        return True
    return False

def in_range(attacker, player):
    """Checks if the attacking player is in range to hit the second player

    Args:
        attacker (Player): attacking player
        player (Player): the second player

    Returns:
        bool: True if the attacking player is in range, otherwise False
    """
    if ((attacker.co_orientation == 0 and attacker.get_pos()[1] - player.get_pos()[1] <= attacker.attack_range + 4)  # if the second player is located on the right and is in attack range
        or (attacker.co_orientation == 1 and player.get_pos()[1] - attacker.get_pos()[1] <= attacker.attack_range + 4)):  # or if the second player is located on the left and is in attack range
        return True
    return False

def face_to_face(player1, player2):
    """Check if both players are facing each other

    Args:
        player1 (Player): first player
        player2 (Player): second player

    Returns:
        bool: True is they are facing each other, otherwise False
    """
    if ((player1.co_orientation == 0 and player2.co_orientation == 1)  # if the first player looks to the right and the second to the left 
        or (player1.co_orientation == 1 and player2.co_orientation == 0)):  # or if the first player looks to the right and the second to the left
        return True
    return False

def attack_can_touch(attacker, player):
    """Checks if the attack can hit/deal damage to the second player 

    Args:
        attacker (Player): attacking player
        player (Player): the second player

    Returns:
        bool: True if the second player can take damage, otherwise False
    """
    if look_enemy(attacker, player) and in_range(attacker, player):
        return True
    return False

def is_blocked(attacker, defender):
    """Checks if the defender can block the attack

    Args:
        attacker (Player): attacking player
        defender (Player): defending player

    Returns:
        bool: True if the attack can be blocked, otherwise False 
    """
    if defender.state == State.BLOCK or defender.state == State.BLOCKEND:
        if ((defender.co_orientation == 0 and defender.get_pos()[1] - attacker.get_pos()[1] <= defender.block_range + 4)  # if the defending player is looking left and can block the attack
        or (defender.co_orientation == 1 and attacker.get_pos()[1] - defender.get_pos()[1] <= defender.block_range + 4)):  # or if the deffending player is looking right and can block the attack
            return True
    return False

def create_players(attributs):
    """create both player

    Args:
        attributs (dict): contains all the attributes of each player

    Returns:
        Player: list of the 2 players
    """
    import stage
    from player import Player
    
    if stage.p1_before_p2:
        orientationp1 = 1  # player 1 is facing right
        orientationp2 = 0  # player 2 is facing left
    else:
        orientationp1 = 0
        orientationp2 = 1
    
    p1 = Player(orientationp1 ,stage.start_pos_p1, Fore.GREEN, attributs.get("movement_speed_p1"), 
                         attributs.get("attacking_speed_p1"), attributs.get("attacking_range_p1"), 
                         attributs.get("blocking_time_p1"), attributs.get("defending_range_p1"))
    p2 = Player(orientationp2 ,stage.start_pos_p2, Fore.RED, attributs.get("movement_speed_p2"), 
                         attributs.get("attacking_speed_p2"), attributs.get("attacking_range_p2"), 
                         attributs.get("blocking_time_p2"), attributs.get("defending_range_p2"))
    return [p1, p2]