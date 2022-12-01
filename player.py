from colorama import Style
import stage
from state import State

class Player :
    """class to represent a player"""


    characterL = [[" ","<","o",">"," "],
			      [" "," ","|"," "," "],
			      [" ","_","|"," "," "],
			      [" "," ","|"," "," "],
			      [" "," ","|","\\"," "]]

    characterR = [[" ","<","o",">"," "],
			      [" "," ","|"," "," "],
			      [" "," ","|","_"," "],
			      [" "," ","|"," "," "],
			      [" ","/","|"," "," "]]

    jump = 4

    score_p1 = 0
    score_p2 = 0
    score_board = ["|"," ","1"," ","|"," ","2"," ","|"]

    p1_scored = None
    p2_scored = None

    def __init__(self, character_orientation, pos, color , 
                 move_speed, 
                 attack_speed, attack_range, 
                 block_duration, block_range):
        """constructor

        Args:
            character_orientation (int): 0 if the player is facing left and 1 if he is facing right
            pos (list[list[int]]): list of list of int positon of the two players [[player1], [player2]]
            color (constant: str): the color of the sword
            move_speed (int, optional): player's movement speed.
            attack_speed (int, optional): player's attack speed.
            attack_range (int, optional): player's attack range.
            block_duration (int, optional): player's block duration.
            block_range (int, optional): player's block range.
        """
        self.sword_arrangement = {"attack": [f"{color}_{Style.RESET_ALL}",f"{color}_{Style.RESET_ALL}"],
                                  "block": [f"{color}|{Style.RESET_ALL}",f"{color}|{Style.RESET_ALL}"],
                                  "rest": [f"{color}\\{Style.RESET_ALL}",f"{color}/{Style.RESET_ALL}"]}
        if character_orientation == 0:  # if the player is facing left
            self.character_orientation = Player.characterL
            self.sword = self.sword_arrangement.get("rest")[0]
            self.co_orientation = 0  # if the player is facing left
        elif character_orientation == 1:  # else the player is facing right
            self.character_orientation = Player.characterR
            self.sword = self.sword_arrangement.get("rest")[1]
            self.co_orientation = 1  # else the player is facing right
        self.pos = pos
        self.color = color
        self.state = State.REST
        self.move_speed = move_speed
        self.attack_speed = attack_speed
        self.attack_range = attack_range
        self.block_duration = block_duration
        self.block_range = block_range

    def get_character_orientation(self):
        """get the current character of the character/player

        Returns:
            list[list[str]]: the current orientation of character
        """
        return self.character_orientation

    def set_character_orientation(self, new_orientation):
        """change character/player's orientation

        Args:
            new_orientation (list[list[str]]): new character/player's orientation
        """
        self.character_orientation = new_orientation

    def get_pos(self):
        """get the current position of the character/player

        Returns:
            list[int]: the current position of character
        """
        return self.pos

    def set_pos(self, new_pos):
        """change character/player's position

        Args:
            new_pos (list[int]]): new character/player's position
        """
        if stage.collision(new_pos):
            self.pos = new_pos

    def get_sword(self):
        """get the character that represents the current sword

        Returns:
            str: the current character that represents the sword
        """
        return self.sword

    def set_sword(self, state, orientation):
        """changes the character by which the sword is represented in case of block or rest

        Args:
            state (str): the new state of the sword (block, rest)
            orientation (int): the new orientation of the sword 
        """
        self.co_orientation = orientation
        self.sword = self.sword_arrangement.get(state)[orientation]

    def set_sword2(self, state):
        """changes the character by which the sword is represented in case of attack

        Args:
            state (str): the new state of the sword (attack)
        """
        self.sword = self.sword_arrangement.get(state)[self.co_orientation]

    def rest(self):
        """changes the character by which the sword is represented in case of rest
        """
        self.sword = self.sword_arrangement.get("rest")[self.co_orientation]

    def move_right(self, deplacement=1):
        """moves the player to the right changing the current position and change the sword state to rest

        Args:
            deplacement (int, optional): number of cells moved to the right in case of jump . Defaults to 1.

        Returns:
            list[int]: the player's new position
        """
        self.set_sword("rest", 1)
        return [self.pos[0], self.pos[1] + deplacement]

    def move_left(self, deplacement=1):
        """moves the player to the left changing the current position and change the sword state to rest

        Args:
            deplacement (int, optional): number of cells moved to the left in case of jump. Defaults to 1.

        Returns:
            list[int]: the player's new position
        """
        self.set_sword("rest", 0)
        return [self.pos[0], self.pos[1] - deplacement]

    def move_jump(self, orientation):
        """moves the player to the top changing the current position and change the sword state to rest

        Args:
            orientation (int): the new orientation of the sword

        Returns:
            list[int]: the player's new position
        """
        self.set_sword("rest", orientation)
        return [self.pos[0] - 2, self.pos[1]]

    def move_fall(self):
        """moves the player to the bottom changing the current position and change the sword state to rest

        Returns:
            list[int]: the player's new position 
        """
        return [self.pos[0] + 2, self.pos[1]]

