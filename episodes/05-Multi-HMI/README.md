## Overview
This episode showcases the powerful multi-device testing capabilities of the AuroraTests HMI Framework.

It demonstrates how to test and verify the Bluetooth connectivity feature between two Android-based HMI devices: Head Unit and Phone, in a single automated test - [test_pair_new_device.py](hmi_tests/src/test_pair_new_device.py)..

Additionally, it includes tests for forgetting connected devices on both the Head Unit and the Phone - [test_forget_device.py](hmi_tests/src/test_forget_device.py).

The project utilizes a single helper class, [BtConnectivityTester](hmi_tests/src/bt_connectiviy_tester.py), to optimize interactions with the Android-based HMIs. This unified approach works seamlessly for both devices, as they share similar menu structures and functionality.