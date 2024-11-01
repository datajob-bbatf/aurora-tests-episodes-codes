# Copyright (C) 2024 DataJob Sweden AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import time
from typing import Optional
from aurora_tests.interfaces.idisplay import IDisplay
from aurora_tests.interfaces.ikeyboard import IKeyboard
from aurora_tests.interfaces.imouse import IMouse
from aurora_tests.rectangle import Rectangle


class ScreenKeyboard(IKeyboard):
    """
    A class to simulate typing on an on-screen keyboard in an HMI application.

    This class implements the `IKeyboard` interface and uses the `IDisplay`, `IMouse`,
    and resources for interacting with the screen-based keyboard.
    """

    def __init__(self, display: IDisplay, mouse: IMouse, resources: json) -> None:
        """
        Initializes the ScreenKeyboard by locating and clicking the on-screen keyboard icon.

        Args:
            display (IDisplay): The display object to capture the screen.
            mouse (IMouse): The mouse object to simulate mouse clicks.
            resources (json): The configuration and resource data for the application, including icons.

        Raises:
            RuntimeError: If the screen keyboard icon is not found.
        """
        self._display = display
        self._mouse = mouse
        self._resources = resources
        self._TRANSITION_DELAY = resources["SCREEN_KB_TRANSITION_DELAY_S"]

        # Capture the screen and find the screen keyboard icon
        login_screen = display.grab()
        screen_kb_icon = login_screen.find_image(
            resources["SCREEN_KB_OFF_ICON"])
        if not screen_kb_icon:
            raise RuntimeError("Screen Keyboard icon not found")
        mouse.click(screen_kb_icon.center())
        time.sleep(resources["SCREEN_TRANSITION_DELAY_S"])

    def type(self, text: str, char_delay_s: float = IKeyboard._CHAR_TYPE_DELAY_S) -> None:
        """
        Types a string of text using the on-screen keyboard.

        Args:
            text (str): The text to type.
            char_delay_s (float, optional): The delay between typing each character. Defaults to IKeyboard._CHAR_TYPE_DELAY_S.
        """
        self._screenshot = self._display.grab()

        for char in text:
            if char in "#123456789":
                mode_switcher_rec = self._is_letters_mode()
                if mode_switcher_rec:
                    self._switch_mode(mode_switcher_rec)
                    self._screenshot = self._display.grab()

                if char in "123456789":
                    char_icon = self._resources["SCREEN_KB"][f"NUM_{char}"]
                elif char == "#":
                    char_icon = self._resources["SCREEN_KB"]["HASH"]

                self._type_char(char_icon, char_delay_s)
            else:
                mode_switcher_rec = self._is_numbers_mode()
                if mode_switcher_rec:
                    self._switch_mode(mode_switcher_rec)
                    self._screenshot = self._display.grab()

                if char.isupper():
                    char_icon = self._resources["SCREEN_KB"][f"BIG_{char.capitalize()}"]
                    self._switch_to_shift()
                    self._screenshot = self._display.grab()
                    self._type_char(char_icon, char_delay_s)
                    self._screenshot = self._display.grab()
                else:
                    char_icon = self._resources["SCREEN_KB"][f"SML_{char.capitalize()}"]
                    self._type_char(char_icon, char_delay_s)

        self._type_enter()

    def _is_numbers_mode(self) -> Optional[Rectangle]:
        """
        Checks if the on-screen keyboard is in numbers mode.

        Returns:
            Optional[Rectangle]: The rectangle bounding the mode switcher icon if found, else None.
        """
        icon = self._resources["SCREEN_KB"]["ABC"]
        mode_switcher_rec = self._screenshot.find_image(icon)
        return mode_switcher_rec

    def _is_letters_mode(self) -> Optional[Rectangle]:
        """
        Checks if the on-screen keyboard is in letters mode.

        Returns:
            Optional[Rectangle]: The rectangle bounding the mode switcher icon if found, else None.
        """
        icon = self._resources["SCREEN_KB"]["123"]
        mode_switcher_rec = self._screenshot.find_image(icon)
        return mode_switcher_rec

    def _switch_mode(self, mode_switcher_rec: Rectangle) -> None:
        """
        Switches the mode on the on-screen keyboard between letters and numbers.

        Args:
            mode_switcher_rec (Rectangle): The rectangle bounding the mode switcher icon.
        """
        self._mouse.click(mode_switcher_rec.center())
        time.sleep(self._TRANSITION_DELAY)

    def _switch_to_shift(self) -> None:
        """
        Switches the on-screen keyboard to shift mode for typing uppercase characters.

        Raises:
            RuntimeError: If the shift icon is not found.
        """
        icon = self._resources["SCREEN_KB"]["SHIFT_LEFT"]
        rec = self._screenshot.find_image(icon)
        if not rec:
            raise RuntimeError("Left Shift icon not found")
        self._mouse.click(rec.center())
        time.sleep(self._TRANSITION_DELAY)

    def _type_char(self, icon: str, char_delay_s: float) -> None:
        """
        Types a single character by finding and clicking the character's icon.

        Args:
            icon (str): The resource key for the character icon to be typed.
            char_delay_s (float): The delay after typing the character.

        Raises:
            RuntimeError: If the character icon is not found.
        """
        rec = self._screenshot.find_image(icon)
        if not rec:
            raise RuntimeError(f"{icon} icon not found")
        self._mouse.click(rec.center())
        time.sleep(max(char_delay_s, self._TRANSITION_DELAY))

    def _type_enter(self) -> None:
        """
        Presses the enter key on the on-screen keyboard.

        Raises:
            RuntimeError: If the enter icon is not found.
        """
        icon = self._resources["SCREEN_KB"]["ENTER"]
        rec = self._screenshot.find_image(icon)
        if not rec:
            raise RuntimeError("Enter icon not found")
        self._mouse.click(rec.center())
        time.sleep(self._TRANSITION_DELAY)
