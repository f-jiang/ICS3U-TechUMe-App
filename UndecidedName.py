from kivy.app import App
from kivy.properties import ObjectProperty, BoundedNumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.animation import Animation
from kivy.storage.jsonstore import JsonStore

import json


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

    pass


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


class Assets():
    pass


class UndecidedName(App):

    def build(self):
        GameSave.load() # will probably move this somewhere else
        print(len(GameSave.source.keys())) # just a test

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
    UndecidedName().run()
