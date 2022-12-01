from colorama import Fore, Style
from player import Player
import utils
import os


start_pos_p1 = []
start_pos_p2 = []

line = 15
coll = 0

displayed_scene = []  # print scene on the terminal
base_scene = []  # scene without the players

p1_before_p2 = True

list_collision = []

tab_sword_position = [f"{Fore.GREEN}_{Style.RESET_ALL}",
					  f"{Fore.RED}_{Style.RESET_ALL}"]

file_content = ""

def ground(content):
	"""create the ground of the scene

	Args:
		content (str): content of .ffscene files

	Returns:
		list[str]: _description_
	"""
	grd = []
	for elem in content:
		if elem == "_":
			grd.append("#")
		elif elem == "1":
			for i in range(5):
				grd.append("#")
		elif elem == "2":
			for i in range(5):
				grd.append("#")
		elif elem == "x":
			grd.append("#")
	return grd

def pos_players(content):
	"""returns players position

	Args:
		content (str): content of .ffscene files

	Returns:
		list[list[int]]: the list of players' positions
	"""
	global start_pos_p1, start_pos_p2, p1_before_p2
	start_pos = [[],[]]
	start_line = line-6
	start_col = 0
	for elem in content:
		if elem == "1":
			start_pos[0] = [start_line, start_col]  # the coordinate of player top left corner
			start_pos_p1 = [start_line, start_col]
			start_col += 5
			p1_before_p2 = False
		elif elem == "2":
			start_pos[1] = [start_line, start_col]
			start_pos_p2 = [start_line, start_col]
			start_col += 5
			p1_before_p2 = True
		else:
			start_col += 1
	return start_pos

def empty_scene(col, grd):
	"""create the scene with the floor and the key a pressed to access the menu  

	Args:
		col (int): the collone
		grd (list[str]): the ground

	Returns:
		list[list[str]]: the scene with the floor and the key a pressed to access the menu
	"""
	menu = ["w",":"," ","o","p","e","n"," ","m","e","n","u"]
	scene = []
	for li in range(line-1):
		scene.append([" "]*col)
	scene.append(grd)
	for ind in range(len(menu)):
		scene[0][ind] = menu[ind]
	return scene

def pos_obstacle(content):
	"""recovers the positions of possible obstacles

	Args:
		content (str): content of .ffscene files

	Returns:
		list[list[itn]]: list of obstacle positions
	"""
	global list_collision, coll
	list_collision = []
	pos = []
	start_lin = line-3
	start_col = 0
	for char in content:
		if char == "_":
			start_col += 1
		elif char == "x":
			pos.append([start_lin, start_col])
			list_collision.append([start_lin, start_col])
			start_col += 1
		elif char == "1" or char == "2":
			start_col += 5
	coll = start_col
	return pos

def add_obstacle(scene, pos):
	"""adds obstacles to the scene

	Args:
		scene (list[list[str]]): the scene
		pos (list[list[int]]): obstacle positions
	"""
	for elem in pos:
		scene[line-3][elem[1]] = "X"
		scene[line-2][elem[1]] = "X"

def add_score(scene):
	"""adds the score to the scene

	Args:
		scene (list[list[str]]): the scene
	"""
	start_line = line//4
	start_coll = coll//2 - len(Player.score_board)//2
	for char in Player.score_board:
		if char == "1":
			scene[start_line][start_coll] = str(Player.score_p1)
		elif char == "2":
			scene[start_line][start_coll] = str(Player.score_p2)
		else:
			scene[start_line][start_coll] = char
		start_coll +=1

def add_string(scene):
	"""adds the message of the player who scored the point to the scene

	Args:
		scene (list[list[str]]): the scene
	"""
	player = 0
	if Player.p1_scored:
		player = 1
	elif Player.p2_scored:
		player = 2
	string = f"Player {player} score !"
	start_line = line//8
	start_coll = coll//2 - len(string)//2
	for char in string:
		scene[start_line][start_coll] = char
		start_coll +=1

def add_end_string(scene):
	"""adds the message of the player who scored the point to the scene

	Args:
		scene (list[list[str]]): the scene
	"""
	player = 0
	if Player.score_p1 == 3:
		player = 1
	elif Player.score_p2 == 3:
		player = 2
	string = f"Player {player} wins, ending games..."
	start_line = 0
	start_coll = coll//2 - len(string)//2
	for char in string:
		scene[start_line][start_coll] = char
		start_coll +=1 

def add_players(scene, pos, character, sword):
	"""add players to the scene

	Args:
		scene (list[list[str]]): the scene
		pos (list[list[int]]): players positions
		character (list[list[list[str]]]): the players visual without their sword
		sword (list[str]): the list of characters for the sword
	"""
	for player in range(2):
		height = 0
		#add players without their sword
		for lin in range(pos[player][0],pos[player][0]+5):
			length = 0
			for col in range(pos[player][1],pos[player][1] + 5):
				if character[player][height][length] != " ":
					scene[lin][col] = character[player][height][length]
				length += 1
			height += 1

	for player in range(2):
		pos_y = pos[player][0] + 2
		pos_x = pos[player][1]
		
		
		if character[player][2][3] == "_":  # if the player is turned to the right
			if pos_x  < coll - 5 and sword[player] in tab_sword_position:
				if sword[player] == f"{Fore.GREEN}_{Style.RESET_ALL}" or sword[player] == f"{Fore.RED}_{Style.RESET_ALL}":
					scene[pos_y][pos_x + 4] = sword[player]
					scene[pos_y][pos_x + 5] = sword[player]
			else:
				scene[pos_y][pos_x + 4] = sword[player]
		
		elif character[player][2][1] == "_":  # if the player is turned to the left
			if sword[player] in tab_sword_position and pos_x > 0 :
				if sword[player] == f"{Fore.GREEN}_{Style.RESET_ALL}" or sword[player] == f"{Fore.RED}_{Style.RESET_ALL}":
					scene[pos_y][pos_x] = sword[player]
					scene[pos_y][pos_x-1] = sword[player]
			else:
				scene[pos_y][pos_x] = sword[player]

def collision(next_pos):
	"""check collision between players and obstacles

	Args:
		next_pos (list[int]): the list of players' positions in the next frame

	Returns:
		bool: True if collision, otherwise False
	"""
	if next_pos[1] + 1 <= 0 or next_pos[1] + 3 >= coll - 1:
		return False
	for coord in list_collision:
		if next_pos[1] +1 <= coord[1] and next_pos[1]+3 >= coord[1]:
			return False
	return True

def cp(matrix2):
	"""copy a table in the displayed scene

	Args:
		matrix2 (list[list[list[str]]]): the table
	"""
	global displayed_scene
	displayed_scene = []
	for i in range(line):
		displayed_scene.append(matrix2[i].copy())

def display_start_scene(file_name, character, sword):
	"""show the start scene

	Args:
		file_name (str): _description_
		character (list[list[list[str]]]): the players visual without their sword
		sword (list[str]): the list of characters for the sword
	"""
	global displayed_scene, base_scene, file_content
	file_content = utils.scene_content(file_name)
	base_scene = empty_scene(len(file_content)+8, ground(file_content))
	add_obstacle(base_scene, pos_obstacle(file_content))
	add_score(base_scene)
	cp(base_scene)
	add_players(displayed_scene, pos_players(file_content), character, sword)
	display_scene(displayed_scene)

def update_scene_after_scored():
	"""show the scene after a point"""
	add_score(base_scene)
	cp(base_scene)
	add_string(displayed_scene)
	display_scene(displayed_scene)

def update_scene_end():
	"""show the end scene"""
	add_score(base_scene)
	cp(base_scene)
	add_end_string(displayed_scene)
	display_scene(displayed_scene)

def update_scene(new_pos, new_look, new_oriantaion):
	"""show the scene with the players

	Args:
		next_pos (list[int]): the list of players' positions in the next frame
		new_look (list[list[list[str]]]): the players visual without their sword
		new_oriantaion (list[str]): the list of characters for the sword
	"""
	add_score(base_scene)
	cp(base_scene)
	add_players(displayed_scene, new_pos, new_look, new_oriantaion)
	display_scene(displayed_scene)

def display_scene(scene):
	"""show the scene

	Args:
		scene (list[list[str]]): the scene
	"""
	for row in scene:
		print("".join(row))

def save_current_scene(file, player1, player2):
	"""save to a file or a new file .ffscene

	Args:
		file (str): the file to save to
		player1 (Player): player 1
		player2 (Player): player 2
	"""
	tmp = file.split(".")
	extension =  tmp[-1]
	if extension == "ffscene":
		list_saved = []
		list_saved.append(["_"]*(len(file_content)+8))

		list_saved[0][player1.get_pos()[1]+1] = "1"
		list_saved[0][player2.get_pos()[1]+1] = "2"
  
		for elem in list_collision:
			list_saved[0][elem[1]] = "x"
		
		

		if p1_before_p2:
			for i in range(4):
				if player2.get_pos()[1]+2 > len(list_saved[0]) :
					break
				if list_saved[0][player2.get_pos()[1]+2] =="1" or list_saved[0][player2.get_pos()[1]+2] =="x":
					break
				list_saved[0].pop(player2.get_pos()[1]+2)
			for i in range(4):
				if player1.get_pos()[1]+2 > len(list_saved[0]) :
					break
				if list_saved[0][player1.get_pos()[1]+2] =="2" or list_saved[0][player1.get_pos()[1]+2] =="x":
					break
				list_saved[0].pop(player1.get_pos()[1]+2)
		else:
			for i in range(4):
				if player1.get_pos()[1]+2 > len(list_saved[0]) :
					break
				if list_saved[0][player1.get_pos()[1]+2] =="2" or list_saved[0][player1.get_pos()[1]+2] =="x":
					break
				list_saved[0].pop(player1.get_pos()[1]+2)
			for i in range(4):
				if player2.get_pos()[1]+2 > len(list_saved[0]) :
					break
				if list_saved[0][player2.get_pos()[1]+2] =="1" or list_saved[0][player2.get_pos()[1]+2] =="x":
					break
				list_saved[0].pop(player2.get_pos()[1]+2)
    
		my_file = open(file, "w")
		my_file.write("".join(list_saved[0]))
		my_file.close()


def load_new_scene():
	"""loads a new scene contained in a .ffscene file entered with the keyboard

	Returns:
		str: the .ffscene file
	"""
	path = "."
	files = os.listdir(path)
	for file_name in files:
		tmp = file_name.split(".")
		extension =  tmp[-1]
		if extension == "ffscene":
			print(file_name)
	file_name = input("enter a file name and press enter to load the scene: ")
	while file_name not in files:
		file_name = input("enter a file name and press enter to load the scene: ")
	return file_name