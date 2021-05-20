# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 02:17:34 2021

@author: Faizan
"""

import pymysql


db = pymysql.connect(host='localhost',
 user='mp2',
 passwd='eecs116',
 db= 'flights')
cur = db.cursor()

#sql= "SELECT * FROM customer"
#cur.execute(sql)

def findCheapestFlight():
    departureAirport=input("Please enter the Departure Airport code")
    arrivalAirport=input("Please enter the arrival Airport code")
    date=input("Please enter the date of travel?")
    params=(departureAirport, arrivalAirport, date)
    sql= ("""SELECT flight_Number, min(amount) 
         FROM fare NATURAL JOIN leg_instance
         Where Departure_airport_code=%s 
         and Arrival_airport_code=%s and leg_date=%s """)  
    cur.execute(sql, params)   
    result=cur.fetchall()
    print("The cheapest Flight Number is {} with a fare of {}".format(result[0], result[1]))

 
#findCheapestFlight()
#findCheapestFlight('SCK', 'IWA', '2018-01-28')

def findFlightNumber():
    customerName=input("Please enter the passenger's name")
    sql=("""SELECT Flight_number, Seat_number
            FROM seat_reservation 
            Where Customer_name=%s;""")
    cur.execute(sql, customerName)
    for row in cur.fetchall():
        print("The flight number is: ", row[0], " and the seat number is: ", row[1])

#findFlightNumber('Alex')

def findNonStopFlights():
    airline=input("Please enter the airline name")
    sql=("""SELECT Flight_number
            from flight NATURAL JOIN flight_leg
            where Airline=%s
            group by Flight_number
            having max(leg_number)=1;""")
    cur.execute(sql, airline)
    print("Non Stop Flights are: ")
    for row in cur.fetchall():
        print(row + ", ")
#findNonStopFlights('Southwest')

def insertNewAirplane():
    airplane_type=input("Please enter the name of the new airplane")
    seats=input("Please enter the maximum number of seats on the new airplane")
    cur.execute('SELECT MAX(Airplane_id) From Airplane')
    maxID=cur.fetchall()[0][0]
    sql = ("""INSERT INTO Airplane(Airplane_id, Total_number_of_seats, Airplane_type)
              VALUES(%s, %s, %s)""") # %s is a place holder for inserting a variable here
    val = (int(maxID+1), int(seats), airplane_type) # customer name is stored in variable cust_name
    
    cur.execute(sql, val)
    db.commit() #use commit to save the changes you made to the database
    print("The new airplane has been added with ID: ", maxID+1)

#insertNewAirplane(550, 'A380-800')

def increaseLowCostFare():
    factor=input("Please enter the factor you wish to increase the low cost fare by?")
    sql=("""UPDATE fare
         SET amount=amount * %s
         WHERE amount < 200 """)
    flightsChanged=cur.execute(sql, float(1+factor))
    print("Number of Flights with changed fares are: ", flightsChanged)
    db.commit()
    
    
def cancelReservation():
    flightNumber=input("Please enter the flight Number")
    name=input("Please enter the name of the passanger")
    q=("""Select Seat_number from seat_reservation
       Where Flight_Number='DL1149'
       and Customer_name='Mark'; """)
    cur.execute(q, (flightNumber, name))
    seatNumber=cur.fetchall()[0]
    sql=("""DELETE from seat_reservation 
         Where Flight_Number=%s
         and Customer_name=%s """)
    if (cur.execute(sql, (flightNumber, name))==1):
        print("Seat {} is released".format(seatNumber))
    db.commit()

#cancelReservation('AA1522', 'Lisa')

def clientInterface():
    while (True):
            response=input("""Hi please select a number between (1-6) corresponding to the queries below to make a request. Press anyother key to quit:
                           1) Find the cheapest flight from given a departure and arrival airport.
                           2) Find the flight and seat information for a customer.
                           3) Find all non-stop flights for an airline.
                           4) Add a new airplane.
                           5) Increase Fares less than $200 (Low-cost) by a specified factor.
                           6) Cancel a reservation for a customer.""" + "\n")
            try:
                response=int(response)
                
                if response <1 or response>6:
                    print("Have an amazing Day. Bye")
                    break
                
                else:
                
                    if response == 1: findCheapestFlight()
                    elif response == 2: findFlightNumber()
                    elif response == 3: findNonStopFlights()
                    elif response == 4: insertNewAirplane()
                    elif response == 5: increaseLowCostFare()
                    elif response == 6: cancelReservation()
                    else: break
                
            except:
                print("Have an amazing Day. Bye")
                break;
        
clientInterface()
                    
                