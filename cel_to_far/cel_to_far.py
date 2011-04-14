#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys


def convert(celsius):
    """Takes a temperature in degrees Celsius and converts it to Fahrenheit """
    try:
        celsius = float(celsius)
    except ValueError:
        print "%s is not a numeric value" % celsius
        raise TypeError
    fahrenheit = celsius * (9 / 5.) + 32
    return fahrenheit

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Usage: ./cel_to_far.py temp_in_cel"
    else:
        celsius = sys.argv[1]
        fahrenheit = convert(celsius)
        print "%s°C = %.2f°F" % (celsius, fahrenheit)
