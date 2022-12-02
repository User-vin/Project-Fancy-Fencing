![Fancy_Fencing (2)](https://user-images.githubusercontent.com/101265722/205340697-1387c947-7f25-4fbd-9812-108992eb8fcd.png)


# Fancy Fencing

## What is it ?
Fancy Fencing is a game about fencing playable by two people at the same time. You will fight against your opponent, the first one to score 3 points by eliminating your adversary is the winner.

It offers a gameplay adaptable to your wishes, with background music and sound effects to make the game more immersive.

Unfortunately, only playable on windows terminal.

# Installation

- download all the files of the project page, and put them all in the same folder (don't delete the default.ffscene and attribut_value.txt files, you need them)
- install python 3.9.6 or higher version
- install all necessary python module

## Python modul to install

Use the pakage manager [pip](https://pip.pypa.io/en/stable/installation/) to install [simpleaudio](https://simpleaudio.readthedocs.io/en/latest/)
```python
pip install simpleaudio
```
cursor
```python
pip install cursor
```
[pynput](https://pypi.org/project/pynput/)
```python
pip install pynput
```
[threading](https://docs.python.org/3.9/library/threading.html)
```python
pip install threading
```
[colorama](https://pypi.org/project/colorama/)
```python
pip install colorama
```

# The game is now ready

You can start a game using this command in your game folder
```python
python main.py
```

## Load scene
The game will first ask you to enter the name of the scene you want to load (.ffscene). 
Only then the game will start.

You can create the scene you want with a file file_name.ffscene. You want to add the ground using "_" and the player1 using "1" and player2 "2" and obstacle with "x", all of these with only a single line.



With this: ![image](https://user-images.githubusercontent.com/101265722/205369720-8b0ac2a4-f073-4e67-bda3-ed7c57cb1cbd.png)
 in your .ffscene file 

You obtain this scene: 

![scene_with_obstacles](https://user-images.githubusercontent.com/101265722/205369142-d3e7b3b6-7558-41eb-9214-f5a9dba0d6b0.PNG)

Without obstacles: 
![image](https://user-images.githubusercontent.com/101265722/205369610-0640cfb0-e535-4872-9e0a-c85f10376ec5.png)


![attack3](https://user-images.githubusercontent.com/101265722/205369259-3812299a-9fb5-497c-9599-5853245ca970.PNG)


## Play scene

In this scene you have:

- the two players (1st player with green sword, the 2nd a red sword)
- the score board
- the key to press to access the menu

![image](https://user-images.githubusercontent.com/101265722/205354644-2c716bfd-2ae4-40f3-b948-f97a0a8b0cf0.png)

Each player can move his character

Block attack

![gif_block](https://user-images.githubusercontent.com/101265722/205373232-bfb2d55b-7e54-48f3-a29f-7edcb43a9112.gif)


Score a point

![gif_kill](https://user-images.githubusercontent.com/101265722/205373238-c074dfad-e32a-462f-a693-e55a5a8a9239.gif)

## Menu scene
Press the w key to access to menu pause showing the different controls and allowing to quit the game.

![image](https://user-images.githubusercontent.com/101265722/205355915-a878b38e-fc14-42d3-a972-caa50d6bea6a.png)

- press f and enter a valid name to load a new scene
- press g and enter a valid name to save the current scene
- press v to quit the game
- press b to resume the game




In its current state, the game is quite playable, but you can make it even better by customizing your own settings.
Each player can have unique attributes.
Changing the values in the attribute_value.txt file changes the speed (frame per second) and the way the game is played.

![image](https://user-images.githubusercontent.com/101265722/205365397-a66d0040-aed3-46dd-ac5c-cc8d30125e35.png)




