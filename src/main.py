from kivy.config import Config

Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')
Config.set('graphics', 'resizable', True)

from kivy import platform
import os
from pathlib import Path

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.lang.builder import Builder
from kivy.resources import resource_add_path


# ============================================================
# PATH CONFIGURATION
# ============================================================

APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent

FONTS_DIR = PROJECT_ROOT / 'fonts'
IMAGES_DIR = PROJECT_ROOT / 'images'
AUD_DIR = PROJECT_ROOT / 'audio'

resource_add_path(str(FONTS_DIR))
resource_add_path(str(IMAGES_DIR))
resource_add_path(str(AUD_DIR))

try:
    os.chdir(APP_DIR)
except Exception:
    pass


# ============================================================
# KV FILES
# ============================================================

Builder.load_file('menu.kv')
Builder.load_file('modes.kv')
# Builder.load_file('nebula.kv')


# ============================================================
# MAIN GAME WIDGET
# ============================================================

class MainWidget(RelativeLayout):

    # Game construction
    from build import (
        build_hlines,
        build_ship,
        build_tiles,
        build_vlines,
        generate_tiles_coordinates,
        get_lineh_from_index,
        get_linev_from_index,
        get_tile_coordinates
    )

    # Game updates
    from updates import (
        update_best_score,
        update_hlines,
        update_ship,
        update_tiles,
        update_vlines,
        check_collision,
        get_check_coordinates
    )

    # Perspective
    from transforms import transform, transform_perspective

    # Controls
    from user_interactions import (
        on_keyboard_down,
        on_touch_down,
        keyboard_closed,
        h_movement
    )

    # --------------------------------------------------------
    # UI REFERENCES
    # --------------------------------------------------------

    modes_widget = ObjectProperty()
    menu_widget = ObjectProperty()

    # --------------------------------------------------------
    # PERSPECTIVE
    # --------------------------------------------------------

    perspective_x = NumericProperty(0)
    perspective_y = NumericProperty(0)

    # --------------------------------------------------------
    # TRACK
    # --------------------------------------------------------

    vlines_number = 8
    vlines_spacing = 0.3
    vlines = []

    hlines_number = 8
    hlines_spacing = 0.2
    hlines = []

    # --------------------------------------------------------
    # TILES
    # --------------------------------------------------------

    tiles = []
    tiles_coordinates = []

    tiles_number_started = 30
    tiles_number_not_started = 8

    # --------------------------------------------------------
    # SHIP
    # --------------------------------------------------------

    ship = None
    ship_width = 0.1
    ship_height = 0.035
    ship_base = 0.04
    ship_point = ()

    # --------------------------------------------------------
    # GAME STATE
    # --------------------------------------------------------

    current_loop = 0
    current_offset = 0
    last_y = 0
    movement = 0

    speed = 8
    score = 0
    best_score = 0

    state_game_over = False
    state_game_started = False

    # --------------------------------------------------------
    # MENU TEXT
    # --------------------------------------------------------

    menu_title = StringProperty("S T A R   D R I V E")
    menu_button_title = StringProperty("START")
    menu_modes_title = StringProperty("MODES")

    score_label = StringProperty("SCORE: 0")
    best_score_label = StringProperty("BEST: 0")

    # --------------------------------------------------------
    # MODE SYSTEM
    # --------------------------------------------------------

    mode_speed = StringProperty('normal')
    mode_width = StringProperty('normal')

    base_speed = NumericProperty(8)

    MODE_SPEEDS = {
        'normal': 8,
        'turtle': 5,
        'sonic': 12,
    }

    MODE_VLINES = {
        'normal': 8,
        'tight': 4,
        'wide': 20,
    }

    # --------------------------------------------------------
    # INIT
    # --------------------------------------------------------

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

        self.build_vlines()
        self.build_hlines()
        self.build_tiles()
        self.build_ship()

        self.generate_tiles_coordinates()
        self.load()

        self.width = self.width
        self.height = self.height

        self.label = None

        if self.is_pc():
            self._keyboard = Window.request_keyboard(
                self.keyboard_closed,
                self
            )

            if self._keyboard:
                self._keyboard.bind(
                    on_key_down=self.on_keyboard_down
                )

        Clock.schedule_interval(
            self.update,
            1 / 60
        )

    # ========================================================
    # GAME RESET
    # ========================================================

    def reset_game(self):
        self.current_loop = 0
        self.current_offset = 0
        self.last_y = 0
        self.movement = 0

        self.speed = self.base_speed
        self.score = 0

        self.tiles_coordinates.clear()

        self.load()
        self.generate_tiles_coordinates()

        self.state_game_started = True
        self.state_game_over = False

        self.menu_title = "S T A R   D R I V E"
        self.menu_button_title = "START"
        self.menu_modes_title = "MODES"

    # ========================================================
    # LOAD BEST SCORE
    # ========================================================

    def load(self):
        best_score_path = APP_DIR / 'best_score.txt'

        try:
            with open(best_score_path, 'r') as file:
                self.best_score = str(file.readline()).strip() or '0'

        except FileNotFoundError:
            self.best_score = 0

        try:
            if int(self.best_score) <= 30:
                self.best_score = 0

        except ValueError:
            self.best_score = 0

    # ========================================================
    # PLATFORM
    # ========================================================

    def is_pc(self):
        return platform in ('linux', 'win', 'macosx')

    # ========================================================
    # WINDOW SIZE
    # ========================================================

    def on_size(self, *args):
        self.perspective_x = self.width / 2
        self.perspective_y = self.height * 0.75

    # ========================================================
    # TUTORIAL
    # ========================================================

    def tutorial(self):

        if int(self.best_score) < 30:

            if self.label is None:

                self.label = Label(
                    text='WELCOME PILOT',
                    font_name='Sackers-Gothic-Std-Light.ttf',
                    font_size=self.width * 0.023,
                    pos_hint={
                        'center_x': 0.5,
                        'center_y': 0.88
                    },
                    color=(0.7, 0.95, 1, 1)
                )

                self.add_widget(self.label)

            if (
                int(self.best_score) < 20
                and int(self.best_score) > 5
                and not self.is_pc()
            ):
                self.label.text = (
                    'TOUCH LEFT OR RIGHT TO PILOT'
                )

            if (
                int(self.best_score) < 20
                and int(self.best_score) > 5
                and self.is_pc()
            ):
                self.label.text = (
                    'USE  ←  /  →  TO PILOT'
                )

            if (
                int(self.best_score) < 29
                and int(self.best_score) > 19
            ):
                self.label.text = (
                    'KEEP THE SHIP ON THE WHITE TRACK'
                )

            if int(self.best_score) == 29:
                self.label.text = ''

    # ========================================================
    # GAME UPDATE LOOP
    # ========================================================

    def update(self, time):

        time_fix = time * 60

        self.update_vlines()
        self.update_hlines()
        self.update_tiles()
        self.update_ship()
        self.update_best_score()

        self.best_score_label = (
            "BEST: " + str(self.best_score)
        )

        if not self.state_game_over:

            self.generate_tiles_coordinates()

            self.score_label = (
                "SCORE: " + str(self.score)
            )

            spacing_y = (
                self.hlines_spacing * self.height
            )

            while self.current_offset >= spacing_y:
                self.current_offset -= spacing_y
                self.current_loop += 1

            self.current_offset += (
                time_fix
                * self.speed
                * self.height
                / 1000
            )

        # ----------------------------------------------------
        # ACTIVE GAME
        # ----------------------------------------------------

        if (
            not self.state_game_over
            and self.state_game_started
        ):

            self.score = self.current_loop

            if self.speed < 25:
                self.speed += (
                    self.current_loop * 0.00005
                )

            if (
                not self.get_check_coordinates()
                and not self.state_game_over
                and int(self.best_score) > 29
            ):

                self.state_game_over = True

                self.menu_title = (
                    "G A M E   O V E R"
                )

                self.menu_button_title = "RESTART"
                self.menu_modes_title = "MENU"

                self.show_menu()

        # ----------------------------------------------------
        # TUTORIAL
        # ----------------------------------------------------

        if (
            int(self.best_score) < 30
            and self.state_game_started
        ):
            self.tutorial()

    # ========================================================
    # SHOW MENU
    # ========================================================

    def show_menu(self):

        if self.menu_widget is None:
            return

        self.menu_widget.opacity = 0

        Animation(
            opacity=1,
            duration=0.35,
            transition='out_quad'
        ).start(self.menu_widget)

    # ========================================================
    # HIDE MENU
    # ========================================================

    def hide_menu(self):

        if self.menu_widget is None:
            return

        Animation(
            opacity=0,
            duration=0.25,
            transition='in_quad'
        ).start(self.menu_widget)

    # ========================================================
    # MENU / MODES
    # ========================================================

    def on_menu_modes(self):

        if self.menu_modes_title == "MODES":

            self.state_game_over = False
            self.state_game_started = False

            self.hide_menu()

            if self.modes_widget:
                Animation(
                    opacity=1,
                    duration=0.3,
                    transition='out_quad'
                ).start(self.modes_widget)

        elif self.menu_modes_title == "MENU":

            self.current_loop = 0
            self.current_offset = 0
            self.last_y = 0
            self.movement = 0

            self.speed = self.base_speed
            self.score = 0

            self.state_game_started = False

            self.tiles_coordinates.clear()
            self.generate_tiles_coordinates()
            self.update_tiles()

            self.apply_selected_modes()

            self.state_game_over = False

            self.menu_title = (
                "S T A R   D R I V E"
            )

            self.menu_button_title = "START"
            self.menu_modes_title = "MODES"

    # ========================================================
    # START / RESTART
    # ========================================================

    def on_menu_button(self):

        self.apply_selected_modes()

        self.reset_game()

        self.state_game_started = True

        self.hide_menu()

    # ========================================================
    # MODE PLACEHOLDER
    # ========================================================

    def on_modes_button(self):
        pass

    # ========================================================
    # REBUILD VERTICAL LINES
    # ========================================================

    def rebuild_vlines(self, new_number):

        if new_number == self.vlines_number:
            return

        self.vlines_number = new_number

        self.build_vlines()

    # ========================================================
    # APPLY MODES
    # ========================================================

    def apply_selected_modes(self):

        desired_speed = self.MODE_SPEEDS.get(
            self.mode_speed,
            8
        )

        desired_vlines = self.MODE_VLINES.get(
            self.mode_width,
            8
        )

        width_changed = (
            desired_vlines != self.vlines_number
        )

        if width_changed:

            self.rebuild_vlines(
                desired_vlines
            )

            if not self.state_game_started:

                self.tiles_coordinates.clear()
                self.last_y = 0

                self.generate_tiles_coordinates()

        self.base_speed = desired_speed

        if not self.state_game_started:
            self.speed = self.base_speed

    # ========================================================
    # UPDATE MODE SETTINGS
    # ========================================================

    def update_mode_settings(
        self,
        *,
        speed=None,
        width=None
    ):

        if speed in self.MODE_SPEEDS:
            self.mode_speed = speed

        if width in self.MODE_VLINES:
            self.mode_width = width

        self.apply_selected_modes()

    # ========================================================
    # CUSTOM TRACK WIDTH
    # ========================================================

    def change_track_width(self, new_vlines_number):

        try:
            new_v = int(new_vlines_number)

        except (TypeError, ValueError):
            return

        if (
            new_v < 4
            or new_v > 30
            or new_v % 2 != 0
        ):
            return

        if new_v == self.vlines_number:
            return

        if self.state_game_started:

            self.MODE_VLINES['custom'] = new_v
            self.mode_width = 'custom'

            return

        self.rebuild_vlines(new_v)

        self.tiles_coordinates.clear()
        self.last_y = 0

        self.generate_tiles_coordinates()


# ============================================================
# APP
# ============================================================

class NebulaApp(App):

    def build(self):
        return MainWidget()


if __name__ == '__main__':
    NebulaApp().run()