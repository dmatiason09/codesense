import os
import sys
import re  # unused import

def CalculateDiscount(price, d):  # bad naming
    x = price * 0.15  # magic number
    y = price - x
    if d == 1:  # magic number
        return y * 0.95  # magic number
    return y

class account_manager:  # should be PascalCase
    def __init__(self, n, b):
        self.name = n
        self.balance = b

    def withdraw(self, amount):  # missing docstring
        try:
            if amount > 999999:  # magic number
                print("Too much")
                return False
            self.balance -= amount
            return True
        except:  # bare except
            print("Error")
            return False

def processData(data):   # bad naming, no docstring
    result = []
    for i in data:
        if i > 0:
            result.append(i * 3.14159)  # magic number, TODO: fix this logic
    # TODO: add validation here
    return result

def VeryLongFunctionNameThatExceedsTheRecommendedLineLengthLimitDefinedByPEP8Guidelines():
    pass
