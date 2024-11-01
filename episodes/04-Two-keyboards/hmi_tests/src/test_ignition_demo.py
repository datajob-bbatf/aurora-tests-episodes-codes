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

import subprocess
import time
from typing import Optional
from aurora_tests.point import Point
from aurora_tests.rectangle import Rectangle
from aurora_tests.pytest.fixtures import display, mouse, keyboard, resources
from screen_keyboard import ScreenKeyboard


# Function that handles the logic for interacting with the login screen
def login_logic(display, mouse, keyboard, resources):
    # Capture the current screen display
    login_screen = display.grab()

    # Find the "Username" field on the login screen
    username_rect = login_screen.find_text("Username")
    assert username_rect, "Username input text box not found"
    # Click below the username text to place the cursor in the input box
    mouse.click(username_rect.p2 + Point(0, 30))

    # Wait for the screen to update after the click
    time.sleep(resources["SCREEN_TRANSITION_DELAY_S"])

    # Type the username using the provided keyboard
    keyboard.type(resources["LOGIN_USER"])

    # Find the "Password" field on the login screen
    password_rect = login_screen.find_text("Password")
    assert password_rect, "Password input text box not found"
    # Click below the password text to place the cursor in the input box
    mouse.click(password_rect.p2 + Point(0, 30))

    # Wait for the screen to update
    time.sleep(resources["SCREEN_TRANSITION_DELAY_S"])

    # Type the password using the provided keyboard
    keyboard.type(resources["LOGIN_PASSWORD"])

    # Find the login button image
    login_screen = display.grab()
    login_rect = login_screen.find_image(resources["LOGIN_BTN_ICON"])
    assert login_rect, "Login button not found"
    # Click the center of the login button to submit the login form
    mouse.click(login_rect.center())

    # Wait for the login process to complete
    time.sleep(resources["LOGIN_DELAY_S"])


# Function that handles the logic for the Hello World feature
def hello_world(display, mouse, resources):
    # Capture the current screen display
    main_screen = display.grab()

    # Find and click the "Empty" tab
    empty_tab = main_screen.find_text("Empty")
    assert empty_tab, "Empty tab not found"
    mouse.click(empty_tab.center())

    # Wait for the screen transition to complete
    time.sleep(resources["SCREEN_TRANSITION_DELAY_S"])
    main_screen = display.grab()  # Refresh the screen capture

    # Find and click the "Say Hello" button
    hello_btn = main_screen.find_text("Say Hello")
    assert hello_btn, "Hello button not found"
    mouse.click(hello_btn.center())

    # Wait for the screen transition to complete
    time.sleep(resources["SCREEN_TRANSITION_DELAY_S"])
    main_screen = display.grab()  # Refresh the screen capture

    # Verify that the "Hello World" text appears on the screen
    hello_hmi = main_screen.find_text("Hello World")
    assert hello_hmi, "Hello World text not found"


# Function that handles the application exit logic
def exit_logic(display, mouse, resources):
    # Capture the current screen display
    main_screen = display.grab()

    # Navigate to the Command menu to exit the application
    command_menu = main_screen.find_text("Command")
    assert command_menu, "Command menu not found"
    mouse.click(command_menu.center())

    # Wait for the screen transition to complete
    time.sleep(resources["SCREEN_TRANSITION_DELAY_S"])
    main_screen = display.grab()  # Refresh the screen capture

    # Find and click the "Exit" command to close the application
    try:
        command_menu_rectangle = Rectangle(resources["COMMAND_MENU_RECTANGLE"])
    except:
        command_menu_rectangle = None

    exit_command = main_screen.find_text("Exit", command_menu_rectangle)
    assert exit_command, "Exit command not found"
    mouse.click(exit_command.center())

    # Wait for the application to fully exit
    time.sleep(resources["APP_EXIT_DELAY_S"])


# Start the Ignition HMI application
def start_hmi_app(resources):
    app_start_args = resources["APP_START_ARGS"]
    subprocess.run(app_start_args)
    # Wait for the application to fully start
    time.sleep(resources["APP_START_DELAY_S"])


# Test scenario using a physical keyboard for login and main screen actions
def test_hello_world_physical_keyboard(display, mouse, keyboard, resources):
    # Start the Ignition HMI application
    start_hmi_app(resources)

    # Use the provided physical keyboard for this test
    used_keyboard = keyboard

    login_logic(display, mouse, used_keyboard, resources)
    hello_world(display, mouse, resources)
    exit_logic(display, mouse, resources)


# Test scenario using a screen keyboard for login and main screen actions
def test_hello_world_screen_keyboard(display, mouse, resources):
    # Start the Ignition HMI application
    start_hmi_app(resources)

    # Use a ScreenKeyboard instance for this test
    used_keyboard = ScreenKeyboard(display, mouse, resources)

    login_logic(display, mouse, used_keyboard, resources)
    hello_world(display, mouse, resources)
    exit_logic(display, mouse, resources)
