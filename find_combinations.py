"""
Author: Samuel Pucek
Date: 14.6.2019

Brief INFO:
* 2 inputs: name of the input csv file, number of bags
* recursive algorithm for finding available trips
* solution is saved in list trips => list of the available trips => suitable for further processing
* we dealt with basic exceptions
"""

import csv
from datetime import datetime


class FindCombination:
    def __init__(self):
        # Initialize variable for saving data
        self.bags = 0
        self.data = []

        # transfer limit minimum 1 hour
        self.transfer_limit_min = 3600
        # tranfer limit maximum 4 hours
        self.transfer_limit_max = 3600 * 4

        # list of final trips
        self.trips = []

    def reader(self):
        """
        Funcion for reading data from csv file. Data are saved in variable data[].
        :return:
        """

        # Read input data
        try:
            # catch errors with input arguments

            # Read file name given via standard input
            file_name = input()
            # Read number of bags
            self.bags = int(input())

            # For testing...
            # file_name = "input.csv"
            # self.bags = 0

            file = open(file_name, encoding="utf-8")

        except FileNotFoundError as ex:
            print(ex)

        except ValueError as ex:
            print("Number of bags - wrong input parameter")
            print(ex)

        else:
            reader = csv.reader(file)

            header = next(reader)
            for row in reader:
                try:
                    # catch errors with wrong data format

                    # row = [From, To, Departure date/time, Arrival date/time, Flight no, Price, Bags allowed,
                    # Bag price]
                    dep_airport = row[0]
                    arr_airport = row[1]
                    # USM,HKT,2019-05-11T06:25:00,2019-05-11T07:25:00,PV404,24,1,9
                    dep_date_time = datetime.strptime(row[2], "%Y-%m-%dT%H:%M:%S")
                    arr_date_time = datetime.strptime(row[3], "%Y-%m-%dT%H:%M:%S")
                    flight_no = row[4]
                    flight_price = int(row[5])
                    bag_allowed = int(row[6])
                    bag_price = int(row[7])

                except ValueError as ex:
                    print("Wrong input file format - row skipped")
                    print(row)
                    print(ex)
                    print()

                except IndexError as ex:
                    print("Wrong input file format - row skipped")
                    print(row)
                    print(ex)
                    print()

                else:
                    self.data.append(
                        [dep_airport, arr_airport, dep_date_time, arr_date_time, flight_no, flight_price, bag_allowed,
                         bag_price])

            # Close file
            file.close()

    def flight_combo_maker(self, flights, transfer_city, flights_short):
        """
        Recursive function. Searching new trips. Save them in the list trips.
        :param flights: list of flights (part of the trip)
        :param transfer_city: remember last city => find connecting flight in a short time
        :param flights_short: list of flights - short form of parameter flight, remember only the city codes
        :return: the result is in a list called trips
        """
        for row in self.data:
            # first check, if the bags are allowed
            if row[6] >= self.bags:

                # this is the first flight of the trip
                if not flights:
                    # we just found a trip => add it to list trips
                    self.trips.append([row])

                    # call flight_combo_maker
                    self.flight_combo_maker(flights + [row], row[1], flights_short + [row[0] + row[1]])

                # this is not the first flight of the trip
                else:
                    # if we find a via airport
                    if row[0] == transfer_city:
                        # copy last flight
                        last_flight = flights[len(flights) - 1]

                        # last flight arrival date/time
                        last_flight_date_time = last_flight[3]
                        connecting_flight_date_time = row[2]
                        transfer_time = connecting_flight_date_time.timestamp() - last_flight_date_time.timestamp()

                        # if the transfer is between 1 and 4 hours
                        if (transfer_time >= self.transfer_limit_min) & (transfer_time <= self.transfer_limit_max):

                            # do not include the same flights, e.g. A -> B -> A -> B
                            if (row[0] + row[1]) not in flights_short:
                                # we just found a trip => add it to list trips
                                self.trips.append(flights + [row])

                                # call flight_combo_maker
                                self.flight_combo_maker(flights + [row], row[1], flights_short + [row[0] + row[1]])

    def trips_printer(self):
        """
        Print out the result in nice, readable form. Results are stored in list trips.
        :return:
        """
        print("DEPARTURE \t\t\t\t\t ARRIVAL \t\t\t\t\t DURATION")
        for trip in self.trips:
            total_price = 0
            for flight in trip:
                total_price = total_price + flight[5] + self.bags * flight[7]
                print("{}   {} \t {}   {} \t {}".format(flight[0], flight[2], flight[1], flight[3], flight[3]-flight[2]))
            print("Total price: {} EUR".format(total_price))
            print()

        # print the total number of existing trips
        print("Total number of trips: {}".format(len(self.trips)))


find_combination = FindCombination()
find_combination.reader()
find_combination.flight_combo_maker([], "", [])
find_combination.trips_printer()
