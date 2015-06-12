from kivy.app import App
from kivy.graphics import BorderImage
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, BoundedNumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.settings import *
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.storage.jsonstore import JsonStore
from kivy.core.audio import Sound, SoundLoader
from kivy.uix.progressbar import ProgressBar
from kivy.config import ConfigParser
from kivy.config import Config
from kivy.uix.popup import Popup
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

class SplashScreen(Screen):
    bar = ObjectProperty(None)

    def on_enter(self, *args):
        bar = self.ids["loading_bar"]
        animation = Animation(value=bar.max, duration=2.0)
        animation.start(bar)
        animation.bind (on_complete=SplashScreen.complete)

    def complete(self, *args):
        FranSons.screen_manager.transition.direction = "left"
        FranSons.screen_manager.current = "main"


class MainMenuScreen(Screen):
    def on_enter(self, *args):
        if Assets.sounds['backgroundmusic.wav'].state == 'stop':
            Assets.play_music('backgroundmusic.wav', True)


class CreditsScreen(Screen):
    shitter = 0
    def ericEaster(self, *args): # Eric's Easter Egg. Click his name three times in credits to have the time of your life.
        self.shitter += 1
        if self.shitter==6:
            self.shitter = 0
            Assets.sounds['lel.wav'].play() # this will play even if sound effects have been muted in the settings!


'''class GameConfigScreen(Screen):

    # feilan: because ingame is a part of the playscreen, ingame.go should be called in playscreen class
    def go(self, *args):
        Assets.sounds['backgroundmusic.wav'].stop()
        InGame().go(2, 5)'''


class PlayScreen(Screen):
    global box1
    global box3
    global box3data
    global promptE
    global ib
    global timerbar

    def __init__(self, **kwargs):
        super(PlayScreen, self).__init__(**kwargs)

        # self.add_widget(Image(source="assets/textures/bg2.png"))
        global box1
        global box3
        global box3data
        global promptE
        global ib
        global timerbar
        global timerholder
        global healthLabel
        box0 = BoxLayout(orientation="vertical")
        box1 = BoxLayout(orientation="horizontal",
                         size_hint_y=0.9,
                         padding=50,
                         spacing=25)
        box2 = BoxLayout(orientation="vertical",
                         size_hint_x=0.5,
                         size_hint_y=1.0)

        ib=GridLayout(cols=2) # input stuffs go here
        box2.add_widget(ib)
        bb=Button(size_hint_x=1.0,
                  size_hint_y=0.25,
                  text="Quit"
                  )
        bb.bind(on_release=PlayScreen.toMenu)
        box2.add_widget(bb)
        box1.add_widget(box2)

        promptE = Image(source="")
        box1.add_widget(promptE)
        timerbar = ProgressBar(max=100,
                               size_hint_y=1.0,
                               size_hint_x=0.5,
                               pos_hint={'right': 0.9}
                               )
        healthLabel = Label(text="HEALTH",
                            size_hint_y=1.0,
                            size_hint_x=0.5)
        timerholder = GridLayout(cols=2,
                                 size_hint_y=0.1,
                                 size_hint_x=0.8,
                                 pos_hint={'right': 0.9}
                                 )
        timerholder.add_widget(timerbar)
        timerholder.add_widget(healthLabel)
        box0.add_widget(timerholder)
        box0.add_widget(box1)
        self.add_widget(box0)

    def on_pre_enter(self, *args):
        health = 0
        length = 0
        diffculty = 0

        # sets health according to difficulty level
        if FranSons.settings.get('gameplay', 'difficulty') == 'Easy':
            health = 7
            difficulty = 1
        elif FranSons.settings.get('gameplay', 'difficulty') == 'Normal':
            health = 5
            difficulty = 2
        elif FranSons.settings.get('gameplay', 'difficulty') == 'Hard':
            health = 3
            difficulty = 3

        if FranSons.settings.get('gameplay', 'words') == 'All Words':
            length = len(Assets.words)
        else:
            length = int(FranSons.settings.get('gameplay', 'words'))

        print('length: ', length, ' health: ', health, ' difficulty number: ', difficulty)

        # starts the game and uses length and health variables as parameters
        InGame().go(health, length, difficulty)

    def on_enter(self, *args):
        animation = Animation(volume=0.0, duration=0.5)
        animation.start(Assets.sounds['backgroundmusic.wav'])
        animation.bind(on_complete=PlayScreen.on_mute)

    def on_mute(self, *args):
        Assets.sounds['backgroundmusic.wav'].stop()
        Assets.sounds['backgroundmusic.wav'].volume = 1.0

    def toMenu(self): # go to menu
        InGame.stop(self)
        global timerO
        global timerbar
        timerO.cancel(timerbar)
        FranSons.screen_manager.transition.direction = "down"
        FranSons.screen_manager.current = "main"

    def toEndScreen(self):
        InGame.stop(self)

        FranSons.screen_manager.transition.direction = "left"
        FranSons.screen_manager.current = "end"

    def updatePrompt(self, hint, input_data, correct_answer, type, promptType, tl, **kwargs):
        global box1
        global box3
        global box3data
        global promptE
        global ib
        global timerbar
        global timerholder
        global timerO

        ib.clear_widgets(children=None)

        # if input_data is of mc format
        # newSource = args[0]
        # potentialAnswers = args[1]
        # correctAnswer = args[2]
        box1.remove_widget(promptE)
        timerholder.remove_widget(timerbar)
        box3 = []
        box3data = []
        timerbar = None
        for pa in input_data:
            box3.append(Button(text=str(pa),
                               size_hint_x=0.5,
                               size_hint_y=0.5,
                               font_size=20))
            box3data.append(pa)
        for i in range(0, len(input_data)):
            if box3data[i]==correct_answer:
                box3[i].bind(on_press=InGame.takeCorrect)
            else:
                box3[i].bind(on_press=InGame.takeWrong)
            ib.add_widget(box3[i])

        # if the hint provided is an image
        if type == "mc":
            if promptType == "texture":
                promptE = Image(source=hint, size_hint_x=0.5)
            else:
                promptE = Button(text="(sound)", size_hint_x=0.3, font_size=64, color=[1,1,1, 1], )
                promptE.bind(on_press=InGame.playCurrentPrompt)
                InGame.playCurrentPrompt()
        else:
            promptE = Button(text=hint,
                             size_hint_x=0.5,
                             size_hint_y=0.5,
                             font_size=64,
                             color=[1,1,1, 1],
                             pos_hint={'center_y': 0.5})
        box1.add_widget(promptE)
        timerbar = ProgressBar(max=100,
                               value=100,
                               size_hint_y=1.0,
                               size_hint_x=1.0
                               )
        timerholder.add_widget(timerbar)
        timerO = Animation(value=0, duration=tl)
        timerO.start(timerbar)
        timerO.bind(on_complete=InGame.takeTime)

    def level(self, *args): # feilan: could remove because not being used anywhere
        InGame.level(InGame)


class EndScreen(Screen):
    summary = ObjectProperty(None)

    def on_enter(self, *args):
        Assets.play_music('backgroundmusic.wav', True)

    def on_pre_enter(self, *args):
        summary = self.ids['summary']
        summary.text = "Correct Answers: " + str(InGame.num_correct) \
                       + "\nWrong Answers: " + str(InGame.num_wrong) \
                       + "\nUnanswered Questions: " + str(InGame.num_unanswered)

class StatsScreen(Screen):
    stats_box = ObjectProperty(None)
    stats_reset = ObjectProperty(None)
    popup = None

    def __init__(self, **kwargs):
        super(StatsScreen, self).__init__(**kwargs)

        StatsScreen.popup = Popup(title='Reset Stats',
                                  size_hint=(0.6, 0.6),
                                  auto_dismiss=False)
        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(Label(text='Are you sure you want to do this?'))
        popup_buttons = BoxLayout(size_hint_y=0.2)
        yes_btn = Button(text='Yes')
        yes_btn.bind(on_press=StatsScreen.reset_stats)
        no_btn = Button(text='No')
        no_btn.bind(on_press=StatsScreen.popup.dismiss)
        popup_buttons.add_widget(yes_btn)
        popup_buttons.add_widget(no_btn)
        popup_content.add_widget(popup_buttons)
        StatsScreen.popup.content = popup_content

        stats_reset = self.ids['stats_reset']
        stats_reset.bind(on_press=StatsScreen.popup.open)

    def on_pre_enter(self, *args):
        print(self)
        StatsScreen.refresh_stats_box(self)

    def reset_stats(self, *args):
        GameSave.reset()
        StatsScreen.refresh_stats_box(FranSons.screen_manager.current_screen)
        StatsScreen.popup.dismiss()

    def refresh_stats_box(self):
        stats_box = self.ids['stats_box']
        stats_box.text = "Correct Answers: " + str(GameSave.total_correct) \
                         + "\nWrong Answers: " + str(GameSave.total_wrong) \
                         + "\nUnanswered Questions: " + str(GameSave.total_unanswered) \
                         + "\nTotal Time Played: " + str(GameSave.time_played_s) + " s"



# feilan: for this class we need to decide whether we should use it as a static (would use InGame instead of self)
# class or an instance (would use self) because using both conventions at the same time will cause us a lot of problems
# for now ive made it so that we use ingame as a static class
# also if we choose not to use instances, we may as well go procedural and move all the code in this class back into
# playscreen (i say we do it)
class InGame(): # host for functions relating to gameplay

    health = 3
    progress = -1
    goal = 10       # the value progress needs to be if we want to win
    difficulty = 1  # TODO: to be user-defined
    banged = [] # each word's face value that was banged is put into this array

    num_correct = 0
    num_wrong = 0
    num_unanswered = 0
    time = 0

    def go(self, starting_health, goal, difficulty):
        #BackgroundScreenManager.background_image = ObjectProperty(Image(source='assets/textures/bg1.png'))

        InGame.health = starting_health
        InGame.progress = 0
        InGame.goal = goal
        InGame.difficulty = difficulty

        InGame.num_correct = 0
        InGame.num_wrong = 0
        InGame.num_unanswered = 0
        InGame.time = 0

        print('starting values for health, progress, and goal: ', InGame.health, InGame.progress, InGame.goal)

        InGame.level()

    def stop(self):
        GameSave.total_correct += InGame.num_correct
        GameSave.total_wrong += InGame.num_wrong
        GameSave.total_unanswered += InGame.num_unanswered
        GameSave.time_played_s += InGame.time
        GameSave.save()
        InGame.banged = []

    def level(*args):
        global time
        global healthLabel
        global timerholder
        """feilan: BASIC GAMEFLOW DESCRIPTION:
        -progress increases when answer correct
        -health decreases when answer incorrect
        -win by getting progress to certain value
        -lose by losing all health"""

        # self.progress += 1

        # making a list of words that can be asked
        possibilities = [] # creates list of possible prompts, picks random one from this later
        for p in Assets.words:
            if not (p in InGame.banged):
                possibilities.append(p)
        if len(possibilities) > 0 and InGame.progress < InGame.goal and InGame.health > 0:
            # selecting a word
            t = random.randrange(0, len(possibilities))
            InGame.currentWord = Assets.words[possibilities[int(t)]].definition # sets the level's current word
            (InGame.banged).append(InGame.currentWord) # adds to list of already used words, so as not to use it in the future

            # here: add code for picking answer format, hint format
            opts = ["mc","wp"]
            random.shuffle(opts)
            # if mc is the chosen answer format
            if opts[0]=="mc":
                promptType = ["texture", "sound"][random.randint(0,1)]
                hint = Assets.words[InGame.currentWord].assets[promptType]
                pa0 = Assets.words[InGame.currentWord].inputs["mc"] # possible answers
                random.shuffle(pa0)
                inputData = [pa0[0], # here, add 3 of the bs answers and then the actual answer, then shuffle that shit up
                             pa0[1],
                             pa0[2],
                             InGame.currentWord]
                correct_answer = InGame.currentWord
            elif opts[0]=="wp":
                promptType = "giant penis" # null value, will not be used, just here to fill a parameter space that is only necessary for "mc". Do not remove.
                hn = random.randint(0, 1)
                hint = (InGame.currentWord).replace(Assets.words[InGame.currentWord].inputs["wp"][hn]["def"], "qwertyuiop")
                bsl = ""
                for i in range(0, len(Assets.words[InGame.currentWord].inputs["wp"][hn]["def"])):
                    bsl += "_"
                hint = hint.replace("qwertyuiop", bsl)
                pa0 = Assets.words[InGame.currentWord].inputs["wp"][random.randint(2, 3)]["def"] # possible answers
                pa00= Assets.words[InGame.currentWord].inputs["wp"][hn]["def"]
                inputData = [pa0,
                             pa00]
                correct_answer = pa00
            random.shuffle(inputData)
            timeLength = ((0.5**((4/InGame.goal)*InGame.progress)/(4 - InGame.difficulty))*9)+(7 - InGame.difficulty)

            InGame.time += int(timeLength)
            
            # feilan: suggestion: move updateprompt into this class
            PlayScreen.updatePrompt(PlayScreen, hint, inputData, correct_answer, opts[0], promptType, timeLength) # update level
            # update health display:
            timerholder.remove_widget(healthLabel)
            healthLabel = None
            healthLabel = Label(text="Health: "+str(InGame.health),
                            size_hint_y=1.0,
                            size_hint_x=0.5,
                            font_size=32,
                            color=[0, 0, 0, 1],
                            halign="center")
            timerholder.add_widget(healthLabel)
        else:
            InGame.end()
    def playCurrentPrompt(*args):
        Assets.sounds[Assets.words[InGame.currentWord].assets["sound"].replace("assets/sounds/", "")].play()
        
    def takeCorrect(*args):
        global timerO
        global timerbar
        timerO.cancel(timerbar)
        
        # update stat
        InGame.num_correct += 1
        if (int(GameSave.total_correct) + int(InGame.num_correct)) == 420:
            Assets.sounds['enya_only_time.mp3'].play()
        InGame.progress += 1
        print("Correct")
        print('current values for health, progress, and goal: ', InGame.health, InGame.progress, InGame.goal)

        if InGame.progress >= InGame.goal:
            InGame.end()
        else:
            InGame.level()

        Assets.play_sound('correctanswer.wav')


    def takeWrong(*args):
        global timerO
        global timerbar
        timerO.cancel(timerbar)
        
        # update stat
        InGame.num_wrong += 1

        InGame.health -= 1
        print("Incorrect")
        print('current values for health, progress, and goal: ', InGame.health, InGame.progress, InGame.goal)

        if InGame.health > 0:
            InGame.level()
        else:
            InGame.end()

        Assets.play_sound('surprise.wav')
    def takeTime(*args):
        global timerO
        global timerbar
        timerO.cancel(timerbar)
        
        # update stat
        InGame.num_unanswered += 1

        InGame.health -= 1
        print("unanswered")
        print('current values for health, progress, and goal: ', InGame.health, InGame.progress, InGame.goal)

        if InGame.health > 0:
            InGame.level()
        else:
            InGame.end()

        Assets.play_sound('surprise.wav')
    def end(*args):
        InGame.stop(None)
        print('game over')

        # go to end screen instead
        PlayScreen.toEndScreen(None)


# TODO: determine what needs to be saved
class GameSave():
    source = JsonStore('save.json')

    total_correct = 0
    total_wrong = 0
    total_unanswered = 0    # TODO: find a place to update this stat
    time_played_s = 0       # TODO: find a place to update this stat

    # loads game save
    def load(*args):
        # sets up json if it has no values yet
        if GameSave.source.count() == 0:
            GameSave.set_to_default()

        # writes json values to class variables
        GameSave.total_correct = GameSave.source.get('answers')['total_correct']
        GameSave.total_wrong = GameSave.source.get('answers')['total_wrong']
        GameSave.total_unanswered = GameSave.source.get('answers')['total_unanswered']
        GameSave.time_played_s = GameSave.source.get('time_played_s')['value']

    # overwrites game save
    def save(*args):
        # writes class variables to json values
        GameSave.source.put('answers',
                            total_correct=GameSave.total_correct,
                            total_wrong=GameSave.total_wrong,
                            total_unanswered=GameSave.total_unanswered)
        GameSave.source.put('time_played_s', value=GameSave.time_played_s)

    # resets game save
    def reset(*args):
        GameSave.set_to_default()     # clear the json
        GameSave.load()               # load default values

    # resets game save json to default values
    def set_to_default(*args):
        GameSave.source.put('answers', total_correct=0, total_wrong=0, total_unanswered=0)
        GameSave.source.put('time_played_s', value=0)
        print(GameSave.source.get('answers'))


class Assets():
    word_source = JsonStore('assets/words.json')
    sound_sources = JsonStore('assets/sounds/index.json')
    texture_sources = JsonStore('assets/textures/index.json')
    
    words = {}
    sounds = {}
    textures = {}

    current_music = []
    current_sound_effects = []

    # loads all assets and writes them to class variables
    def load(*args):
        # Loading the words
        Assets.words = {word['definition']:Word(word['definition'],
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

    def play_sound(name: str, do_loop=False):
        if FranSons.settings.get('app', 'sfx') and name in Assets.sounds:
            Assets.sounds[name].play()
            if do_loop:
                Assets.sounds[name].loop = True

    def play_music(name: str, do_loop=False):
        if FranSons.settings.get('app', 'music') and name in Assets.sounds:
            Assets.sounds[name].play()
            if do_loop:
                Assets.sounds[name].loop = True

    def toggle_sounds(do_mute: bool):
        if do_mute:
            volume = 0
        else:
            volume = 1

        print(Assets.current_sound_effects)

        for name in Assets.current_sound_effects:
            Assets.sounds[name].volume = volume

    def toggle_music(do_mute: bool):
        if do_mute:
            volume = 0
        else:
            volume = 1

        print(Assets.current_music)

        for name in Assets.current_music:
            Assets.sounds[name].volume = volume


# to access: Assets.words['the word you're looking for'].definition
class Word:

    def __init__(self, word, inputs, hints, *args):
        self.definition = word                              # the actual word
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
    settings = None

    def build(self):
        # TODO: make a function for setting up game-related stuff?
        GameSave.load()
        Assets.load()
        
        # configure Settings panel
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False

        # initialize ScreenManager, set transition, add screens, and set current to splash screen
        FranSons.screen_manager = BackgroundScreenManager(transition=SlideTransition())
        FranSons.screen_manager.add_widget(SplashScreen(name="splash"))      # splash screen; loading occurs here
        FranSons.screen_manager.add_widget(MainMenuScreen(name="main"))      # main menu
        FranSons.screen_manager.add_widget(CreditsScreen(name="credits"))    # credits
        # FranSons.screen_manager.add_widget(GameConfigScreen(name="conf"))    # more specific settings
        FranSons.screen_manager.add_widget(PlayScreen(name="play"))          # gameplay occurs here
        FranSons.screen_manager.add_widget(EndScreen(name="end"))            # end screen, with score breakdown
        FranSons.screen_manager.add_widget(StatsScreen(name="stats"))        # players stats
        FranSons.screen_manager.current = "splash"

        ''' the app's settings can now be accessed through this variable
            how to access this from an outside class:
            print(FranSons.settings.get('gameplay', 'difficulty'))
        '''
        FranSons.settings = self.config

        return FranSons.screen_manager

    def build_config(self, config):
        config.setdefaults("settings", {
            "music": True,
            "sfx": True
        })
        config.setdefaults("gameplay", {
            "difficulty": 'Normal',
            "words": 10,
            "nature": True,
            "food": True,
            "machines": True
        })

    def build_settings(self, settings):
        settings.add_json_panel("App",
                                self.config,
                                data=json.dumps([
                                    {'type': 'bool',
                                     'title': 'Music',
                                     'desc': 'Toggle Music',
                                     'section': 'app',
                                     'key': 'music',
                                     'values': ['False', 'True']},
                                    {'type': 'bool',
                                     'title': 'Sound Effects',
                                     'desc': 'Toggle Sound Effects',
                                     'section': 'app',
                                     'key': 'sfx',
                                     'values': ['False', 'True']}])
                                )
        settings.add_json_panel("Gameplay",
                                self.config,
                                data=json.dumps([
                                    {'type': 'options',
                                     'title': 'Difficulty',
                                     'desc': 'In harder games, you have fewer lives and less time to answer each '
                                             'question.',
                                     'section': 'gameplay',
                                     'key': 'difficulty',
                                     'options': ['Easy', 'Normal', 'Hard']},
                                    {'type': 'options', # number of words per game
                                     'title': 'Words per Game',
                                     'section': 'gameplay',
                                     'key': 'words',
                                     'options': ["5", "10", "25", "50", "All Words"]},
                                    {'type': 'title',
                                     'title': 'Word Categories'},
                                    {'type': 'bool',
                                     'title': 'Nature',
                                     'section': 'gameplay',
                                     'key': 'nature',
                                     'values': ['False', 'True']},
                                    {'type': 'bool',
                                     'title': 'Food',
                                     'section': 'gameplay',
                                     'key': 'food',
                                     'values': ['False', 'True']},
                                    {'type': 'bool',
                                     'title': 'Machines',
                                     'section': 'gameplay',
                                     'key': 'machines',
                                     'values': ['False', 'True']}])
                                )

    def on_config_change(self, config, section, key, value):
        print(section, key, value)

        if section == 'app':
            if key == 'music':
                print('toggling music')
                Assets.toggle_music(value)
            elif key == 'sfx':
                print('toggling sound')
                Assets.toggle_sounds(value)


if __name__ == "__main__":
    FranSons().run()
