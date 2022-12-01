from pynput import keyboard
import colorama
import stage
import utils
from player import Player
from state import State
import time
import threading
import simpleaudio as sa
import cursor


listener = None  # keyboard listener
is_not_created = True  # True if the thread is not created
t1 = None

time_refresh = 10
pas = 1/time_refresh  # frame rate

counter_p1=0  # a counter for the speed of p1
counter_p2=0 

restart = False  # True if restart the scene

end_game = False

p1 = None  # player 1
p2 = None  # player 2

open_menu = False  # True if the menu is opened

save_current_scene = False
load_new_scene =False
load = False

file_name = ""

#sounds effects
walk = "walk.wav"
jp = "jump.wav"
sword_hit = "sword_hit.wav"
sword_swing = "sword_swing.wav"
shield_block = "shield_block.wav"

def signal_user_input():
	"""start the keyboard listener"""
	global listener
	with keyboard.Listener(on_release=key_pressed) as listener:
		listener.join()

def key_pressed(key):
	"""does something according to the keyboard keys pressed, change the players state and the boolean value

	Args:
		key (keyboard._win32.KeyCode): the key pressed
	"""
	global open_menu, end_game, save_current_scene, load_new_scene

	if type(key) == keyboard._win32.KeyCode:
		if key.char == "w":
			open_menu = True
    
	if not open_menu:
		#PLAYER1
		if p1.state == State.REST:
			if type(key) == keyboard._win32.KeyCode:
				if key.char == "q":
					p1.state = State.LEFT
				elif key.char == "d":
					p1.state = State.RIGHT
				elif key.char == "a":
					p1.state = State.JUMPLSTART
				elif key.char == "e":
					p1.state = State.JUMPRSTART
				elif key.char == "z":
					p1.state = State.ATTACK
				elif key.char == "s":
					p1.state = State.BLOCK
		
		#PLAYER2
		if p2.state == State.REST:
			if type(key) == keyboard._win32.KeyCode:
				if key.char == "l":
					p2.state = State.JUMPLSTART
				elif key.char == "m":
					p2.state = State.JUMPRSTART
				#Attack
				elif key.char == "o":
					p2.state = State.ATTACK
				#Block
				elif key.char == "p":
					p2.state = State.BLOCK
			else:
				if key == keyboard.Key.left:
					p2.state = State.LEFT
				elif key == keyboard.Key.right:
					p2.state = State.RIGHT
	elif open_menu:
		if type(key) == keyboard._win32.KeyCode:
			if key.char == "b":
				open_menu = False		
			elif key.char == "v":
				open_menu = False
				end_game = True
			elif key.char == "f":
				load_new_scene = True
			elif key.char == "g":
				save_current_scene = True
				

def update_in_game():
	"""update the players position"""
	print("\033[%d;%dH" % (1, 1))  # reposition the cursor to the coordinate (1,1)
	all_p_pos = [p1.get_pos(), p2.get_pos()]
	all_p_character = [p1.get_character_orientation(), p2.get_character_orientation()]
	all_p_orientation = [p1.get_sword(), p2.get_sword()]
	stage.update_scene(all_p_pos, all_p_character, all_p_orientation)

def update():
	"""update the screen

	Returns:
		bool: to exit the while loop
	"""
	global pas_true, counter_p1, counter_p2, open_menu, t1, save_current_scene, load_new_scene, is_not_created, listener, load, file_name
	Player.p1_scored = False  # no score scored by player 1
	Player.p2_scored = False
	while True:

		ti = time.time()
		time.sleep(pas)  # used to do the frame rate
		pas_true = time.time()-ti
		counter_p1 += 1
		counter_p2 += 1

		if p1.state == State.LEFT:  # if player 1 state change to LEFT 
			if counter_p1 > p1.move_speed:  
				p1.set_character_orientation(Player.characterL)  # he looks left
				counter_p1 = 0
				sa.WaveObject.from_wave_file(walk).play()  # play walk sound
				p1.set_pos(p1.move_left())  # change the player position to his left
				p1.state = State.REST
		elif p1.state == State.RIGHT:  # if player 1 state change to RIGHT
			if counter_p1 > p1.move_speed:
				p1.set_character_orientation(Player.characterR)
				counter_p1 = 0
				sa.WaveObject.from_wave_file(walk).play()  # play walk sound
				p1.set_pos(p1.move_right())
				p1.state = State.REST
		#JUMP LEFT
		elif p1.state == State.JUMPLSTART:  # if player 1 state change to JUMP, first movement of this action
			if counter_p1 > p1.move_speed:  
				p1.set_character_orientation(Player.characterL)
				counter_p1 = 0
				sa.WaveObject.from_wave_file(jp).play()  # play jump sound
				p1.set_pos(p1.move_jump(0))  # change the player 1 position upwards
				p1.state = State.JUMPLMIDDLE
		elif p1.state == State.JUMPLMIDDLE:
			if counter_p1 > p1.move_speed:
				p1.set_pos(p1.move_left(Player.jump))
				counter_p1 = 0
				p1.state = State.JUMPLEND
		elif p1.state == State.JUMPLEND:
			if counter_p1 > p1.move_speed:
				p1.set_pos(p1.move_fall())  # change the position of the player 1 downwards
				counter_p1 = 0
				p1.state = State.REST
		#JUMP RIGHT
		elif p1.state == State.JUMPRSTART:
			if counter_p1 > p1.move_speed:
				p1.set_character_orientation(Player.characterR)
				counter_p1 = 0
				sa.WaveObject.from_wave_file(jp).play()  # play jump sound
				p1.set_pos(p1.move_jump(1))
				p1.state = State.JUMPRMIDDLE
		elif p1.state == State.JUMPRMIDDLE:
			if counter_p1 > p1.move_speed:
				p1.set_pos(p1.move_right(Player.jump))
				counter_p1 = 0
				p1.state = State.JUMPREND
		elif p1.state == State.JUMPREND:
			if counter_p1 > p1.move_speed:
				p1.set_pos(p1.move_fall())
				counter_p1 = 0
				p1.state = State.REST
		#ATTACK
		elif p1.state == State.ATTACK:
			p1.set_sword2("attack")
			counter_p1 = 0
			p1.state = State.ATTACKEND
		elif p1.state == State.ATTACKEND:
			if counter_p1 > p1.attack_speed:
				counter_p1 = 0
				if utils.attack_can_touch(p1, p2):
					sa.WaveObject.from_wave_file(shield_block).play()  # play shield block attack sound
					if not (utils.face_to_face(p1, p2) 
						and (utils.is_blocked(p1,p2))):
						sa.WaveObject.from_wave_file(sword_hit).play()  # play hit the enemy sound
						Player.score_p1 += 1
						Player.p1_scored = True
				else:
					sa.WaveObject.from_wave_file(sword_swing).play()  # play sword swing sound
				p1.state = State.REST
				p1.rest()
		#BLOCK
		elif p1.state == State.BLOCK:
			p1.set_sword2("block")
			counter_p1 = 0
			p1.state = State.BLOCKEND
		elif p1.state == State.BLOCKEND:
			if counter_p1 > p1.block_duration:
				counter_p1 = 0
				p1.state = State.REST
				p1.rest()
		#PLAYER2
		if p2.state == State.LEFT:
			if counter_p2 > p2.move_speed:
				p2.set_character_orientation(Player.characterL)
				counter_p2 = 0
				sa.WaveObject.from_wave_file(walk).play()
				p2.set_pos(p2.move_left())
				p2.state = State.REST
		elif p2.state == State.RIGHT:
			if counter_p2 > p2.move_speed:
				p2.set_character_orientation(Player.characterR)
				counter_p2 = 0
				sa.WaveObject.from_wave_file(walk).play()
				p2.set_pos(p2.move_right())
				p2.state = State.REST
		#JUMP LEFT
		elif p2.state == State.JUMPLSTART:
			if counter_p2 > p2.move_speed:
				p2.set_character_orientation(Player.characterL)
				counter_p2 = 0
				sa.WaveObject.from_wave_file(jp).play()
				p2.set_pos(p2.move_jump(0))
				p2.state = State.JUMPLMIDDLE
		elif p2.state == State.JUMPLMIDDLE:
			if counter_p2 > p2.move_speed:
				p2.set_pos(p2.move_left(Player.jump))
				counter_p2 = 0
				p2.state = State.JUMPLEND
		elif p2.state == State.JUMPLEND:
			if counter_p2 > p2.move_speed:
				p2.set_pos(p2.move_fall())
				counter_p2 = 0
				p2.state = State.REST
		#JUMPR
		elif p2.state == State.JUMPRSTART:
			if counter_p2 > p2.move_speed:
				p2.set_character_orientation(Player.characterR)
				counter_p2 = 0
				sa.WaveObject.from_wave_file(jp).play()
				p2.set_pos(p2.move_jump(1))
				p2.state = State.JUMPRMIDDLE
		elif p2.state == State.JUMPRMIDDLE:
			if counter_p2 > p2.move_speed:
				p2.set_pos(p2.move_right(Player.jump))
				counter_p2 = 0
				p2.state = State.JUMPREND
		elif p2.state == State.JUMPREND:
			if counter_p2 > p2.move_speed:
				p2.set_pos(p2.move_fall())
				counter_p2 = 0
				p2.state = State.REST
		#ATTACK
		elif p2.state == State.ATTACK:
			p2.set_sword2("attack")
			counter_p2 = 0
			p2.state = State.ATTACKEND
		elif p2.state == State.ATTACKEND:
			if counter_p2 > p2.attack_speed:
				counter_p2 = 0
				if utils.attack_can_touch(p2, p1):
					sa.WaveObject.from_wave_file(shield_block).play()
					if not (utils.face_to_face(p1, p2) 
             			and (utils.is_blocked(p1,p2))):
						sa.WaveObject.from_wave_file(sword_hit).play()
						Player.score_p2 += 1
						Player.p2_scored = True
				else:
					sa.WaveObject.from_wave_file(sword_swing).play()
				p2.state = State.REST
				p2.rest()
		#BLOoCK
		elif p2.state == State.BLOCK:
			p2.set_sword2("block")
			counter_p2 = 0
			p2.state = State.BLOCKEND
		elif p2.state == State.BLOCKEND:
			if counter_p2 > p2.block_duration:
				counter_p2 = 0
				p2.state = State.REST
				p2.rest()

		if open_menu:
			utils.clear_terminal()
			while open_menu:
				utils.show_menu()
				if save_current_scene:
					utils.clear_terminal()
					keyboard.Listener.stop(listener)
					t1.join()  # kill the thread
				
					kd = keyboard.Controller()  # a controller for sending virtual keyboard input
					key = keyboard.Key.enter  # the input to simulate
					kd.press(key)  #  simulates the pressure on the keyboard
					kd.release(key)  # simulates release on the keyboard
					input()  # used to hide the output of keyboard.Listener().join()
					utils.clear_terminal()
     
					file_name = input("Enter the file name in which you want to save the current scene and press enter: ")
					stage.save_current_scene(file_name, p1, p2)
					save_current_scene = False
					t1 = threading.Thread(target = signal_user_input,args=[])
					t1.start()
					utils.clear_terminal()
				elif load_new_scene:
					utils.clear_terminal()
					is_not_created = True
					if t1.is_alive():
						keyboard.Listener.stop(listener)
						t1.join()
					kd = keyboard.Controller()
					key = keyboard.Key.enter
					kd.press(key)
					kd.release(key)
					input()
					utils.clear_terminal()
					cursor.show()
					file_name = stage.load_new_scene()
					cursor.hide()
					utils.clear_terminal()
					load_new_scene = False
					open_menu = False
					load = True
			utils.clear_terminal()

  
		if Player.p1_scored or Player.p2_scored or end_game or load:
			return False
		update_in_game()

def play():
	"""play the game"""
	global restart, p1, p2, t1, is_not_created, load_new_scene, load
	print("\033[%d;%dH" % (1, 1))
	if restart:
		list_players = utils.create_players(attributs)
		stage.pos_players(utils.scene_content(file_name))
		p1 = list_players[0]
		p2 = list_players[1]
		restart = False
	elif load:
		Player.score_p1 = 0
		Player.score_p2 = 0
		stage.pos_players(utils.scene_content(file_name)) 
		list_players = utils.create_players(attributs)
		p1 = list_players[0]
		p2 = list_players[1]
		load = False

	stage.display_start_scene(file_name, 
							[p1.get_character_orientation(), p2.get_character_orientation()], 
							[p1.get_sword(), p2.get_sword()])
	if is_not_created:
		t1 = threading.Thread(target = signal_user_input,args=[])
		t1.start()
		is_not_created = False
	update()

def game(fps, file, player1, player2, file_attributs):
	"""start en end the game

	Args:
		fps (int): _description_
		file (str): _description_
		player1 (Player): _description_
		player2 (Player): _description_
		file_attributs (str): _description_
	"""
	global end_game, restart, time_refresh, pas, restart, file_name, attributs, p1, p2
	p1 = player1
	p2 = player2
	attributs = utils.attribut(utils.game_attribut(file_attributs))
	file_name = file
	time_refresh = fps
	pas = 1/time_refresh
	while not end_game:
		if Player.p1_scored and Player.p2_scored:  # if player 1 and 2 scored a point at the same time
			print("\033[%d;%dH" % (1, 1))
			stage.update_scene_after_scored()
			time.sleep(1.5)
			Player.score_p1 -= 1
			Player.score_p2 -= 1
			Player.p1_scored = False
			Player.p2_scored = False

			restart = True
   
		elif Player.p1_scored or Player.p2_scored:  # if player 1 or 2 scored a point
			print("\033[%d;%dH" % (1, 1))
			stage.update_scene_after_scored()
			time.sleep(1.5)
			Player.p1_scored = False
			Player.p2_scored = False

			restart = True

			if Player.score_p1 == 3 or Player.score_p2 == 3:
				print("\033[%d;%dH" % (1, 1))
				stage.update_scene_end()
				end_game = True
		else:
			play()
	print("GAME OVER")
