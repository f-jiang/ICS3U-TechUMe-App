from kivy.app import App
from kivy.properties import ObjectProperty, BoundedNumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.storage.jsonstore import JsonStore
from kivy.core.audio import Sound, SoundLoader
from kivy.lang import Builder

import json
import os

'''
how ScreenManagers work:
-each screen gets its own class
-you add screens to the screen manager using the add_widget function
-you set the screen being displayed by setting the "current" property to the name of the desired screen
-you can set the direction of the transition animation by setting the "transition.direction" property to either "up",
"down", "left", or "right"
'''

# TODO: for all classes determine which variables are "private"


class SplashScreen(Screen):

    bar = ObjectProperty(None)

    def play_load_animation(self, *args):
        bar = self.ids["loading_bar"]
        animation = Animation(value=bar.max, duration=2.0)
        animation.start(bar)


class MainMenuScreen(Screen):

    pass


class CreditsScreen(Screen):

    pass


class GameConfigScreen(Screen):

    pass


class PlayScreen(Screen):

    def on_pre_enter():
        InGame().go()
        InGame().level("fraise")


class EndScreen(Screen):

    pass


# TODO: determine what needs to be saved
class GameSave():
    source = JsonStore('save.json')

    # loads game save
    def load(*args):
        # sets up json if it has no values yet
        if GameSave.source.count() == 0:
            GameSave.set_to_default()

        # writes json values to class variables

    # overwrites game save
    def save(*args):
        # writes class variables to json values
        pass

    # resets game save
    def reset(*args):
        GameSave.source.clear()     # clear the json
        GameSave.set_to_default()   # set to default values
        GameSave.load()             # load default values

    # resets game save json to default values
    def set_to_default(*args):
        GameSave.source.put('example', value=1)    # placeholder; will replace with real values later


class InGame(): # allows for functions relating to gameplay
    def go(self, *args):
        Builder.load_string("""
<PlayScreen>:
    name: "play"
    BoxLayout:
        orientation: "horizontal"
        Button:
            size_hint_x: 0.5
            size_hint_y: 1.0
            text: "Output/Prompts"
            on_press:
                root.manager.transition.direction = "right"
                root.manager.current = "end"
        BoxLayout:
            orientation: "vertical"
            size_hint_x: 0.5
            size_hint_y: 1.0
            padding: 50
            spacing: 25
            Button:
                size_hint_x: 1.0
                size_hint_y: 0.75
                text: "Player Input"
                on_press:
                    InGame().level("pomme")
            Button:
                size_hint_x: 1.0
                size_hint_y: 0.25
                text: "Quit"
                on_press:
                    root.manager.transition.direction = "down"
                    root.manager.current = "main"
""")
        
    def level(self, *args):
        Builder.load_string("""
<PlayScreen>:
    name: "play"
    BoxLayout:
        orientation: "horizontal"
        Button:
            size_hint_x: 0.5
            size_hint_y: 1.0
            text: "Output/Prompts"
            on_press:
                root.manager.transition.direction = "right"
                root.manager.current = "end"
        BoxLayout:
            orientation: "vertical"
            size_hint_x: 0.5
            size_hint_y: 1.0
            padding: 50
            spacing: 25
            Button:
                size_hint_x: 1.0
                size_hint_y: 0.75
                text: "Player Input"
                on_press:
                    InGame().level(\"""" + str(args[0]) + """\")
            Button:
                size_hint_x: 1.0
                size_hint_y: 0.25
                text: "Quit"
                on_press:
                    root.manager.transition.direction = "down"
                    root.manager.current = "main"
""")
        

class Assets():
    word_source = JsonStore('assets/words.json')   # TODO: for each word, add keys specified in Word class
    sound_sources = JsonStore('assets/sounds/index.json')
    texture_sources = JsonStore('assets/textures/index.json')

    words = {}
    sounds = {}
    textures = {}

    # loads all assets and writes them to class variables
    def load(*args):
        # Loading the words
        Assets.words = {word['definition']:Word(word['definition'],
                                                word['difficulty'],
                                                word['inputs'],
                                                word['outputs'],
                                                word['assets']['texture'],
                                                word['assets']['sound'])
                        for word in Assets.word_source.get('words')}

        # Loading the sounds
        Assets.sounds = {file_name:SoundLoader.load(os.path.join('assets/sounds/', file_name))
                         for file_name in Assets.sound_sources.get('files')}
        # TODO: get sounds working after visit
        # Sound.play(Assets.sounds['lel.wav'])    # play the sound (just a test) (unsuccessful)

        # Loading the textures
        # for some reason this dict appears to be empty when accessed from the .kv file
        # TODO: find out why this is empty in kv file
        Assets.textures = {file_name:os.path.join('assets/textures/', file_name)
                           for file_name in Assets.texture_sources.get('files')}


class Word():

    # TODO: remove picture or sound output from list if no texture or sound provided
    def __init__(self, word, diff, inputs, outputs, texture=None, sound=None, *args):
        self.definition = word
        self.difficulty = diff
        self.input_prompts = inputs
        self.output_prompts = outputs
        self.assets = {'texture': texture, 'sound': sound}


class FranSons(App):

    def build(self):
        # TODO: make a function for setting up game-related stuff?
        GameSave.load()
        Assets.load()

        # configure Settings panel
        self.settings_cls = SettingsWithTabbedPanel
        self.use_kivy_settings = False

        # create ScreenManager, set transition, add screens, and set current to splash screen
        screen_manager = ScreenManager(transition=SlideTransition())
        screen_manager.add_widget(SplashScreen(name="splash"))      # splash screen; loading occurs here
        screen_manager.add_widget(MainMenuScreen(name="main"))      # main menu
        screen_manager.add_widget(CreditsScreen(name="credits"))    # credits
        screen_manager.add_widget(GameConfigScreen(name="conf"))    # more specific settings
        screen_manager.add_widget(PlayScreen(name="play"))          # gameplay occurs here
        screen_manager.add_widget(EndScreen(name="end"))            # end screen, with score breakdown
        screen_manager.current = "splash"

        return screen_manager

    def build_config(self, config):
        config.setdefaults("settings", {
            "music": True,
            "sfx": True
        })

    def build_settings(self, settings):
        settings.add_json_panel("Settings",
                                self.config,
                                data=json.dumps([
                                    {'type': 'bool',
                                     'title': 'Music',
                                     'desc': 'Toggle Music',
                                     'section': 'settings',
                                     'key': 'music'},
                                    {'type': 'bool',
                                     'title': 'Sound Effects',
                                     'desc': 'Toggle Sound Effects',
                                     'section': 'settings',
                                     'key': 'sfx'}])
                                )

if __name__ == "__main__":
    FranSons().run()
