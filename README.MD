
## Table of Contents
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Installation](#installation)
3. [Testing app](#installation)
3. [Proposition](#Proposition)
### General Info
***
this project is my attempt at the open technical test "Cooking app".
## Technologies
***
A list of technologies used within the project:
* Flask : Version 2.0.1
* Python : Version 3.8.6
* Docker 
## Installation and Running the project
***
clone the project and inside the project directory launch.
To create a docker image execute:
```
$ docker build . -t cooking
```
To run the docker image execute:
```
$ docker run -p 5000:5000 cooking 
```
and visit with your browser http://localhost:5000
To run unit tests inside the container execute:

```
$ docker run -it cooking /bin/sh
```
and then in the new command promt run
```
$ pip install pytest && pytest
```

## Testing the app 
***
* Visit with your browser http://localhost:5000
* Register and then Login
* The organizer ( Admin ) can access the "command dashboard" after clicking on Command Dashboard where he will see the list of the commands ( restaurant name, menu, date and hour ), he can edit,delete and add a command.
* The organizer can can access the "participant dashboard" after clicking on Participant Dashboard where he will see the list of the commands (name, mail ), he can edit,delete, and add a participant, he can choose which command the participant will participate from a select list.    
* The Participant can access a screen where he will find the list of the command he can participate in a command when he click on order. 
## Proposition
* A table representing  restaurants ( id, name,menu) will be better .
* The Menu for the moment is a Text but we can attach an image instead if it's possible.    
* The Tests that I wrote cover only the authentication functionality and The command CRUD.  
