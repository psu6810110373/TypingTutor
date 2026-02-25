from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

Window.size = (900, 600)
Window.clearcolor = get_color_from_hex('#1E1E2E')

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

        # สร้าง Widget (Labels)
        title = Label(text="SETTINGS", font_size=50, bold=True, size_hint=(1, 0.3))
        subtitle = Label(text="Select Time Limit:", font_size=30, size_hint=(1, 0.1))

        # สร้าง Widget (Buttons สำหรับเลือกเวลา)
        time_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint=(1, 0.2))
        self.btn_15 = Button(text="15 Sec", font_size=30, background_color=(0.5, 0.5, 0.5, 1))
        self.btn_30 = Button(text="30 Sec", font_size=30, background_color=(0.2, 0.7, 0.3, 1)) 
        self.btn_60 = Button(text="60 Sec", font_size=30, background_color=(0.5, 0.5, 0.5, 1))
        
        # ผูก Callbacks ให้ตรวจจับการกดปุ่ม
        self.btn_15.bind(on_press=self.set_time_15)
        self.btn_30.bind(on_press=self.set_time_30)
        self.btn_60.bind(on_press=self.set_time_60)

        #นำปุ่มเวลาใส่ในlayout
        time_layout.add_widget(self.btn_15)
        time_layout.add_widget(self.btn_30)
        time_layout.add_widget(self.btn_60)

        #ปุ่มเมนูหลัก
        back_btn = Button(text="Back to Menu", font_size=30, size_hint=(1, 0.2))
        back_btn.bind(on_press=self.go_back)

        #นำแต่ละwidgetใส่ในlayout
        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(time_layout)
        layout.add_widget(back_btn)
        self.add_widget(layout)

        self.selected_time = 30

    # สร้างฟังก์ชัน Callback สำหรับปุ่มเวลา
    def set_time_15(self, instance):
        self.selected_time = 15
        self.update_button_colors(self.btn_15)
        print(f"Time selected: {self.selected_time} seconds") # ปริ้นท์เช็คใน Console

    def set_time_30(self, instance):
        self.selected_time = 30
        self.update_button_colors(self.btn_30)
        print(f"Time selected: {self.selected_time} seconds")

    def set_time_60(self, instance):
        self.selected_time = 60
        self.update_button_colors(self.btn_60)
        print(f"Time selected: {self.selected_time} seconds")

    def update_button_colors(self, active_btn):
        # รีเซ็ตทุกปุ่มให้เป็นสีเทา
        self.btn_15.background_color = (0.5, 0.5, 0.5, 1)
        self.btn_30.background_color = (0.5, 0.5, 0.5, 1)
        self.btn_60.background_color = (0.5, 0.5, 0.5, 1)
        active_btn.background_color = (0.2, 0.7, 0.3, 1) 
        

    def go_back(self, instance):
        self.manager.current = 'menu'


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        layout.add_widget(Label(text="Game Screen", font_size=40))
        
        finish_btn = Button(text="Simulate Finish (Go to Result)", font_size=30, size_hint=(1, 0.2), background_color=(0.8, 0.5, 0.2, 1))
        finish_btn.bind(on_press=self.go_to_result)
        
        back_btn = Button(text="Give Up (Back to Menu)", font_size=30, size_hint=(1, 0.2))
        back_btn.bind(on_press=self.go_back)
        
        layout.add_widget(finish_btn) 
        layout.add_widget(back_btn)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'menu'
    def go_to_result(self, instance):
        self.manager.current = 'result'

class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        # สร้าง Widget (Labels, Buttons)
        title_label = Label(text="GAME OVER", font_size=50, bold=True, size_hint=(1, 0.3))        
        self.wpm_label = Label(text="WPM: 0", font_size=40, size_hint=(1, 0.2))      
        self.acc_label = Label(text="Accuracy: 0%", font_size=40, size_hint=(1, 0.2))      
        play_again_btn = Button(text="Play Again", font_size=30, size_hint=(1, 0.15), background_color=(0.2, 0.7, 0.3, 1))
        menu_btn = Button(text="Main Menu", font_size=30, size_hint=(1, 0.15))
        
        #  Bind (เชื่อมปุ่มกับฟังก์ชัน)
        play_again_btn.bind(on_press=self.play_again)
        menu_btn.bind(on_press=self.go_to_menu)

        layout.add_widget(title_label)
        layout.add_widget(self.wpm_label)
        layout.add_widget(self.acc_label)
        layout.add_widget(play_again_btn)
        layout.add_widget(menu_btn)
        self.add_widget(layout)

    def play_again(self, instance):
        self.manager.current = 'game'
    def go_to_menu(self, instance):
        self.manager.current = 'menu'

class TypingTutorApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(ResultScreen(name='result'))
        return sm

if __name__ == '__main__':
    TypingTutorApp().run()