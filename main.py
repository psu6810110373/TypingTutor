import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.core.audio import SoundLoader
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse

Window.size = (900, 600)
Window.clearcolor = get_color_from_hex('#1E1E2E')

WORDS_LIST = ["PYTHON", "KIVY", "GAME", "CLOUD", "LAVA", "TYPE", "WORD", "JUMP", "ESCAPE", "SURVIVE", "SCREEN", "BUTTON", "WIDGET", "CLASS", "CODING", "TUTOR"]


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
        App.get_running_app().play_click_sound()
        settings_screen = self.manager.get_screen('settings')
        game_screen = self.manager.get_screen('game')
        game_screen.time_limit = settings_screen.selected_time
        self.manager.current = 'game' 
    def go_to_settings(self, instance):
        App.get_running_app().play_click_sound()
        self.manager.current = 'settings'        
    def exit_app(self, instance):
        App.get_running_app().play_click_sound()
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
        App.get_running_app().play_click_sound()
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

class PlayerCloud(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (100, 50)
        # ตั้งตำแหน่งให้อยู่ตรงกลางจอ และลอยสูงขึ้นมาที่พิกัด Y=250
        self.pos = (Window.width/2 - 50, 250) 
        with self.canvas:
            Color(0.8, 0.9, 1, 1) # สีฟ้าขาว (ก้อนเมฆ)
            self.rect = Ellipse(pos=self.pos, size=self.size)
        self.bind(pos=self.update_graphics_pos)
        
    def update_graphics_pos(self, instance, value):
        self.rect.pos = instance.pos

class WordItem(Label):
    def __init__(self, text='', **kwargs):
        kwargs['text'] = text
        super().__init__(**kwargs)
        self.font_size = 30
        self.font_name = 'Bungee-Regular.ttf'
        self.color = get_color_from_hex('#CDD6F4')
        self.size_hint = (None, None)
        self.size = (150, 50)
        self.valign = 'center'
        self.halign = 'center'
        # สุ่มให้เกิดแบบสุ่มแกน X และอยู่บนสุดของจอ (แกน Y)
        self.pos = (random.randint(50, Window.width - 200), Window.height)
        self.speed = random.uniform(50, 100) # ความเร็วในการตก

class Lava(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.size = (Window.width, 100) # ลาวาสูง 100
        self.pos = (0, 0) # อยู่ติดขอบล่างสุด
        with self.canvas:
            Color(rgba=get_color_from_hex('#F38BA8')) # สีแดงลาวา
            self.rect = Rectangle(pos=self.pos, size=self.size)

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time_limit = 30
        self.game_active = False

    def on_enter(self):
        # 1. ล้างหน้าจอเก่าทิ้งทั้งหมด
        self.clear_widgets()
        
        # 2. วางลาวา และ เมฆผู้เล่น
        self.lava = Lava()
        self.add_widget(self.lava)
        
        self.player = PlayerCloud()
        self.player.pos = (Window.width/2 - 50, 250) 
        self.add_widget(self.player)
        
        # 3. สร้างแถบ HUD ด้านบน (เวลา, พลังชีวิต, คะแนน)
        self.hud_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), pos=(0, Window.height - 50))
        self.time_label = Label(text=f"Time: {self.time_limit}", font_size=30, color=get_color_from_hex('#89B4FA'), font_name='Bungee-Regular.ttf')
        self.health_label = Label(text="Health: 3", font_size=30, color=get_color_from_hex('#F38BA8'), font_name='Bungee-Regular.ttf')
        self.score_label = Label(text="Score: 0", font_size=30, color=get_color_from_hex('#A6E3A1'), font_name='Bungee-Regular.ttf')
        
        self.hud_layout.add_widget(self.time_label)
        self.hud_layout.add_widget(self.health_label)
        self.hud_layout.add_widget(self.score_label)
        self.add_widget(self.hud_layout)

        # 4. ข้อความสำหรับแสดงคำที่เรากำลังพิมพ์ (ลอยอยู่บนก้อนเมฆ)
        self.current_input = Label(text="TYPE HERE...", font_size=40, size_hint=(None, None), size=(200, 50), pos=(Window.width/2 - 100, self.player.pos[1] + 60), color=get_color_from_hex('#F9E2AF'), font_name='Bungee-Regular.ttf')
        self.add_widget(self.current_input)

        # 5. ปุ่มยอมแพ้ (ย้ายไปไว้มุมขวาล่าง)
        give_up_btn = Button(text="Give Up", font_size=20, size_hint=(None, None), size=(150, 50), pos=(Window.width - 160, 10), background_color=get_color_from_hex('#F38BA8'), font_name='Bungee-Regular.ttf')
        give_up_btn.bind(on_press=self.give_up)
        self.add_widget(give_up_btn)

        # 6. รีเซ็ตตัวแปรเกม (เตรียมพร้อมสำหรับสเต็ป 3)
        self.words = []
        self.health = 3
        self.score = 0
        self.time_left = float(self.time_limit)
        self.spawn_timer = 0
        self.typed_word = ""
        self.game_active = True
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def give_up(self, instance):
        self.manager.current = 'menu'
    
    def on_leave(self):
        # ปิดการทำงานเมื่อออกจากหน้าจอ
        Clock.unschedule(self.update)
        self.game_active = False

    def update(self, dt):
        if not self.game_active:
            return

        # 1. ลดเวลาลงเรื่อยๆ
        self.time_left -= dt
        self.time_label.text = f"Time: {int(self.time_left)}"
        
        if self.time_left <= 0:
            self.end_game(win=True) # เวลาหมด = รอดตาย!
            return

        # 2. สุ่มสร้างก้อนเมฆคำศัพท์ใหม่ ทุกๆ 1.5 วินาที
        self.spawn_timer += dt
        if self.spawn_timer > 1.5:
            self.spawn_timer = 0
            new_word_text = random.choice(WORDS_LIST)
            new_word = WordItem(text=new_word_text)
            self.words.append(new_word)
            self.add_widget(new_word)

        # 3. ทำให้เมฆทุกก้อนตกลงมา และเช็คการชน
        for word_widget in self.words[:]:
            word_widget.pos = (word_widget.pos[0], word_widget.pos[1] - word_widget.speed * dt)
            
            # ถ้าคำศัพท์ร่วงแตะลาวา
            if word_widget.pos[1] <= self.lava.size[1]:
                self.remove_widget(word_widget)
                self.words.remove(word_widget)
                
                # หักเลือด และดึงตัวละครให้ต่ำลง
                self.health -= 1
                self.health_label.text = f"Health: {self.health}"
                new_y = self.player.pos[1] - 40
                self.player.pos = (self.player.pos[0], new_y)
                self.current_input.pos = (Window.width/2 - 100, self.player.pos[1] + 60)
                
                # ถ้าตัวละครแตะลาวา หรือ เลือดหมด = ตาย!
                if self.player.pos[1] <= self.lava.size[1] or self.health <= 0:
                    self.end_game(win=False)
                    return

    def end_game(self, win):
        self.game_active = False
        Clock.unschedule(self.update)
        
        # ส่งค่าไปหน้าจอสรุปผล
        result_screen = self.manager.get_screen('result')
        result_screen.set_result(
            win=win, 
            score=self.score, 
            time_survived=float(self.time_limit) - self.time_left
        )
        self.manager.current = 'result'

class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        self.title_label = Label(text="GAME OVER", font_size=50, bold=True, size_hint=(1, 0.3),color=get_color_from_hex('#F38BA8'),font_name='Bungee-Regular.ttf')        
        self.wpm_label = Label(text="WPM: 0", font_size=40, size_hint=(1, 0.2),color=get_color_from_hex('#A6E3A1'),font_name='Bungee-Regular.ttf')      
        self.acc_label = Label(text="Score: 0", font_size=40, size_hint=(1, 0.2),color=get_color_from_hex('#F9E2AF'),font_name='Bungee-Regular.ttf')      
        
        play_again_btn = Button(text="Play Again", font_size=30, size_hint=(1, 0.15),background_color=get_color_from_hex('#A6E3A1'),font_name='Bungee-Regular.ttf')
        menu_btn = Button(text="Main Menu", font_size=30, size_hint=(1, 0.15),background_color=get_color_from_hex('#89DCEB'),font_name='Bungee-Regular.ttf')
        
        play_again_btn.bind(on_press=self.play_again)
        menu_btn.bind(on_press=self.go_to_menu)

        layout.add_widget(self.title_label)
        layout.add_widget(self.wpm_label)
        layout.add_widget(self.acc_label)
        layout.add_widget(play_again_btn)
        layout.add_widget(menu_btn)
        self.add_widget(layout)

    def set_result(self, win, score, time_survived):
        if win:
            self.title_label.text = "YOU SURVIVED!"
            self.title_label.color = get_color_from_hex('#A6E3A1') # สีเขียว
        else:
            self.title_label.text = "GAME OVER"
            self.title_label.color = get_color_from_hex('#F38BA8') # สีแดง
            
        minutes = max(time_survived / 60.0, 0.01)
        wpm = round(score / minutes)
        
        self.wpm_label.text = f"WPM: {wpm}"
        self.acc_label.text = f"Score: {score}"

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
        self.click_sound = SoundLoader.load('click_sound.wav')
        return sm
    
    def play_click_sound(self):
        if self.click_sound:
            self.click_sound.play()

if __name__ == '__main__':
    TypingTutorApp().run()