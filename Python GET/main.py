#!/bin/python3

import math
import os
import random
import re
import sys
from xmlrpc.client import DateTime


#
# Complete the 'getUserTransaction' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts following parameters:
#  1. INTEGER uid
#  2. STRING txnType
#  3. STRING monthYear
#
#  https://jsonmock.hackerrank.com/api/transactions/search?userId=
#
import pip._vendor.requests as requests
import pandas as pd
from datetime import datetime


def getUserTransaction(uid, txnType, monthYear):
    # Get list of transactions using uid, 
    # Store in list transactions that match txnType and monthYear
    # Return id of transactions that are above average monthly spending
    URL = "https://jsonmock.hackerrank.com/api/transactions/search"
    params = {'userId': uid}
    session = requests.Session()
    listOfMatchingTransactions = []
    resultList = []
    totalSpending = 0
    # Get total number of pages
    response = requests.get(url=URL, params=params)
    jsonResponse = response.json()
    currentPage = jsonResponse.get('page')
    totalPages = jsonResponse.get('total_pages')
    # Process inputs 
    monthYearArr = monthYear.split('-')
    month = monthYearArr[0]
    # While loop to handle pagination and go through all records
    while(currentPage <= totalPages):
        response = session.get(url=URL, params={'userId': uid ,'page': currentPage}).json()
        transactionRecords = response.get('data')
        for record in transactionRecords:
            recordTimeStamp = record['timestamp']
            transactionDate = datetime.fromtimestamp(recordTimeStamp/1000.0)
            transactionMonth = str(transactionDate.month).zfill(2)
            transactionYear = str(transactionDate.year)
            transactionMonthYear = transactionMonth + "-" + transactionYear
            if (month == transactionMonth and record['txnType'] == 'debit'):
                totalSpending = totalSpending + float(record['amount'].replace('$', '').replace(',', ''))
            if (monthYear == transactionMonthYear and record['txnType'] == txnType):
                listOfMatchingTransactions.append(record)
        currentPage = currentPage + 1;

    averageSpending = totalSpending / len(listOfMatchingTransactions)
    for transaction in listOfMatchingTransactions:
        if (float(transaction['amount'].replace('$', '').replace(',', '')) > averageSpending):
            resultList.append(transaction['id'])
    return resultList


def main():
    result = getUserTransaction(4, 'debit', '02-2019')
    for transactionId in result:
        print(transactionId)


if __name__ == '__main__':
    main()
