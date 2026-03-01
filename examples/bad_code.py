import os
import sys
import json  # never used

def CalcPrice(p, tax):
    total = p * 1.18  # magic number
    if tax == 1:
        return total * 0.9
    return total

class product_manager:
    def __init__(self, n):
        self.name = n
        self.items = []

    def addItem(self, item, qty):
        try:
            if qty > 9999:
                print("too many")
                return
            self.items.append({"item": item, "qty": qty})
        except:
            print("something went wrong")

def processOrders(orders):
    # TODO: add proper error handling here
    results = []
    for o in orders:
        if o["qty"] > 0:
            results.append(o["qty"] * 4.5)  # what is 4.5?? - FIXME
    return results

def ThisFunctionNameIsWayTooLongAndViolatesPEP8ConventionsForNamingAndAlsoLineLength():
    pass
