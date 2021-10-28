import os
import math
import time
from datetime import datetime

def is_float(string):
    """
        Checks if string is a float by forcing catching ValueError.
        Does not count if string is an integer.
    """
    try:
        if float(string).is_integer():
            return False
        return True
    except ValueError:
        return False

def list_dir(dir_list, path):
    """
        Prints directories from dir_list of path.
        Display files with "info-" as name, "txt" as file extension,
        and folders.
    """
    print("Directory list of path \\" + path + ":")
    for i in dir_list:
        try:
            file_ext = i.split('.')[1].lower()
            if "info-" in i and file_ext == "txt":
                print(i) # display info-<name>.txt
        except IndexError:
            print(i) # display folder

def open_file(file_path):
    """
        Opens text file and return data from text in form of dictionary.
    """
    result = {}
    with open(file_path, "r", encoding = "utf-8-sig") as reader:
        txt = [r.strip() for r in reader.readlines()]
        for s in txt:
            strings = []
            value = 0
            for x in s.split():
                if is_float(x):
                    value = float(x)
                else:
                    strings.append(x)
            key = " ".join(strings) # combine strings
            result.update({key : value}) # add
    return result

def search():
    """
        Searches for the data file and returns processed data in form
        of dictionary.
    """
    is_found = False # make infinite loop, terminates when file is found
    dir_list = os.listdir() # list directories
    path = "" # current path
    # begin search
    while (not is_found):
        try:
            list_dir(dir_list, path)
            file_name = input("\nFile name: ") # user input
            # catch IndexError as folders do not have extension names
            file_ext = file_name.split('.')[1].lower()
            if file_name in dir_list:
                data = open_file(path + file_name)
                is_found = True
                return data # end search
            else:
                print("File does not exist.\n")
        except IndexError:
            if file_name not in dir_list:
                print("File does not exist.\n")
            else:
                if path.find("\\") == -1:
                    path += file_name # first time traversal
                else:
                    path += "\\" + file_name # recurring traversal
                path += "\\"
                dir_list = os.listdir(path) # update directory list

def save_text_data(file_name, dictionary):
    """
        Saves processed data into a text file.
    """
    with open(file_name, "w") as writer:
        for key in dictionary:
            writer.writelines(key + " " + str(dictionary[key]) + "\n")

def save_slp_data(file_name, key, value, php, usd, eth):
    """
        Saves SLP data into a text file.
    """
    with open("slp.txt", "w") as writer:
        writer.writelines("Current Date and Time: "
                          + str(datetime.now()) + "\n")
        for i, j, k, l, m in zip(key, value, php, usd, eth):
            writer.writelines(str(i) + ":\t"
                + str(j) + " SLP = " 
                + str(k) + " PHP = " 
                + str(l) + " USD = " 
                + str(m) + " ETH\n")

def breakdown(slp, dictionary):
    """
        Calculates equivalent SLP from percentage.
        Returns dictionary along with current price and total earned.
    """
    for key in dictionary:
        dictionary[key] = int(math.ceil(float(slp) * dictionary[key]))
    updated = {"Current Price" : 1, "Total Earned" : slp}
    updated.update(dictionary)
    return updated

def get_keys(dictionary):
    """
        Returns a list of key names in dictionary.
    """
    result = []
    for i in dictionary:
        result.append(i)
    return result

def get_values(dictionary):
    """
        Returns a list of key values in dictionary.
    """
    result = []
    for i in dictionary:
        result.append(dictionary[i])
    return result

def get_rate(dictionary, rate):
    """
        Returns a list of converted SLP depending on rate.
    """
    result = []
    for i in dictionary:
        result.append(dictionary[i] * rate)
    return result

is_running = True
data = {}

while (is_running):
    print("Main Menu")
    print("[1] Open data from directory")
    print("[2] Add data manually")
    print("[3] Save data")
    print("[4] View data")
    print("[5] Reset data")
    print("[9] Breakdown SLP to PHP, USD, and ETH")
    print("[0] Exit")

    option = int(input("Option: "))

    if option == 1:
        data = search()
    elif option == 2:
        is_adding = True
        while (is_adding):
            # user input
            key_name = input("Name: ")
            key_value = float(input("Percentage: "))
            data.update({key_name : key_value})

            # insert function to check if percentage is 100%

            decision = input("Add (Y/N)? ").lower()

            if decision == "n":
                is_adding = False
    elif option == 3:
        if data:
            text_name = input("File name: info-")
            save_text_data("info-" + text_name + ".txt", data)
        else:
            print("No input data.\n")
    elif option == 4:
        if data:
            for key in data:
                print(key + ": " + str(data[key] * 100.00) + "%")
            print()
        else:
            print("No input data.\n")
    elif option == 5:
        if data:
            data = {}
            print("Data cleared.\n")
        else:
            print("Data already cleared.\n")
    elif option == 9:
        if data:
            # user inputs
            slp_input = int(input("SLP: "))
            slp_name = input("File name: ")

            # access pycoingecko
            cg = CoinGeckoAPI()
            convert = cg.get_price(ids = "smooth-love-potion",
                                vs_currencies="php,usd,eth").values()
            rates = []

            # get conversion rate
            for currency in convert:
                for value in currency:
                    rates.append(currency[value])

            # calculate breakdown and get conversion rates
            breakdown = breakdown(slp_input, data)
            key = get_keys(breakdown)
            value = get_values(breakdown)
            php = get_rate(breakdown, rates[0])
            usd = get_rate(breakdown, rates[1])
            eth = get_rate(breakdown, rates[2])

            # output
            save_slp_data(slp_name, key, value, php, usd, eth)
        else:
            print("No input data.\n")
    elif option == 0:
        print("Program exit.")
        is_running = False
        time.sleep(1)