from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock


class Modes(RelativeLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        Clock.schedule_once(
            self.initialize_toggle_buttons,
            0
        )

    # ========================================================
    # INITIALIZE
    # ========================================================

    def initialize_toggle_buttons(self, dt):

        self.ids.toggle_button_1.bind(
            on_press=self.on_turtle_pressed
        )

        self.ids.toggle_button_2.bind(
            on_press=self.on_sonic_pressed
        )

        self.ids.tight_button.bind(
            on_press=self.on_tight_pressed
        )

        self.ids.wide_button.bind(
            on_press=self.on_wide_pressed
        )

        self.ids.return_button.bind(
            on_press=self.return_to_menu
        )

        self.update_speed_buttons()
        self.update_width_buttons()

    # ========================================================
    # TOUCH
    # ========================================================

    def on_touch_down(self, touch):

        if self.opacity == 0:
            return False

        return super().on_touch_down(touch)

    # ========================================================
    # SPEED
    # ========================================================

    def on_turtle_pressed(self, *_):

        parent = self.parent

        if not parent:
            return

        if parent.mode_speed == 'turtle':
            parent.update_mode_settings(
                speed='normal'
            )
        else:
            parent.update_mode_settings(
                speed='turtle'
            )

        self.update_speed_buttons()

    def on_sonic_pressed(self, *_):

        parent = self.parent

        if not parent:
            return

        if parent.mode_speed == 'sonic':
            parent.update_mode_settings(
                speed='normal'
            )
        else:
            parent.update_mode_settings(
                speed='sonic'
            )

        self.update_speed_buttons()

    def update_speed_buttons(self):

        parent = self.parent

        if not parent:
            return

        mode = parent.mode_speed

        turtle = self.ids.toggle_button_1
        sonic = self.ids.toggle_button_2

        turtle.selected = mode == 'turtle'
        sonic.selected = mode == 'sonic'

    # ========================================================
    # TRACK WIDTH
    # ========================================================

    def on_tight_pressed(self, *_):

        parent = self.parent

        if not parent:
            return

        if parent.mode_width == 'tight':

            parent.update_mode_settings(
                width='normal'
            )

        else:

            parent.update_mode_settings(
                width='tight'
            )

        self.update_width_buttons()

    def on_wide_pressed(self, *_):

        parent = self.parent

        if not parent:
            return

        if parent.mode_width == 'wide':

            parent.update_mode_settings(
                width='normal'
            )

        else:

            parent.update_mode_settings(
                width='wide'
            )

        self.update_width_buttons()

    def update_width_buttons(self):

        parent = self.parent

        if not parent:
            return

        mode = parent.mode_width

        tight = self.ids.tight_button
        wide = self.ids.wide_button

        tight.selected = mode == 'tight'
        wide.selected = mode == 'wide'

    # ========================================================
    # RETURN
    # ========================================================

    def return_to_menu(self, instance):

        if not self.parent:
            return

        self.parent.apply_selected_modes()

        self.opacity = 0

        self.parent.menu_widget.opacity = 1