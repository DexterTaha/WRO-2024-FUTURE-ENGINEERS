MINDCRAFT WRO Future Engineers team
====

<p align="center">
  <img src="https://github.com/DexterTaha/WRO-2024-FUTURE-ENGINEERS/assets/130682580/d9385136-f971-4c95-ba80-ffc14f7c0a4e" alt="banner" width="1500">
</p>


This repository provides information and knowledge regarding the ongoing progress, evolution, and development of our self-driving robot vehicle, which was created and coded by us, [Salmane Derdeb](https://github.com/salmane-derdeb) and [Taha TAIDI LAAMIRI](https://github.com/DexterTaha), as participants in the Future Engineers 2024 division of the World Robot Olympiad (WRO).

## World Robot Olympiad (WRO)
<p align="center">
  <img src="https://github.com/DexterTaha/WRO-2024-FUTURE-ENGINEERS/assets/130682580/6d08f11e-2e99-4d6c-8994-0dc8783c6f05" width="1500">
</p>

The World Robot Olympiad (WRO) is a prestigious international robotics competition that ignites the imaginations of students worldwide. It challenges participants to showcase their creativity, problem-solving skills, and technical prowess in designing and programming robots for a variety of tasks and challenges.

One of the most dynamic categories within WRO is the Future Engineers category. Here, participants are tasked with developing innovative solutions to real-world problems using robotics and automation. This category serves as a breeding ground for future innovators, encouraging students to think critically and creatively, laying the groundwork for a new generation of engineers and technologists.

This year, the Future Engineers category presents an exciting challenge: creating a self-driving car. This challenge pushes participants to explore the cutting edge of robotics, adding layers of complexity and innovation to an already thrilling competition.

[Watch the challenge explanation video](https://www.youtube.com/watch?v=_J15lf6uhwo&t=2s)


## Content

- `t-photos`: Contains 2 photos of the team, including an official one and a funny photo with all team members.
- `v-photos`: Contains 6 photos of the vehicle, showcasing it from every side as well as from the top and bottom.
- `video`: Contains a `video.md` file with a link to a video demonstrating the vehicle's driving capabilities.
- `schemes`: Contains one or several schematic diagrams (JPEG, PNG, or PDF) illustrating all electromechanical components used in the vehicle, including electronic components and motors, and how they connect to each other.
- `src`: Contains the control software code for all components programmed to participate in the competition.
- `models` (optional): Contains files for models used by 3D printers, laser cutting machines, and CNC machines to produce the vehicle elements. If not needed, this directory can be removed.
- `other` (optional): Contains additional files that can help understand how to prepare the vehicle for the competition, such as documentation on connecting to a SBC/SBM, uploading files, datasets, hardware specifications, and communication protocols descriptions. If not needed, this directory can be removed.

OUR ROBOT
====
## OUR ROBOT
<p align="center">
  <img src="https://github.com/DexterTaha/WRO-2024-FUTURE-ENGINEERS/assets/130682580/64664154-5967-491a-95b5-6b116392faf6" alt="W15" width="500">
</p>

OUR ROBOT 


Our robot, named W15, is a remarkable creation built using LEGO components. It incorporates five main parts, each crucial to its functionality. The steering mechanism allows for precise control, while the gearbox ensures smooth operation. Sensing elements provide environmental awareness, enabling the robot to react to its surroundings. The driving system propels the robot with agility and speed. The name W15 is inspired by the W15 Mercedes Formula One car of 2024, reflecting our robot's cutting-edge design and performance.
<p align="center">
  <img src="https://github.com/DexterTaha/WRO-2024-FUTURE-ENGINEERS/assets/130682580/3843db28-f352-4599-a5ec-a22cdc28278d" alt="W15 F1" width="300">
</p>
W15 MERCEDES F1 car

## ROBOT AIM and OBJECTIVES
Aim
The aim of the robot is to swiftly maneuver its environment or parkour.
This involves

**Objectives**

1. Detect obstacles in the environment.
2. Avoid obstacles in the environment.
3. Perform (1) and (2) while self driving.
4. Detect state and auto-correct when crashed or in error.
### Constraints
1. Time
2. Motor
3. Drive train
4. Cannot use too common ideas from the internet
5. Dimensions

## RESEARCH and BRAINSTORMING
Practical Functions of the Robot
Using a rear-wheel drive system the bot will be able to perform the follow (the following list is in order of priority)

### PRACTICAL FUNCTIONS OF ROBOT
● Moving in all directions
  
● Lane following
  
● Acceleration and deceleration
  
● Braking
  
● Color Detection
  
● Turning
  
● Crash handling
  
● Orientation detection
  
● Obstacle detection
  
● Obstacle avoidance
  
● Light adjustment
  
### ELABORATION OF PRACTICAL FUNCTIONS DETAILS
**COLOR DETECTION BY THE ROBOT:**  
With the OpenCV library, the robot will be programmed to detect color using the following.

**The HSV format**:

1. The video frame is read correctly.
2. Each frame is converted from BGR to HSV.
3. A mask is created using the inRange() method on the image with the image and the color to be detected as the arguments.
4. After doing the above, a threshold image is created by the mask. This blacks out every other item in the image leaving only the pixels that match the mask. This creates a black background with a white range of detection.
5. This shows that the color has been detected

## Energy Source for the Robot

The robot uses a 9V adapter that has an output of 2.5A or more.


## Intelligence (How does the robot think):

The bot uses deep learning models alongside computer vision, Kalman filtering and concepts of Advanced Driver Assistance Systems(ADAS) all made with C++ and python.
Using Computer vision and Kalman filtering to make itself aware of itself and  environment and how to react to changes in the environment.
Sketching
This is where the AutoCAD(Fusion360).
Building a Prototype


### Competition Strategy
Since the competition is a time attack race time of completion is very essential to everything. Therefore all ideas should be developed to the point where it makes the robot do things faster.
Current Strategy

Motion:
For the first lap the robot learns about [//the environment and positions of all the red and green bars on the mat. – Why is this the first thing to do?
Using that data, the robot adapts itself increasing to maximum speeds and turn rates at various points during the second and last laps of the round and possibly drifting

**To be able to do this:** 

1. The first step is to be able to move around the game mat as possible while no obstacles on the mat.
2. Then moving while detecting obstacles and avoiding obstacles.
3. Performing (2) flawlessly.
4. Gather information on the current mat
5. Moving with pre-recorded information
6. Speeding up.
7. Drifting (optional. We would really love to be able to drift) – Do you know the essence of drifiting?



## Bill of materials

| Quantity | Status                             | Description                                                                                                                                             |
| ---------| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1        | Raspberry Pi 4 Model B             | ![Raspberry-Pi4](https://github.com/DexterTaha/WRO-2024-FUTURE-ENGINEERS/assets/130682580/29ab19c0-aab2-42f6-a3a3-ed79587e58bc)                         |
| 1        | Logitech® HD Webcam C270           | ![Logitech® HD Webcam C270](https://github.com/DexterTaha/WRO-2024-FUTURE-ENGINEERS/assets/130682580/49862a6a-7090-4f75-b339-11148f137492)              |
| 1        | 5v power bank                      | ![5v power bank](https://github.com/DexterTaha/WRO-2024-FUTURE-ENGINEERS/assets/130682580/4259c9a3-a346-4806-9d60-ad36e5115942)                         |
| 2        | Logo® Robot inventor hub           | ![Logo® Robot inventor hub](https://github.com/DexterTaha/WRO-2024-FUTURE-ENGINEERS/assets/130682580/21c04300-7178-4238-b390-21bdbd0f5f05)              |
| 5        | Logo® Technic™ Medium Angular Motor| ![Logo® Technic™ Medium Angular Motor_2](https://github.com/DexterTaha/WRO-2024-FUTURE-ENGINEERS/assets/130682580/33029bab-2e1a-4e48-8a18-d5d74be013a8) |
| 2        | Logo® Technic™ Color Sensor        | ![Logo® Technic™ Color Sensor](https://github.com/DexterTaha/WRO-2024-FUTURE-ENGINEERS/assets/130682580/3e84f65e-d1ff-419e-8f44-291a97303c2c)           |
| 3        | Logo® Technic™ Ultrasonic Sensor   | ![Logo® Technic™ Ultrasonic Sensor](https://github.com/DexterTaha/WRO-2024-FUTURE-ENGINEERS/assets/130682580/e8e2d6ac-bb61-4a2b-bb90-486233006838)      |
| 280      | Logo® Technic™ spare pieces        | ![efw](https://github.com/DexterTaha/WRO-2024-FUTURE-ENGINEERS/assets/130682580/5115e60b-d975-47cc-acee-51f2e9d34bb0)                                   |

## Contribution
<p align="center">
  <a href="https://github.com/DexterTaha/WRO-2024-FUTURE-ENGINEERS/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=DexterTaha/WRO-2024-FUTURE-ENGINEERS" alt="Contributors" width="200"/>
  </a>
</p>
