from kivy.uix.relativelayout import RelativeLayout


def keyboard_closed(self):

    if self._keyboard:

        self._keyboard.unbind(
            on_key_down=self.on_keyboard_down
        )

        self._keyboard = None


def on_keyboard_down(
    self,
    keyboard,
    keycode,
    text,
    modifiers
):

    if (
        not self.state_game_over
        and self.state_game_started
    ):

        if keycode[1] == 'left':

            if (
                self.movement
                < (self.vlines_number - 2) / 2
            ):

                self.movement += 1

        elif keycode[1] == 'right':

            if (
                self.movement
                > (self.vlines_number - 2) / -2
            ):

                self.movement -= 1

    return True


def on_touch_down(
    self,
    touch
):

    if (
        not self.state_game_over
        and self.state_game_started
    ):

        self.h_movement(
            list(touch.pos)
        )

    return super(
        RelativeLayout,
        self
    ).on_touch_down(touch)


def h_movement(
    self,
    touch_pos
):

    if self.is_pc():
        return

    if touch_pos[0] < self.width / 2:

        if (
            self.movement
            > (self.vlines_number - 2) / -2
        ):

            self.movement -= 1

    elif touch_pos[0] > self.width / 2:

        if (
            self.movement
            < (self.vlines_number - 2) / 2
        ):

            self.movement += 1