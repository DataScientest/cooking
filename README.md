# Cooking API

Cooking API is an open source API to organize lunch orders for multiples peoples in a same place

Specifications

## Data
* order : id, restaurant, menu, day, hour
* participant : id, name, mail, order_id (reference), order_details

## Routes
CRUD (create, read, update, delete) 
* CRUD order
* CRUD particant

## Functionalities
* As an organisator i want to create a new order
* As a participant i want to order by adding my name, email and order_details
