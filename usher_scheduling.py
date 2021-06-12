# -*- coding: UTF-8 -*-
from crew_class import Crew
import pandas as pd

# Theater cleaning term
theater_A = 5
theater_B = 5
theater_1 = 10
theater_2 = 10
theater_3 = 10
theater_4 = 10
theater_5 = 10
theater_6 = 10
theater_7 = 10
theater_8 = 10
theater_9 = 10
theater_10 = 10
theater_11 = 10

# Configure excel version
excelType = 0

# Read '어셔출근시간' and create DataFrame
try:
    print("*** Read excel file '어셔출근시간' ***")
    df = pd.read_excel('어셔출근시간.xls')
    excelType = 1
except FileNotFoundError:
    try:
        df = pd.read_excel('어셔출근시간.xlsx')
        excelType = 2
    except FileNotFoundError:
        print("Read file error")
    else:
        print("-> OK")

crew_name_list = df['크루'].values.tolist()
crew_time_list = df['출근시간'].values.tolist()  # int type

crew_list = []

# Create Crew object
for i in range(0, len(crew_name_list)):
    crew_list.append(Crew(crew_name_list[i],  # name
                     crew_time_list[i],  # start time
                     crew_time_list[i] + 630,  # Work during 06:30
                     i))  # index

    # Calculate over the 60 minute
    if crew_list[i].end_time % 100 >= 60:
        crew_list[i].end_time += 40  # - 60minute, + 1hour

    # Calculate over the 24 hour
    if crew_list[i].end_time >= 25:
        crew_list[i].end_time - 2400

# Read '최종스케줄' and create DataFrame
try:
    print("*** Read excel file '최종스케줄' ***")
    df = pd.read_excel('최종스케줄.xls')
except FileNotFoundError:
    try:
        df = pd.read_excel('최종스케줄.xlsx')
    except FileNotFoundError:
        print("Read file error")
    else:
        print("-> OK")

