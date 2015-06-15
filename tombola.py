#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'werdeil'

import random
import csv


def random_select(list_names):
    '''Return a name choosen randomly from the list'''
    return random.choice(list_names)


def draw_prices(list_prices, list_names):
    '''For each price of the list_prices, draw a name from list_names'''
    for price in list_prices:
        if len(list_names) == 0:
            raise ValueError("Too many prices, not enough people")
        print "price to win ... %s" % price
        random.shuffle(list_names)
        print " et le gagnant est : %s" % list_names.pop(0)


def draw_name(list_names):
    '''Return a name choosen randomly from the list and the list without the name'''
    random.shuffle(list_names)
    name = list_names.pop(0)
    return name, list_names


def import_lists(csv_file):
    '''Read a csv file and return the list of names'''
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        list_names = []
        for row in reader:
            if row['Prenom'] != "":
                list_names.append("%s %s" % (row['Prenom'], row['Nom']))

        return list_names
        
def import_prices(csv_file):
    '''Read a csv file and return the list of prices'''
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        list_prices = []
        for row in reader:
            if row['Price'] != "":
                list_prices.append(row['Price'])

        return list_prices


def write_results(save_file, name, objet):
    '''Save the result of the tombola in a file'''
    save_file = open(save_file, 'a')
    save_file.write("%s;%s\n" % (name, objet))
    save_file.close()
