# Term-Project

Readme File for Balloons Tower Defense 1

Project Description:

This project is a spinoff of the popular online game, Bloons Tower Defense developed by Ninja Kiwi. 
Balloons will traverse a randomly generated map, from a start point to an end point. The player's goal is to 
pop as many balloons as possible before their health reaches 0. To do this, they can use certain key presses
in order to place down different types of towers. The archer tower and fast tower, shoot by predicting the movement
of balloons, the wizard, flame, and ice towers shoot the closest balloon in their range. If the player's health reaches 
0, the game is over. Player's can choose between "Normal" and "Nightmare" mode, which changes the starting gold, health,
and number of balloons spawned. 

Balloons:

Red: 1 Health, Blue 2 Health, Green: 3 Health, Yellow 4 Health, Metal 20 Health (can only be damaged if frozen, or by fire)


Towers:

Archer Tower: key: "A", price = 100 gold, has a brief cooldown after using all ammo
Fast Tower: key: "F", price = 150 gold, shoots faster, and has no cooldown
Freeze Tower: key = "I", price = 400 gold, Freezes first balloon in its range 
Wizard Tower: key = "M", price = 500 gold, uses lighting to instanly kill a balloon, and leaves a mark. If the mark is clicked player gains 50 gold. 
Fire: key = "H", price = 700 gold, burns balloons that pass through it, melts a metal balloon into a yellow balloon. 

How to Run:

All files are imported into term project 112.py. To Run: Run term project 112.py. 

Libraries:
No external libraries used, other than cmu 15112 graphics 

SHORTCUTS:
key: "L", decreases player lives to 0 
key: "Z", gives player 10000 gold 
