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
from aurora_tests.pytest.fixtures import device_display, relays

# Device identifier for the Head Unit (HU)
DEV_HU = "HeadUnit"

# Estimated boot-up time for the Head Unit to fully initialize
BOOTUP_TIME_S = 30

# Estimated shutdown time for the Head Unit to power down
SHUTDOWN_TIME_S = 2

# Delay for relay switching operations
SWITCHING_DELAY_S = 1

# Estimated boot-up time for the HU in Programming Mode
PROG_MODE_BOOTUP_TIME_S = 5

# Path to the flashing script for updating the HU software
FLASH_SCRIPT = "/home/mykola/Projects/my/ncar/device/linaro/hikey/installer/hikey960/uefi-flash-all.sh"


def flash_head_unit():
    """Executes the flashing script to update the Head Unit software."""
    subprocess.run(FLASH_SCRIPT)


def test_sw_update(device_display, relays):
    """Test Scenario: Head Unit Software Update"""

    # Verify initial state: HU and its display should be powered off
    assert relays.hu_display.is_off(), "HU Display should initially be off."
    assert relays.head_unit.is_power_off(), "Head Unit should initially be off."
    assert relays.hu_prog_mode.is_disable(), "Head Unit should not be in Programming Mode."
    assert device_display[DEV_HU].grab() is None, "No display content should be available when HU is off."

    # Enable Programming Mode to prepare for flashing
    relays.hu_prog_mode.enable()
    time.sleep(SWITCHING_DELAY_S)  # Allow time for mode switching

    # Power on the Head Unit in Programming Mode
    relays.head_unit.power_on()
    time.sleep(PROG_MODE_BOOTUP_TIME_S)  # Wait for the HU to initialize in this mode

    # Start the flashing process
    flash_head_unit()

    # Power off the Head Unit after flashing is complete
    relays.head_unit.power_off()
    time.sleep(SHUTDOWN_TIME_S)  # Allow time for a complete shutdown

    # Disable Programming Mode to return to normal operation
    relays.hu_prog_mode.disable()
    time.sleep(SWITCHING_DELAY_S)  # Allow time for mode switching

    # Power on the HU display and Head Unit for verification
    relays.hu_display.on()
    relays.head_unit.power_on()
    time.sleep(BOOTUP_TIME_S)  # Wait for the Head Unit to boot up fully

    # Verify final state: HU display should now be active and showing content
    assert device_display[DEV_HU].grab() is not None, "HU Display should show content after boot-up."
