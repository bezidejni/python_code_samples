#!/usr/bin/env python


def convert(celsius):
    """Takes a temperature in degrees Celsius and converts it to Fahrenheit """
    try:
        celsius = float(celsius)
    except ValueError:
        print "%s is not a numeric value" % celsius
        raise TypeError
    fahrenheit = celsius * (9 / 5.) + 32
    return fahrenheit
