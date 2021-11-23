# Cooking API

Cooking API is an open source API to organize lunch command for multiples peoples in a same place

Specifications

## Data
* command : id, restaurant, menu, day, hour
* participant : id, name, mail, command_id (reference), command_details

## Routes
CRUD (create, read, update, delete) 
* CRUD command
* CRUD particant

## Functionalities
* As an organisator i want to create a new command
* As a participant i want to order by adding name, email and command_details
