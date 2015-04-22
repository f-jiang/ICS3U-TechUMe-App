from kivy.app import App

from kivy.properties import ObjectProperty, BoundedNumericProperty

from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition, WipeTransition, FadeTransition, \
    FallOutTransition
from kivy.uix.carousel import Carousel
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar

from kivy.animation import Animation

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


class SettingsScreen(Screen):

    pass


class CreditsScreen(Screen):

    pass


class GameConfigScreen(Screen):

    pass


class PlayScreen(Screen):

    pass


class EndScreen(Screen):

    pass


class UndecidedName(App):

    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(SplashScreen(name="splash"))
        screen_manager.add_widget(MainMenuScreen(name="main"))
        screen_manager.add_widget(SettingsScreen(name="settings"))
        screen_manager.add_widget(CreditsScreen(name="credits"))
        screen_manager.add_widget(GameConfigScreen(name="conf")) # more specific settings
        screen_manager.add_widget(PlayScreen(name="play")) # gameplay
        screen_manager.add_widget(EndScreen(name="end")) # end screen, with score breakdown
        screen_manager.current = "splash"

        return screen_manager


if __name__ == "__main__":
    UndecidedName().run()
