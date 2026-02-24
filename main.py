from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

Window.size = (900, 600)

class TypingTutorApp(App):
    def build(self):
        sm = ScreenManager()
        return sm

if __name__ == '__main__':
    TypingTutorApp().run()