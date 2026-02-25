from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

Window.size = (900, 600)
class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # ใช้ BoxLayout จัดเรียงจากบนลงล่าง
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        # สร้าง Widget (Label)
        title_label = Label(text="TYPING TUTOR", font_size=50, bold=True, size_hint=(1, 0.4))
        
        # สร้าง Widget (Buttons)
        start_btn = Button(text="Start Game", font_size=30, size_hint=(1, 0.2), background_color=(0.2, 0.7, 0.3, 1))
        settings_btn = Button(text="Settings", font_size=30, size_hint=(1, 0.2))
        exit_btn = Button(text="Exit", font_size=30, size_hint=(1, 0.2), background_color=(0.8, 0.2, 0.2, 1))
        
        # ผูก Callback เมื่อกดปุ่ม 
        start_btn.bind(on_press=self.go_to_game)
        settings_btn.bind(on_press=self.go_to_settings)
        exit_btn.bind(on_press=self.exit_app)
        
        # นำ Widget ทั้งหมดใส่ลงใน Layout
        layout.add_widget(title_label)
        layout.add_widget(start_btn)
        layout.add_widget(settings_btn)
        layout.add_widget(exit_btn)
        self.add_widget(layout)
        
    # ฟังก์ชัน Callback สำหรับเปลี่ยนหน้าจอ
    def go_to_game(self, instance):
        self.manager.current = 'game' 
    def go_to_settings(self, instance):
        self.manager.current = 'settings'        
    def exit_app(self, instance):
        App.get_running_app().stop()


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        layout.add_widget(Label(text="Settings Screen (Coming Soon)", font_size=40))
        
        back_btn = Button(text="Back to Menu", font_size=30, size_hint=(1, 0.2))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        self.add_widget(layout)
    def go_back(self, instance):
        self.manager.current = 'menu'


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50)
        layout.add_widget(Label(text="Game Screen (Coming Soon)", font_size=40))
        
        # ปุ่มชั่วคราวให้กดกลับเมนูได้
        back_btn = Button(text="Give Up (Back to Menu)", font_size=30, size_hint=(1, 0.2))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'menu'


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        # สร้าง Widget (Labels, Buttons)
        title_label = Label(text="GAME OVER", font_size=50, bold=True, size_hint=(1, 0.3))        
        play_again_btn = Button(text="Play Again", font_size=30, size_hint=(1, 0.15), background_color=(0.2, 0.7, 0.3, 1))
        menu_btn = Button(text="Main Menu", font_size=30, size_hint=(1, 0.15))
        
        
class TypingTutorApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
    TypingTutorApp().run()