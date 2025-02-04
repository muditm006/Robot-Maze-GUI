# Robot Control Interface Project

The purpose of this project is to develop a program that enables the client to control a robot through a **GUI interface** on a device. The program provides precise control over the robot's movements, including forward, backward, and turning motions, while allowing the user to regulate parameters such as speed, time, and turning angles.

## Features

- **GUI-Based Robot Control**  
  The interface allows users to control the robot's movements (forward, backward, left, right) with ease.

- **Customizable Parameters**  
  Users can adjust movement parameters like speed, duration, and turning angles directly through the GUI.

- **Robot Class Implementation**  
  A dedicated `Robot` class connects motor pins to the H-bridge for power and includes functions for each movement type.

- **Multi-Language Integration**  
  - **Python**: Used for robot control logic and PyCamera integration.  
  - **Java**: Java Swing provides an intuitive GUI interface.  
  - **HTML/Flask**: Flask server enables communication between the GUI and robot controls.

## File Descriptions

### Folders

- **Camera/**  
  Contains Python scripts for integrating PyCamera functionality to capture and process video feeds.

- **Flask/**  
  Includes Flask server files for handling communication between the GUI and robot control logic.

- **JDK/**  
  Houses Java dependencies required for running the Java Swing-based GUI.

- **Project 1 - Sprint/**  
  Contains additional resources and documentation related to project development.

### Files

- **GUI.java**  
  Implements the graphical user interface using Java Swing. Provides buttons and sliders for controlling robot movements and adjusting parameters like speed and time.

- **clientpkg.java**  
  Handles communication between the GUI and backend logic, facilitating smooth interaction between user inputs and robot commands.

- **scrum.py**  
  Python script containing the `Robot` class with functions to move forward, turn left/right, move backward, and regulate speed/time. Connects motor pins to the H-bridge for power.

- **README.md**  
  This file provides an overview of the project, its features, file descriptions, and usage instructions.

## How to Use

1. Clone this repository to your local machine:
git clone https://github.com/muditm006/RobotControlInterface.git
cd RobotControlInterface

2. Set up dependencies:
- Install Python libraries (e.g., Flask) using:
  ```
  pip install flask
  ```
- Ensure Java JDK is installed for running GUI components.
- Set up PyCamera on your Raspberry Pi or compatible device if using camera functionality.

3. Run the Flask server:
cd Flask
python app.py

4. Launch the Java-based GUI:

5. Use the GUI interface to:
- Control robot movements (forward, backward, left, right).  
- Adjust movement parameters like speed, time duration, and turning angles.  

6. Optional: Use PyCamera functionality in conjunction with robot controls for live video feed or image processing tasks.

## Notes

This project demonstrates a multi-language approach combining Python, Java, and HTML/Flask to create a robust robot control interface. It integrates hardware-level control with user-friendly software tools.
