from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock


class Modes(RelativeLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.initialize_toggle_buttons, 0)

    def initialize_toggle_buttons(self, dt):
        if 'toggle_button_1' in self.ids:
            self.ids.toggle_button_1.bind(on_press=self.on_turtle_pressed)
        if 'toggle_button_2' in self.ids:
            self.ids.toggle_button_2.bind(on_press=self.on_sonic_pressed)
        if 'tight_button' in self.ids:
            self.ids.tight_button.bind(on_press=self.on_tight_pressed)
        if 'wide_button' in self.ids:
            self.ids.wide_button.bind(on_press=self.on_wide_pressed)
        if 'return_button' in self.ids:
            self.ids.return_button.bind(on_press=self.return_to_menu)

        self.update_speed_buttons()
        self.update_width_buttons()

    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super().on_touch_down(touch)

    def on_turtle_pressed(self, *_):
        parent = self.parent
        if not parent:
            return
        parent.update_mode_settings(
            speed='normal' if parent.mode_speed == 'turtle' else 'turtle'
        )
        self.update_speed_buttons()

    def on_sonic_pressed(self, *_):
        parent = self.parent
        if not parent:
            return
        parent.update_mode_settings(
            speed='normal' if parent.mode_speed == 'sonic' else 'sonic'
        )
        self.update_speed_buttons()

    def update_speed_buttons(self):
        parent = self.parent
        if not parent:
            return

        if 'toggle_button_1' in self.ids:
            self.ids.toggle_button_1.state = 'down' if parent.mode_speed == 'turtle' else 'normal'

        if 'toggle_button_2' in self.ids:
            self.ids.toggle_button_2.state = 'down' if parent.mode_speed == 'sonic' else 'normal'

    def on_tight_pressed(self, *_):
        parent = self.parent
        if not parent:
            return
        parent.update_mode_settings(
            width='normal' if parent.mode_width == 'tight' else 'tight'
        )
        self.update_width_buttons()

    def on_wide_pressed(self, *_):
        parent = self.parent
        if not parent:
            return
        parent.update_mode_settings(
            width='normal' if parent.mode_width == 'wide' else 'wide'
        )
        self.update_width_buttons()

    def update_width_buttons(self):
        parent = self.parent
        if not parent:
            return

        if 'tight_button' in self.ids:
            self.ids.tight_button.state = 'down' if parent.mode_width == 'tight' else 'normal'

        if 'wide_button' in self.ids:
            self.ids.wide_button.state = 'down' if parent.mode_width == 'wide' else 'normal'

    def return_to_menu(self, instance):
        if not self.parent:
            return

        self.parent.apply_selected_modes()
        self.opacity = 0
        self.parent.menu_widget.opacity = 1
