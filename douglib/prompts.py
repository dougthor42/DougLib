# -*- coding: utf-8 -*-
"""
Created on Mon Jul 07 14:15:43 2014

@author:        dthor

Usage:
    new_program.py

Options:
    -h --help           # Show this screen.
    --version           # Show version.
"""

# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
import getpass

# Third-Party

# Package


# ---------------------------------------------------------------------------
### Functions
# ---------------------------------------------------------------------------
def die_size():
    """ Prompts user for die size in mm. """
    die_x, die_y = (5, 5)
    while True:
        try:
            die_x = float(input("Die X size (mm): "))
            if die_x > 1000 or die_x <= 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid entry. Please enter a number between 0 and 1000.")

    while True:
        try:
            die_y = float(input("Die Y size (mm): "))
            if die_y > 1000 or die_y <= 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid entry. Please enter a number between 0 and 1000.")
    return (die_x, die_y)


def wafer_size():
    """ Prompts user for wafer size in mm. """
    while True:
        default = 150.0
        dia = input("Wafer diameter (mm) [%dmm]: " % default)
        if dia == "":
            dia = float(default)
            print("  Using default value of %dmm." % default)
            break
        else:
            try:
                dia = float(dia)
                if dia <= 0 or dia > 500:
                    raise ValueError
                break
            except ValueError:
                print("Invalid entry. Please enter a number between 0 and 500.")
    return dia


def exclusion_size():
    """ Prompts user for edge exclusion in mm. """
    while True:
        default = 5.0
        excl = input("Exclusion ring width (mm) [%dmm]: " % default)
        if excl == "":
            excl = float(default)
            print("  Using default value of %dmm." % default)
            break
        else:
            try:
                excl = float(excl)
                if excl < 0:
                    raise ValueError
                break
            except ValueError:
                print("Invalid entry. Please enter a number greater than 0.")
    return excl


def fss_exclusion():
    """ Prompts user for Front-Side Scribe Exclusion width. Also called Flat
    Exclusion """
    while True:
        default = 5.0
        fss = input("Front Side Scribe (Flat) Exclusion (mm) [%dmm]: " % default)
        if fss == "":
            fss = float(default)
            print("  Using default value of %dmm." % default)
            break
        else:
            try:
                fss = float(fss)
                if fss < 0:
                    raise ValueError
                break
            except ValueError:
                print("Invalid entry. Please enter a number greater than 0.")
    return fss


def plot():
    """ Asks user to plot the wafer map y/n. """
    print()
    while True:
        answer = input("Plot the wafer image? [N]: ").lower()
        if answer in ("", "n", "no"):
            return False
        elif answer in ("y", "yes"):
            return True
        else:
            print("Invalid entry. Please enter Yes or No.")


def y_n(prompt):
    """ Generic yes/no prompt with error handling. """
    while True:
        ans = input(prompt).lower()
        if ans in ("", "n", "no"):
            return False
        elif ans in ("y", "yes"):
            return True
        else:
            print("Invalid entry. Please enter Yes or No.")


def username():
    """ Prompts user for a login name. """
    while True:
        try:
            user = input("User: ")
            if user == '':
                raise ValueError
            break
        except ValueError:
            print("User cannot be blank.")
    return user


def password():
    """ Prompts user for a password. """
    while True:
        try:
            pwd = getpass.getpass("Password: ")
            break
        except:
            print("Unexpected error.")
            raise
    return pwd


def die_pattern_id():
    """ Prompts user for a die pattern ID (Reedholm). """
    while True:
        try:
            pattern_id = int(input("DiePattern_ID: "))
            break
        except ValueError:
            print("Invalid DiePattern_ID")
    return pattern_id


def wafer_info():
    """ Prompts the user for the wafer parameters used in mapping and GDW """
    die_xy = die_size()
    dia = wafer_size()
    excl = exclusion_size()
    fss = fss_exclusion()
    return (die_xy, dia, excl, fss)


def main():
    """ Main Code """
    pass


if __name__ == "__main__":
    main()
