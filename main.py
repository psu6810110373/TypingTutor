import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
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
        title_label = Label(text="TYPING TUTOR", font_size=50, bold=True, size_hint=(1, 0.4),color=get_color_from_hex('#89B4FA'),font_name='Bungee-Regular.ttf')
        
        # สร้าง Widget (Buttons)
        start_btn = Button(text="Start Game", font_size=30, size_hint=(1, 0.2), background_color= get_color_from_hex('#A6E3A1'),font_name='Bungee-Regular.ttf')
        settings_btn = Button(text="Settings", font_size=30, size_hint=(1, 0.2),background_color=get_color_from_hex('#89DCEB'),font_name='Bungee-Regular.ttf')
        exit_btn = Button(text="Exit", font_size=30, size_hint=(1, 0.2), background_color=get_color_from_hex('#F38BA8'),font_name='Bungee-Regular.ttf')
        
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
        title = Label(text="SETTINGS", font_size=50, bold=True, size_hint=(1, 0.3),color=get_color_from_hex('#89B4FA'),font_name='Bungee-Regular.ttf')
        subtitle = Label(text="Select Time Limit:", font_size=30, size_hint=(1, 0.1),color=get_color_from_hex('#CDD6F4'),font_name='Bungee-Regular.ttf')

        # สร้าง Widget (Buttons สำหรับเลือกเวลา)
        time_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint=(1, 0.2))
        self.btn_15 = Button(text="15 Sec", font_size=30, background_color=(0.5, 0.5, 0.5, 1),font_name='Bungee-Regular.ttf')
        self.btn_30 = Button(text="30 Sec", font_size=30, background_color=(0.2, 0.7, 0.3, 1),font_name='Bungee-Regular.ttf') 
        self.btn_60 = Button(text="60 Sec", font_size=30, background_color=(0.5, 0.5, 0.5, 1),font_name='Bungee-Regular.ttf')
        
        # ผูก Callbacks ให้ตรวจจับการกดปุ่ม
        self.btn_15.bind(on_press=self.set_time_15)
        self.btn_30.bind(on_press=self.set_time_30)
        self.btn_60.bind(on_press=self.set_time_60)

        #นำปุ่มเวลาใส่ในlayout
        time_layout.add_widget(self.btn_15)
        time_layout.add_widget(self.btn_30)
        time_layout.add_widget(self.btn_60)

        #ปุ่มเมนูหลัก
        back_btn = Button(text="Back to Menu", font_size=30, size_hint=(1, 0.2),background_color=get_color_from_hex('#F38BA8'),font_name='Bungee-Regular.ttf')
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
        self.layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        # --- แถบสถานะด้านบน ---
        self.stats_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        self.time_label = Label(text="Time: 00", font_size=40, color=get_color_from_hex('#F9E2AF'), font_name='Bungee-Regular.ttf')
        self.wpm_label = Label(text="WPM: 0", font_size=40, color=get_color_from_hex('#A6E3A1'), font_name='Bungee-Regular.ttf')
        self.acc_label = Label(text="Acc: 0%", font_size=40, color=get_color_from_hex('#89B4FA'), font_name='Bungee-Regular.ttf')
        
        self.stats_layout.add_widget(self.time_label)
        self.stats_layout.add_widget(self.wpm_label)
        self.stats_layout.add_widget(self.acc_label)
        
        self.layout.add_widget(self.stats_layout)
        # --- พื้นที่แสดงคำศัพท์ ---
        self.word_display = Label(text="Loading...", font_size=60, size_hint=(1, 0.6), font_name='Bungee-Regular.ttf', markup=True)
        self.layout.add_widget(self.word_display)
        # --- ปุ่มยอมแพ้ ---
        self.back_btn = Button(text="Give Up", font_size=30, size_hint=(1, 0.2), background_color=get_color_from_hex('#F38BA8'), font_name='Bungee-Regular.ttf')
        self.back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_btn)
        self.add_widget(self.layout)

        # --- ตัวแปรสำหรับคำนวณเกม ---
        self.time_left = 0
        self.total_keystrokes = 0
        self.correct_keystrokes = 0
        self.is_playing = False
        self.word_list = ["python", "keyboard", "developer", "kivy", "variable", "function", "screen", "button", "project", "system"]
        self.current_word = ""

    def go_back(self, instance):
        self.manager.current = 'menu'

    def update_labels(self):
        self.time_label.text = f"Time: {self.time_left}"

    def start_game(self):
        # ดึงเวลามาจากหน้า Settings ที่คนที่ 1 ทำไว้
        settings_screen = self.manager.get_screen('settings')
        self.time_left = settings_screen.selected_time
        
        # รีเซ็ตค่าคะแนนต่างๆ
        self.total_keystrokes = 0
        self.correct_keystrokes = 0
        self.is_playing = True

        self.wpm_label.text = "WPM: 0"
        self.acc_label.text = "Acc: 0%"

        self.time_label.color = get_color_from_hex('#F9E2AF')
        
        self.update_labels()
        # สั่งให้นาฬิกาเดิน (เรียกฟังก์ชัน update_timer ทุกๆ 1 วินาที)
        Clock.schedule_interval(self.update_timer, 1.0)

        Window.bind(on_key_down=self._on_keyboard_down)
    
    def update_timer(self, dt):
        if self.time_left > 0:
            self.time_left -= 1
            self.update_labels()

            if self.time_left <= 5:
                self.time_label.color = get_color_from_hex('#F38BA8')
        else:
            self.end_game()

    def stop_game(self):
        self.is_playing = False
        Clock.unschedule(self.update_timer) # สั่งหยุดนาฬิกา

        Window.unbind(on_key_down=self._on_keyboard_down)

    def end_game(self):
        self.stop_game()
        result_screen = self.manager.get_screen('result')
        result_screen.wpm_label.text = self.wpm_label.text
        result_screen.acc_label.text = self.acc_label.text
        self.manager.current = 'result'

    def on_enter(self):
        self.start_game()

    def on_leave(self):
        self.stop_game()

    def _on_keyboard_down(self, window, key, scancode, codepoint, modifier):
        # ถ้าเกมยังไม่เริ่ม หรือกดปุ่มแปลกๆ (Shift, Ctrl) ให้ข้ามไป
        if not self.is_playing or codepoint is None:
            return False
        self.total_keystrokes += 1
        self.correct_keystrokes += 1 # สมมติว่าพิมพ์ถูกทุกตัวไปก่อน

        print(f"Key pressed: {codepoint}")

        self.calculate_stats()
            
        return True
    
    def calculate_stats(self):
        settings_time = self.manager.get_screen('settings').selected_time
        time_elapsed = settings_time - self.time_left
        
        if time_elapsed > 0:
            # --- ลบ pass ทิ้ง แล้วใส่โค้ดนี้แทน ---
            words_typed = self.correct_keystrokes / 5.0
            minutes_elapsed = time_elapsed / 60.0
            wpm = int(words_typed / minutes_elapsed)

            if self.total_keystrokes > 0:
                acc = int((self.correct_keystrokes / self.total_keystrokes) * 100) 
            else:
                acc = 0

            self.wpm_label.text = f"WPM: {wpm}"
            self.acc_label.text = f"Acc: {acc}%"

class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        # สร้าง Widget (Labels, Buttons)
        title_label = Label(text="GAME OVER", font_size=50, bold=True, size_hint=(1, 0.3),color=get_color_from_hex('#F38BA8'),font_name='Bungee-Regular.ttf')        
        self.wpm_label = Label(text="WPM: 0", font_size=40, size_hint=(1, 0.2),color=get_color_from_hex('#A6E3A1'),font_name='Bungee-Regular.ttf')      
        self.acc_label = Label(text="Accuracy: 0%", font_size=40, size_hint=(1, 0.2),color=get_color_from_hex('#F9E2AF'),font_name='Bungee-Regular.ttf')      
        play_again_btn = Button(text="Play Again", font_size=30, size_hint=(1, 0.15),background_color=get_color_from_hex('#A6E3A1'),font_name='Bungee-Regular.ttf')
        menu_btn = Button(text="Main Menu", font_size=30, size_hint=(1, 0.15),background_color=get_color_from_hex('#89DCEB'),font_name='Bungee-Regular.ttf')
        
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