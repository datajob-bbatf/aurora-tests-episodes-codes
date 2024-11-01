## Overview

This episode uses an HMI application as the System Under Test (SUT) based on the [Ignition HMI framework](https://inductiveautomation.com/solutions/hmi) from Inductive Automation.

## Setup Ignition Environment

1. **Install the Ignition Gateway**  
   Download and set up the `Ignition Gateway` via the [Ignition Installer](https://inductiveautomation.com/downloads/).

2. **Run the Gateway and Import the Ignition Demo Project**  
   After the gateway is set up, import the provided [Ignition Demo Project](ignition_demo_project).

3. **Install the Vision Client Launcher**  
   From the installed Ignition Gateway, set up the Vision `Client Launcher`.

4. **Run the Client Launcher**  
   Add the application from the imported project to the `Client Launcher`.

## Setup AuroraTests

1. Navigate to the `hmi_tests` folder.
2. Place the provided `conftest.py` file in the `hmi_tests` folder (this file is included with the AuroraTests package).
3. (Optional) **Set up a Python Virtual Environment**  
   If you are using Ubuntu or another Linux-based OS, you can create a virtual environment with the following commands:
   ```bash
   python3 -m venv my_project_venv
   source my_project_venv/bin/activate
   ```
   On Windows:
   ```
   python -m venv my_project_venv
   my_project_venv\Scripts\activate
   ```
4. **Install the AuroraTests Package**  
   Install the AuroraTests package using the provided `.whl` file:
   ```bash
   pip install aurora_tests-2.0.24.whl
   ```

## Prepare the Test Environment

1. **Check Display Resolution**  
   Ensure that your display resolution matches one of the existing resolutions in the resource folders. For instance, for a display resolution of `1920x1080`, the folder `hmi_tests/res_1920_1080` should be used.

2. **Adapt Ignition Configuration**  
   Modify the Ignition-related configuration in the appropriate [resource file](hmi_tests/res_1920_1080/res.json):
   * `APP` - application startup parameters;
   * `LOGIN_USER` - user for login;
   * `LOGIN_PASSWORD` password for login.

## Run HMI Tests

1. **Command Line Execution**  
   From the command line in the `hmi_tests` folder, run:
   ```bash
   pytest --config_file config.json --res_file res_1920_1080/res.json
   ```
