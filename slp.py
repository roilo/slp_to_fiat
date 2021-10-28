"""
    Program that calculates percentage breakdown of SLP earnings.
    Edit the key value pairs within variable result in breakdown()
    depending on your own percentage share.
    Please install pycoingecko first.
    Link: https://pypi.org/project/pycoingecko/
"""

from pycoingecko import CoinGeckoAPI
from datetime import datetime
import math

# breakdown slp earnings to percentage
def breakdown(slp):
    result = {
        "Current Price" : 1,
        "Total Earned" : int(slp),
        # <breakdown name> : int(math.ceil(float(slp) * <percentage>))
        "Pay Bills" : int(math.ceil(float(slp) * 0.3)),
        "Profit RR" : int(math.ceil(float(slp) * 0.3)),
        "Pay Debts" : int(math.ceil(float(slp) * 0.1)),
        "Building EF" : int(math.ceil(float(slp) * 0.1)),
        "Profit Roy" : int(math.ceil(float(slp) * 0.2))
    }
    return result

# get name of keys in dictionary
def get_keys(dictionary):
    result = []
    for i in dictionary:
        result.append(i)
    return result

# get value of keys in dictionary
def get_value(dictionary):
    result = []
    for i in dictionary:
        result.append(dictionary[i])
    return result

# get conversion rate
def get_rate(dictionary, rate):
    result = []
    for i in dictionary:
        result.append(dictionary[i] * rate)
    return result

# input
slp = int(input("SLP: "))

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
breakdown = breakdown(slp)
key = get_keys(breakdown)
value = get_value(breakdown)
php = get_rate(breakdown, rates[0])
usd = get_rate(breakdown, rates[1])
eth = get_rate(breakdown, rates[2])

# output
with open("slp.txt", "w") as writer:
    writer.writelines("Current Date and Time: " + str(datetime.now()) + "\n")
    for i,j,k,l,m in zip(key, value, php, usd, eth):
        writer.writelines(str(i) + ":\t"
            + str(j) + " SLP = " 
            + str(k) + " PHP = " 
            + str(l) + " USD = " 
            + str(m) + " ETH\n")

