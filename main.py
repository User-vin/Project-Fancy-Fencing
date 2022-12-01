from colorama import init, deinit
import stage
import refresh
import utils
import simpleaudio as sa
import cursor


def main(file, file_attributs = "attribut_value.txt"):
    """main function of the programm

    Args:
        file (str): the name of the file containing the scene
        file_attributs (str, optional): the name of the file containing the game parameters. Defaults to "attribut_value.txt".
    """
    utils.clear_terminal()
    cursor.hide()
    play_object = sa.WaveObject.from_wave_file("background.wav").play()  # play background music
    attributs = utils.attribut(utils.game_attribut(file_attributs))  # retrieves the contents of the file in the form of a dictionary
    stage.pos_players(utils.scene_content(file))  # retrieves players' positions
    list_players = utils.create_players(attributs)
    p1 = list_players[0]
    p2 = list_players[1]
    refresh.game(attributs.get("fps"), file, p1, p2, file_attributs)  # start the game
    play_object.stop()  # strop the background music
    cursor.show()

init()  # used to initialize colorama
main(stage.load_new_scene())
deinit()  # to stop colorama