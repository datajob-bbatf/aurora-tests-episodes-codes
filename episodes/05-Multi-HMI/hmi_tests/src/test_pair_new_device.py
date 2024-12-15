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


def test_pair_new_device(device_display, device_touches, device_buttons, device_resources):
    """
    Example usage of the BtConnectivityTester helper class to automate pairing 
    between a Head Unit and a Phone.

    This test demonstrates:
    1. Opening the Bluetooth settings on the Head Unit.
    2. Unlocking the Phone using a PIN.
    3. Opening the Bluetooth settings on the Phone.
    4. Initiating a pairing request from the Phone to the Head Unit.
    5. Accepting the pairing request on both devices.
    6. Verifying that both devices are paired with each other.
    """

    # Instantiate a BtConnectivityTester for the Head Unit
    head_unit = BtConnectivityTester(
        display=device_display[DEV_HU],
        touches=device_touches[DEV_HU],
        buttons=device_buttons[DEV_HU],
        resources=device_resources[DEV_HU]
    )

    # Instantiate a BtConnectivityTester for the Phone
    phone = BtConnectivityTester(
        display=device_display[DEV_PH],
        touches=device_touches[DEV_PH],
        buttons=device_buttons[DEV_PH],
        resources=device_resources[DEV_PH]
    )

    # Step 1: Open the Settings app and navigate to the "Connected devices" menu on the Head Unit
    assert head_unit.open_app("Settings")
    assert head_unit.open_settings_menu("Connected devices")

    # Step 2: Unlock the Phone using its PIN code
    assert phone.unlock("2211")

    # Step 3: Open the Settings app and navigate to the "Connected devices" menu on the Phone
    assert phone.open_app("Settings")
    assert phone.open_settings_menu("Connected devices")

    # Step 4: Initiate a pairing request from the Phone to the Head Unit
    assert phone.request_to_pair("Head Unit")

    # Step 5: Accept the pairing request on both devices
    assert head_unit.accept_to_pair()
    assert phone.accept_to_pair()

    # Step 6: Verify that both devices are paired with each other
    assert head_unit.is_paired_to_device("moto e13")
    assert phone.is_paired_to_device("Head Unit")
