# Hermes
## Brief Introduction
This is the source code of the project I've taken in the 2018 NUS Summer Workshop in Cluster 3 Topic 1 Tele-Robotic Deep Learning. Hermes is the name of the robot designed by our team.

Why do I take this name? Well, this is the name of a acient Greek god. He is a god full of talents, just as I want in our robot. So I just take this name. Quite simple : )

## Folder Structure
In the main folder, I have four sub folders, containing those small tasks checked by professor and the main project on the final demo.

### arduino_basic
In this folder, I have all the basic usage of Arduino, which can give you a specific idea about how to drive the motor, how to turn the directions and how to communicate with Pi. In a word, all these codes will teach you how to build a robot on a base line.

### road_test
In this folder, I have placed the codes used on "Road Test", in which each team are asked to drive their robot from the front door to the back one in the lab. We sit in our seats, viewing the real-time pictures taken by Pi Camera and then give instructions to drive the robot.

### treasure_hunt
In this folder, I have placed the codes (ONLY the robot side) used on "Treasure Hunt". This task is a mid-term exam in a sense. We are going to put the robot in a maze, driving to search the cat pictures by hands. Then we use deep learning techniques to classify the cats we've found. Our scores are measured according to how fast we drive and the correctness of the classification.

### advanced_model
In this folder, I have just one part of the source code, which is the object detection part, and the other of which is the voice recognition part (kept by another guy in our team. What a pity, I do not have the copy T_T). On the server side, we run two processes, one of which runs the tensorflow, and the other of which is a communication terminal, receiving pictures from Pi, sending pictures to TensorFlow, receiving results from TensorFlow, generating instructions according to the results and sending specific instructions to Pi. Hermes can detect the nearest fire hydrant, and move to it autonomously. In the meantime, it can also report the real time crowd density.