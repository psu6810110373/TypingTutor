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
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.animation import Animation

Window.size = (900, 600)
Window.clearcolor = get_color_from_hex('#1E1E2E')

WORDS_LIST = ["PYTHON", "KIVY", "GAME", "CLOUD", "LAVA", "TYPE", "WORD", "JUMP", "ESCAPE", "SURVIVE", "SCREEN", "BUTTON", "WIDGET", "CLASS", "CODING", "TUTOR"]

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        # ใส่ขอบดำให้ตัวหนังสืออ่านง่าย
        title_label = Label(text="TYPING TUTOR", font_size=60, bold=True, size_hint=(1, 0.4), color=get_color_from_hex('#89B4FA'), outline_color=(0,0,0,1), outline_width=3, font_name='Bungee-Regular.ttf')
        
        start_btn = Button(text="Start Game", font_size=30, size_hint=(1, 0.2), background_color= get_color_from_hex('#A6E3A1'),font_name='Bungee-Regular.ttf')
        settings_btn = Button(text="Settings", font_size=30, size_hint=(1, 0.2),background_color=get_color_from_hex('#89DCEB'),font_name='Bungee-Regular.ttf')
        exit_btn = Button(text="Exit", font_size=30, size_hint=(1, 0.2), background_color=get_color_from_hex('#F38BA8'),font_name='Bungee-Regular.ttf')
        
        start_btn.bind(on_press=self.go_to_game)
        settings_btn.bind(on_press=self.go_to_settings)
        exit_btn.bind(on_press=self.exit_app)
        
        layout.add_widget(title_label)
        layout.add_widget(start_btn)
        layout.add_widget(settings_btn)
        layout.add_widget(exit_btn)
        self.add_widget(layout)
        
    def go_to_game(self, instance):
        settings_screen = self.manager.get_screen('settings')
        game_screen = self.manager.get_screen('game')
        game_screen.time_limit = settings_screen.selected_time
        self.manager.current = 'game' 

        app = App.get_running_app()
        if hasattr(app, 'bgm') and app.bgm:
            app.bgm.play()
        
    def go_to_settings(self, instance):
        self.manager.current = 'settings'        
        
    def exit_app(self, instance):
        App.get_running_app().stop()

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        title = Label(text="SETTINGS", font_size=50, bold=True, size_hint=(1, 0.3),color=get_color_from_hex('#89B4FA'), outline_color=(0,0,0,1), outline_width=2, font_name='Bungee-Regular.ttf')
        subtitle = Label(text="Select Time Limit:", font_size=30, size_hint=(1, 0.1),color=get_color_from_hex('#CDD6F4'), outline_color=(0,0,0,1), outline_width=2, font_name='Bungee-Regular.ttf')

        time_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint=(1, 0.2))
        self.btn_15 = Button(text="15 Sec", font_size=30, background_color=(0.5, 0.5, 0.5, 1),font_name='Bungee-Regular.ttf')
        self.btn_30 = Button(text="30 Sec", font_size=30, background_color=(0.2, 0.7, 0.3, 1),font_name='Bungee-Regular.ttf') 
        self.btn_60 = Button(text="60 Sec", font_size=30, background_color=(0.5, 0.5, 0.5, 1),font_name='Bungee-Regular.ttf')
        
        self.btn_15.bind(on_press=self.set_time_15)
        self.btn_30.bind(on_press=self.set_time_30)
        self.btn_60.bind(on_press=self.set_time_60)

        time_layout.add_widget(self.btn_15)
        time_layout.add_widget(self.btn_30)
        time_layout.add_widget(self.btn_60)

        back_btn = Button(text="Back to Menu", font_size=30, size_hint=(1, 0.2),background_color=get_color_from_hex('#F38BA8'),font_name='Bungee-Regular.ttf')
        back_btn.bind(on_press=self.go_back)

        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(time_layout)
        layout.add_widget(back_btn)
        self.add_widget(layout)

        self.selected_time = 30

    def set_time_15(self, instance):
        self.selected_time = 15
        self.update_button_colors(self.btn_15)

    def set_time_30(self, instance):
        self.selected_time = 30
        self.update_button_colors(self.btn_30)

    def set_time_60(self, instance):
        self.selected_time = 60
        self.update_button_colors(self.btn_60)

    def update_button_colors(self, active_btn):
        self.btn_15.background_color = (0.5, 0.5, 0.5, 1)
        self.btn_30.background_color = (0.5, 0.5, 0.5, 1)
        self.btn_60.background_color = (0.5, 0.5, 0.5, 1)
        active_btn.background_color = (0.2, 0.7, 0.3, 1) 

    def go_back(self, instance):
        self.manager.current = 'menu'

class PlayerShip(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (80, 80)
        self.pos = (Window.width/2 - 40, 250) 
        with self.canvas:
            self.rect = Rectangle(source='pixel-rocket-launch-retro-8-bit-spacecraft-spaceship-icon-in-flat-design-png.png', pos=self.pos, size=self.size)
        self.bind(pos=self.update_graphics_pos)
        
    def update_graphics_pos(self, instance, value):
        self.rect.pos = instance.pos

class WordItem(RelativeLayout):
    def __init__(self, text='', **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (150, 80)
        self.pos = (random.randint(50, Window.width - 200), Window.height)
        self.speed = random.uniform(50, 100)
        self.text = text
        
        # แก้คำเตือนสีเหลือง: ใช้ fit_mode='fill'
        self.bg_image = Image(source='pngtree-pixel-art-white-cloud-graphic-illustration-vector-png-image_16480394.png', fit_mode='fill')
        self.add_widget(self.bg_image)
        
        # คำศัพท์สีดำขอบขาว (เด่นชัดบนก้อนเมฆ)
        self.label = Label(text=text, font_size=25, font_name='Bungee-Regular.ttf', color=(0,0,0,1), outline_color=(1,1,1,1), outline_width=1, bold=True)
        self.add_widget(self.label)

class Lava(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.size = (Window.width, 100) 
        self.pos = (0, 0) 
        with self.canvas:
            Color(rgba=get_color_from_hex('#F38BA8')) 
            self.rect = Rectangle(pos=self.pos, size=self.size)

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time_limit = 30
        self.game_active = False
        
        self.correct_sound = SoundLoader.load('correct_sound.mp3')
        self.wrong_sound = SoundLoader.load('wrong_sound.mp3')
        self.gameover_sound = SoundLoader.load('gameover_sound.mp3')
        self.drop_sound = SoundLoader.load('wrong_sound.mp3') 
        
        self.bg_images = ['istockphoto-2080254800-640x640.jpg','istockphoto-1208374725-612x612.jpg']
        self.current_bg_index = 0

    def on_enter(self):
        self.clear_widgets()
        
        # แก้คำเตือนสีเหลือง: ใช้ fit_mode='fill'
        self.bg = Image(source=self.bg_images[self.current_bg_index], fit_mode='fill', color=(0.4, 0.4, 0.4, 1))
        self.add_widget(self.bg)
        
        self.lava = Lava()
        self.add_widget(self.lava)
        
        self.player = PlayerShip()
        self.player.pos = (Window.width/2 - 40, 250) 
        self.add_widget(self.player)
        
        self.hud_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), pos=(0, Window.height - 50))
        
        # ใส่ขอบดำให้ตัวเลขเวลาและคะแนน
        self.time_label = Label(text=f"Time: {self.time_limit}", font_size=35, color=get_color_from_hex('#89B4FA'), outline_color=(0,0,0,1), outline_width=2, font_name='Bungee-Regular.ttf')
        self.score_label = Label(text="Score: 0", font_size=35, color=get_color_from_hex('#A6E3A1'), outline_color=(0,0,0,1), outline_width=2, font_name='Bungee-Regular.ttf')
        
        self.hud_layout.add_widget(self.time_label)
        self.hud_layout.add_widget(self.score_label)
        self.add_widget(self.hud_layout)

        # สีขาวขอบดำหนาๆ ชัดเจนทุกสถานการณ์แน่นอน
        self.current_input = Label(text="TYPE HERE...", font_size=40, size_hint=(None, None), size=(200, 50), pos=(self.player.pos[0] - 60, self.player.pos[1] + 90), color=(1, 1, 1, 1), outline_color=(0,0,0,1), outline_width=2, font_name='Bungee-Regular.ttf')
        self.add_widget(self.current_input)

        give_up_btn = Button(text="Give Up", font_size=20, size_hint=(None, None), size=(150, 50), pos=(Window.width - 160, 10), background_color=get_color_from_hex('#F38BA8'), font_name='Bungee-Regular.ttf')
        give_up_btn.bind(on_press=self.give_up)
        self.add_widget(give_up_btn)

        self.words = []
        self.score = 0
        self.time_left = float(self.time_limit)
        self.spawn_timer = 0
        self.typed_word = ""
        
        Window.bind(on_key_down=self._on_keyboard_down)
        
        self.game_active = True
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.change_background, 15.0)

    def change_background(self, dt):
        if not self.game_active: return
        anim_out = Animation(color=(0, 0, 0, 1), duration=1.0) 
        
        def on_fade_complete(*args):
            self.current_bg_index = (self.current_bg_index + 1) % len(self.bg_images)
            self.bg.source = self.bg_images[self.current_bg_index]
            anim_in = Animation(color=(0.4, 0.4, 0.4, 1), duration=1.0)
            anim_in.start(self.bg)
            
        anim_out.bind(on_complete=on_fade_complete)
        anim_out.start(self.bg)

    def give_up(self, instance):
        app = App.get_running_app()
        if hasattr(app, 'bgm') and app.bgm:
            app.bgm.stop()
        self.manager.current = 'menu'
    
    def on_leave(self):
        Clock.unschedule(self.update)
        Clock.unschedule(self.change_background)
        Window.unbind(on_key_down=self._on_keyboard_down)
        self.game_active = False

    def update(self, dt):
        if not self.game_active: return

        self.time_left -= dt
        self.time_label.text = f"Time: {int(self.time_left)}"
        if self.time_left <= 0:
            self.end_game(win=True) 
            return

        self.spawn_timer += dt
        if self.spawn_timer > 1.5:
            self.spawn_timer = 0
            new_word_text = random.choice(WORDS_LIST)
            new_word = WordItem(text=new_word_text)
            self.words.append(new_word)
            self.add_widget(new_word)

        for word_widget in self.words[:]:
            word_widget.pos = (word_widget.pos[0], word_widget.pos[1] - word_widget.speed * dt)
            
            if word_widget.pos[1] <= self.lava.size[1]:
                if self.drop_sound: self.drop_sound.play() 
                self.remove_widget(word_widget)
                self.words.remove(word_widget)
                
                new_y = self.player.pos[1] - 40
                self.player.pos = (self.player.pos[0], new_y)
                self.current_input.pos = (self.player.pos[0] - 60, self.player.pos[1] + 90)
                
                if self.player.pos[1] <= self.lava.size[1]:
                    self.end_game(win=False)
                    return

    def end_game(self, win):
        self.game_active = False
        Clock.unschedule(self.update)
        Clock.unschedule(self.change_background)
        Window.unbind(on_key_down=self._on_keyboard_down)
        
        app = App.get_running_app()
        if hasattr(app, 'bgm') and app.bgm:
            app.bgm.stop()

        if not win and self.gameover_sound:
            self.gameover_sound.play()
            
        result_screen = self.manager.get_screen('result')
        result_screen.set_result(
            win=win, 
            score=self.score, 
            time_survived=float(self.time_limit) - self.time_left
        )
        self.manager.current = 'result'

    def _on_keyboard_down(self, window, keycode, scancode, text, modifiers):
        if not self.game_active: return False
            
        if keycode == 8: 
            self.typed_word = self.typed_word[:-1]
        elif keycode in (13, 271, 32): 
            self.check_word()
        elif text and text.isalpha(): 
            self.typed_word += text.upper()
            
        self.current_input.text = self.typed_word
        return True

    def check_word(self):
        matched = False
        for word_widget in self.words:
            if word_widget.text == self.typed_word:
                self.remove_widget(word_widget)
                self.words.remove(word_widget)
                self.score += 1
                self.score_label.text = f"Score: {self.score}"
                
                if self.correct_sound:
                    self.correct_sound.play()
                
                new_y = min(Window.height - 150, self.player.pos[1] + 30)
                self.player.pos = (self.player.pos[0], new_y)
                self.current_input.pos = (self.player.pos[0] - 60, self.player.pos[1] + 90)
                
                matched = True
                break
                
        if not matched and len(self.typed_word) > 0:
            if self.wrong_sound:
                self.wrong_sound.play()
                
        self.typed_word = ""
        self.current_input.text = self.typed_word
        
class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        self.title_label = Label(text="GAME OVER", font_size=60, bold=True, size_hint=(1, 0.3),color=get_color_from_hex('#F38BA8'), outline_color=(0,0,0,1), outline_width=2, font_name='Bungee-Regular.ttf')        
        self.wpm_label = Label(text="WPM: 0", font_size=40, size_hint=(1, 0.2),color=get_color_from_hex('#A6E3A1'), outline_color=(0,0,0,1), outline_width=2, font_name='Bungee-Regular.ttf')      
        self.acc_label = Label(text="Score: 0", font_size=40, size_hint=(1, 0.2),color=get_color_from_hex('#F9E2AF'), outline_color=(0,0,0,1), outline_width=2, font_name='Bungee-Regular.ttf')      
        
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
            self.title_label.color = get_color_from_hex('#A6E3A1') 
        else:
            self.title_label.text = "GAME OVER"
            self.title_label.color = get_color_from_hex('#F38BA8') 
            
        minutes = max(time_survived / 60.0, 0.01)
        wpm = round(score / minutes)
        
        self.wpm_label.text = f"WPM: {wpm}"
        self.acc_label.text = f"Score: {score}"

    def play_again(self, instance):
        app = App.get_running_app()
        if hasattr(app, 'bgm') and app.bgm:
            app.bgm.play()
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
        
        # เพลงบรรยากาศหน้า UI (BGM) ยังคงอยู่ปกติ
        self.bgm = SoundLoader.load('marmixer-georgia-484621.mp3')
        if self.bgm:
            self.bgm.loop = True
            self.bgm.volume = 0.4 
            
        return sm

if __name__ == '__main__':
    TypingTutorApp().run()