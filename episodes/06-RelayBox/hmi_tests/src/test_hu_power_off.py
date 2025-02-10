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

# Estimated shutdown time for the Head Unit to power down
SHUTDOWN_TIME_S = 2


def test_power_off(device_display, relays):
    """
    Test Case: Verify the Head Unit powers off successfully.

    Preconditions:
        - Head Unit and its display are initially powered on.
        - Display output is available.

    Steps:
        1. Power off the Head Unit display and Head Unit.
        2. Wait for the shutdown process to complete.
        3. Verify that the display output is no longer available after power-off.
    """
    # Verify initial state: HU and its display are powered on
    assert relays.hu_display.is_on(), "HU Display should initially be on."
    assert relays.head_unit.is_power_on(), "Head Unit should initially be on."
    assert device_display[DEV_HU].grab(
    ) is not None, "HU Display should show content when HU is powered on."

    # Power off the HU display and Head Unit
    relays.hu_display.off()
    relays.head_unit.power_off()

    # Wait for the Head Unit to shut down
    time.sleep(SHUTDOWN_TIME_S)

    # Verify final state: HU display should show no content
    assert device_display[DEV_HU].grab(
    ) is None, "HU Display should not show content after shutdown."
