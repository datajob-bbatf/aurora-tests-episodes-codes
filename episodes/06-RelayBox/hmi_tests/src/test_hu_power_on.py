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

import time
from aurora_tests.pytest.fixtures import device_display, relays

# Device identifier for the Head Unit (HU)
DEV_HU = "HeadUnit"

# Estimated boot-up time for the Head Unit to fully initialize
BOOTUP_TIME_S = 30


def test_power_on(device_display, relays):
    """
    Test Case: Verify the Head Unit powers on successfully.

    Preconditions:
        - Head Unit and its display are initially powered off.
        - No display output is captured.

    Steps:
        1. Power on the Head Unit display and Head Unit.
        2. Wait for the boot-up process to complete.
        3. Verify that the display output becomes available after power-on.
    """
    # Verify initial state: HU and its display are powered off
    assert relays.hu_display.is_off(), "HU Display should initially be off."
    assert relays.head_unit.is_power_off(), "Head Unit should initially be off."
    assert device_display[DEV_HU].grab() is None, "No display content should be available when HU is off."

    # Power on the HU display and Head Unit
    relays.hu_display.on()
    relays.head_unit.power_on()

    # Wait for the Head Unit to boot up
    time.sleep(BOOTUP_TIME_S)

    # Verify final state: HU display should show content
    assert device_display[DEV_HU].grab() is not None, "HU Display should show content after boot-up."

