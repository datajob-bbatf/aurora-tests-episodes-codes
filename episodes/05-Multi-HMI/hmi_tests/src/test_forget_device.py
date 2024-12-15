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

from aurora_tests.pytest.fixtures import device_display, device_touches, device_buttons, device_resources
from bt_connectiviy_tester import BtConnectivityTester

# Device constants for easy reference
DEV_HU = "HeadUnit"  # Represents the Head Unit device
DEV_PH = "Phone"     # Represents the Phone device


def test_forget_device_hu(device_display, device_touches, device_buttons, device_resources):
    """
    Test case to forget a paired device from the Head Unit.

    Steps:
    1. Open the Settings app on the Head Unit.
    2. Navigate to the "Connected devices" menu.
    3. Forget the paired device.

    This test ensures the Head Unit can successfully forget a previously paired device.
    """

    # Instantiate a BtConnectivityTester for the Head Unit
    head_unit = BtConnectivityTester(
        display=device_display[DEV_HU],
        touches=device_touches[DEV_HU],
        buttons=device_buttons[DEV_HU],
        resources=device_resources[DEV_HU]
    )

    # Step 1: Open the Settings app on the Head Unit
    assert head_unit.open_app("Settings")

    # Step 2: Navigate to the "Connected devices" menu
    assert head_unit.open_settings_menu("Connected devices")

    # Step 3: Forget the paired device
    assert head_unit.forget_device()


def test_forget_device_phone(device_display, device_touches, device_buttons, device_resources):
    """
    Test case to forget a paired device from the Phone.

    Steps:
    1. Unlock the Phone using its PIN code.
    2. Open the Settings app on the Phone.
    3. Navigate to the "Connected devices" menu.
    4. Forget the paired device.

    This test ensures the Phone can successfully forget a previously paired device.
    """

    # Instantiate a BtConnectivityTester for the Phone
    phone = BtConnectivityTester(
        display=device_display[DEV_PH],
        touches=device_touches[DEV_PH],
        buttons=device_buttons[DEV_PH],
        resources=device_resources[DEV_PH]
    )

    # Step 1: Unlock the Phone using its PIN code
    assert phone.unlock("2211")

    # Step 2: Open the Settings app on the Phone
    assert phone.open_app("Settings")

    # Step 3: Navigate to the "Connected devices" menu
    assert phone.open_settings_menu("Connected devices")

    # Step 4: Forget the paired device
    assert phone.forget_device()
