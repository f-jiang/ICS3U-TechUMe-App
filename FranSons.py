from kivy.app import App
from kivy.graphics import BorderImage
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, BoundedNumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.storage.jsonstore import JsonStore
from kivy.core.audio import Sound, SoundLoader
#from kivy.lang import Builder


import random
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
    shitter = 0
    def ericEaster(self, *args): # Eric's Easter Egg. Click his name three times in credits to have the time of your life.
        self.shitter += 1
        if self.shitter==3:
            self.shitter = 0
            Assets.sounds['lel.wav'].play()


class GameConfigScreen(Screen):

    def go(self, *args):
        InGame().go()

class PlayScreen(Screen):
    global box1
    global box3
    global box3data
    global promptE
    global ib
    
    def __init__(self, **kwargs):
        super(PlayScreen, self).__init__(**kwargs)
        
        # self.add_widget(Image(source="assets/textures/bg2.png"))
        global box1
        global box3
        global box3data
        global promptE
        global ib
        box1 = BoxLayout(orientation="horizontal")
        box2 = BoxLayout(orientation="vertical",
                         size_hint_x=0.5,
                         size_hint_y=1.0,
                         padding=50,
                         spacing=25)
        
        ib=GridLayout(cols=2) # input stuffs go here
        box2.add_widget(ib)
        bb=Button(size_hint_x=1.0,
                  size_hint_y=0.25,
                  text="Quit"
                  )
        bb.bind(on_press=PlayScreen.gtm)
        box2.add_widget(bb)
        box1.add_widget(box2)
        
        promptE = Image(source="")
        box1.add_widget(promptE)
        self.add_widget(box1)
    
    def gtm(self): # go to menu
        FranSons.screen_manager.transition.direction = "down"
        FranSons.screen_manager.current = "main"
    
    def updatePrompt(self, hint, input_data, correct_answer, **kwargs):
        global box1
        global box3
        global box3data
        global promptE
        global ib
        ib.clear_widgets(children=None)
        # newSource = args[0]
        # potentialAnswers = args[1]
        # correctAnswer = args[2]
        box1.remove_widget(promptE)
        box3 = []
        box3data = []
        for pa in input_data:
            box3.append(Button(text=str(pa),
                               size_hint_x=0.5,
                               size_hint_y=0.5))
            box3data.append(pa)
        for i in range(0,4):
            if box3data[i]==correct_answer:
                box3[i].bind(on_press=InGame.takeCorrect)
            else:
                box3[i].bind(on_press=InGame.takeWrong)
            ib.add_widget(box3[i])
        promptE = Image(source=hint, size_hint_x=0.5)
        box1.add_widget(promptE)
        
    def level(self, *args):
        InGame.level(InGame)

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

class InGame(): # host for functions relating to gameplay

    health = 3
    progress = -1
    difficulty = 0
    banged = [] # each word's face value that was banged is put into this array
    
    def go(self, *args):
        #BackgroundScreenManager.background_image = ObjectProperty(Image(source='assets/textures/bg1.png'))
        self.level()
        
        
    def level(self, *args):
        self.progress += 1
        possibilities = [] # creates list of possible prompts, picks random one from this later
        for p in Assets.words:
            if Assets.words[p].difficulty==self.difficulty and (not (p in self.banged)):
                possibilities.append(p)
        if(len(possibilities)>0):
            t = random.randrange(0, len(possibilities))
            self.currentWord = Assets.words[possibilities[int(t)]].definition # sets the level's current word
            
            pa0 = Assets.words[self.currentWord].inputs["mc"] # possible answers
            hint = Assets.words[self.currentWord].assets["texture"]
            random.shuffle(pa0)
            pa1 = [pa0[0], # here, add 3 of the bs answers and then the actual answer, then shuffle that shit up
                   pa0[1],
                   pa0[2],
                   self.currentWord]
            random.shuffle(pa1)
            
            PlayScreen.updatePrompt(PlayScreen, hint, pa1, self.currentWord)
            
            (self.banged).append(self.currentWord) # adds to list of already used words, so as not to use it in the future
            
        else:
            pass
        
    def takeCorrect(self, *args):
        print("Correct")
        
    def takeWrong(self, *args):
        print("Incorrect")
    
    def end(self, *args):
        pass


class Assets():
    word_source = JsonStore('assets/words.json') # TODO: for each word, add keys specified in Word class
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
                                                word['hints']
                                                )
                        for word in Assets.word_source.get('words')}
        
        # Loading the sounds
        Assets.sounds = {file_name:SoundLoader.load(filename=os.path.join('assets/sounds/', file_name))
                         for file_name in Assets.sound_sources.get('files')}

        # Loading the textures
        # for some reason this dict appears to be empty when accessed from the .kv file
        # TODO: find out why this is empty in kv file
        Assets.textures = {file_name:os.path.join('assets/textures/', file_name)
                           for file_name in Assets.texture_sources.get('files')}

# to access: Assets.words['the word you're looking for'].definition
class Word:

    # TODO: remove picture or sound output from list if no texture or sound provided
    def __init__(self, word, diff, inputs, hints, *args):
        self.definition = word                              # the actual word
        self.difficulty = diff                              # the word's difficulty
        self.inputs = inputs                                 # multiple choice possible answers
        self.assets = hints  # the texture and sound that go with the word (use these in the InGame class)
        

class BackgroundScreenManager(ScreenManager):
    background_image = ObjectProperty(Image(source='assets/textures/bg1.png'))

    """def __init__(self, **kwargs):    # TODO: fix sm size problems in python code
        super(BackgroundScreenManager, self).__init__(**kwargs)

        with self.canvas.before: # TODO: size of the screenmanager is wrong
            BorderImage(texture=BorderImage(source=Assets.textures['bg1.png']).texture, pos=self.pos, size=self.size)"""

class FranSons(App):
    screen_manager = None
    
    def build(self):
        # TODO: make a function for setting up game-related stuff?
        GameSave.load()
        Assets.load()
        
        # configure Settings panel
        self.settings_cls = SettingsWithTabbedPanel
        self.use_kivy_settings = False

        # initialize ScreenManager, set transition, add screens, and set current to splash screen
        FranSons.screen_manager = BackgroundScreenManager(transition=SlideTransition())
        FranSons.screen_manager.add_widget(SplashScreen(name="splash"))      # splash screen; loading occurs here
        FranSons.screen_manager.add_widget(MainMenuScreen(name="main"))      # main menu
        FranSons.screen_manager.add_widget(CreditsScreen(name="credits"))    # credits
        FranSons.screen_manager.add_widget(GameConfigScreen(name="conf"))    # more specific settings
        FranSons.screen_manager.add_widget(PlayScreen(name="play"))          # gameplay occurs here
        FranSons.screen_manager.add_widget(EndScreen(name="end"))            # end screen, with score breakdown
        FranSons.screen_manager.current = "splash"

        return FranSons.screen_manager

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
