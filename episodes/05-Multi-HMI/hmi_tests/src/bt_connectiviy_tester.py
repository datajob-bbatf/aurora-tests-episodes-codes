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
from typing import Dict, Optional
from aurora_tests.interfaces.idisplay import IDisplay
from aurora_tests.interfaces.itouches import ITouches
from aurora_tests.interfaces.ibutton import IButton
from aurora_tests.rectangle import Rectangle


class BtConnectivityTester:
    """Helper class for testing Bluetooth connectivity between HMI devices."""

    _SCROLLING_TRIES: int = 4
    _POPUP_CHECK_TRIES: int = 10
    _POPUP_CHECK_SLEEP_S: float = 0.2

    def __init__(self, display: IDisplay, touches: ITouches, buttons: Dict[str, IButton], resources: Dict):
        """
        Initializes the Bluetooth connectivity tester.

        Args:
            display (IDisplay): The display interface instance.
            touches (ITouches): The touch interface instance.
            buttons (Dict[str, IButton]): A dictionary of button instances.
            resources (Dict): A dictionary of configuration and resource values.
        """
        self._display = display
        self._touches = touches
        self._buttons = buttons
        self._resources = resources

        # Load frequently used resources
        self._SCREEN_TRANSITION_DELAY_S = self._resources["SCREEN_TRANSITION_DELAY_S"]
        self._BOTTOM_SWIPE = tuple(self._resources["BOTTOM_SWIPE"])

    def unlock(self, pin: str) -> None:
        """
        Unlocks the device using a PIN.

        Args:
            pin (str): The unlock PIN code as a string.

        Returns:
            bool: True if successfully unlocked, False otherwise.
        """
        self._buttons["POWER"].press()
        time.sleep(self._SCREEN_TRANSITION_DELAY_S)

        self._touches.swipe(self._BOTTOM_SWIPE)
        time.sleep(self._SCREEN_TRANSITION_DELAY_S)

        for digit in pin:
            self._buttons[digit].press()
            time.sleep(self._SCREEN_TRANSITION_DELAY_S)

        self._buttons["ENTER"].press()
        time.sleep(self._resources["UNLOCK_DELAY_S"])

        screenshot = self._display.grab()
        if screenshot:
            find_region = Rectangle(self._resources["FOOTER_BAR_RECTANGLE"])
            recent_apps_icon_img = self._resources["RECENT_APPS_ICON"]
            recent_apps_icon = screenshot.find_image(
                recent_apps_icon_img, find_region)
            if recent_apps_icon:
                return True

        return False

    def open_app(self, app_name: str) -> bool:
        """
        Opens an application by its name.

        Args:
            app_name (str): The name of the application to open.

        Returns:
            bool: True if the application was successfully opened, False otherwise.
        """
        self._buttons["HOME"].press()
        time.sleep(self._SCREEN_TRANSITION_DELAY_S)

        for _ in range(self._SCROLLING_TRIES):
            app_icon = self._display.grab().find_text(app_name)
            if app_icon:
                self._touches.tap(app_icon.center())
                time.sleep(self._SCREEN_TRANSITION_DELAY_S)
                return True
            self._touches.swipe(self._BOTTOM_SWIPE)
            time.sleep(self._SCREEN_TRANSITION_DELAY_S)

        return False

    def open_settings_menu(self, menu: str) -> bool:
        """
        Opens a settings menu by its name.

        Args:
            menu (str): The name of the settings menu to open.

        Returns:
            bool: True if the menu was successfully opened, False otherwise.
        """
        for _ in range(self._SCROLLING_TRIES):
            menu_icon = self._display.grab().find_text(menu)
            if menu_icon:
                self._touches.tap(menu_icon.center())
                time.sleep(self._SCREEN_TRANSITION_DELAY_S)
                return True
            self._touches.swipe(self._BOTTOM_SWIPE)
            time.sleep(self._SCREEN_TRANSITION_DELAY_S)

        return False

    def request_to_pair(self, device: str) -> bool:
        """
        Initiates pairing with a device.

        Args:
            device (str): The name of the device to pair with.

        Returns:
            bool: True if pairing was initiated successfully, False otherwise.
        """
        pair_new_device_menu = self._display.grab().find_text("Pair new device")
        if pair_new_device_menu:
            self._touches.tap(pair_new_device_menu.center())
            time.sleep(self._SCREEN_TRANSITION_DELAY_S)

            for _ in range(self._POPUP_CHECK_TRIES):
                device_icon = self._display.grab().find_text(device)
                if device_icon:
                    self._touches.tap(device_icon.center())
                    return True
                time.sleep(self._POPUP_CHECK_SLEEP_S)

        return False

    def accept_to_pair(self) -> bool:
        """
        Accepts a pairing request.

        Returns:
            bool: True if the pairing request was accepted, False otherwise.
        """
        for _ in range(self._POPUP_CHECK_TRIES):
            if "PAIR_POPUP_RECTANGLE" in self._resources:
                popup_region = Rectangle(
                    self._resources["PAIR_POPUP_RECTANGLE"])
            else:
                popup_region = None

            popup_pair_btn = self._display.grab().find_text("PAIR", popup_region)
            if popup_pair_btn:
                self._touches.tap(popup_pair_btn.center())
                return True
            time.sleep(self._POPUP_CHECK_SLEEP_S)

        return False

    def is_paired_to_device(self, device: str) -> bool:
        """
        Checks if the device is paired.

        Args:
            device (str): The name of the device to check.

        Returns:
            bool: True if the device is paired, False otherwise.
        """
        for _ in range(self._POPUP_CHECK_TRIES):
            device_icon = self._display.grab().find_text(device)
            if device_icon:
                return True
            time.sleep(self._POPUP_CHECK_SLEEP_S)

        return False

    def forget_device(self) -> bool:
        """
        Forgets a paired device.

        Returns:
            bool: True if the device was successfully forgotten, False otherwise.
        """
        device_details_icon = self._display.grab().find_image(
            self._resources["DEVICE_DETAILS_ICON"])
        if device_details_icon:
            self._touches.tap(device_details_icon.center())
            time.sleep(self._SCREEN_TRANSITION_DELAY_S)

            forget_btn_text = self._display.grab().find_text("FORGET")
            if forget_btn_text:
                self._touches.tap(forget_btn_text.center())
                time.sleep(self._SCREEN_TRANSITION_DELAY_S)

                if "FORGET_POPUP_RECTANGLE" in self._resources:
                    popup_region = Rectangle(
                        self._resources["FORGET_POPUP_RECTANGLE"])
                else:
                    popup_region = None

                popup_forget_device_btn_text = self._display.grab(
                ).find_text("FORGET DEVICE", popup_region)
                if popup_forget_device_btn_text:
                    self._touches.tap(popup_forget_device_btn_text.center())
                    return True

        return False
