# -*- coding: UTF-8 -*-
from crew_class import Crew, Assignment
import pandas as pd

# Theater cleaning term dictionary
cleaning_term_dict = {
    '돌비시네마관': 10,
    '2관': 10,
    '3관': 10,
    '4관': 10,
    '5관': 10,
    '6관': 10,
    '7관': 10,
    '8관': 10,
    '9관': 10,
    '10관': 10,
    '11관': 10,
    '스크린A': 5,
    '스크린B': 5
}

# Configure excel version
excelType = 0

# Read '어셔출근시간' and create DataFrame
try:
    print("*** Read excel file '어셔출근시간' ***")
    usher_time_df = pd.read_excel('어셔출근시간.xls')
    excelType = 1
except FileNotFoundError:
    try:
        usher_time_df = pd.read_excel('어셔출근시간.xlsx')
        excelType = 2
    except FileNotFoundError:
        print("Read file error")
    else:
        print("-> OK")

crew_name_list = usher_time_df['크루'].values.tolist()
crew_time_list = usher_time_df['출근시간'].values.tolist()  # int type

# Create Crew object
crew_list = []
for i in range(0, len(crew_name_list)):
    crew_list.append(Crew(crew_name_list[i],  # name
                     crew_time_list[i],  # start time
                     crew_time_list[i] + 630,  # Work during 06:30
                     i))  # index

    # Calculate over the 60 minute
    if crew_list[i].end_time % 100 >= 60:
        crew_list[i].end_time += 40  # - 60minute, + 1hour

    # Calculate over the 24 hour
    if crew_list[i].end_time >= 2500:
        crew_list[i].end_time -= 2400

# Read ErrorTime.excel and create DataFrame
try:
    print("*** Read excel file '반불시간' ***")
    df_er = pd.read_excel('반불시간.xls', sheet_name='반불시간', header=1)
except FileNotFoundError:
    try:
        df_er = pd.read_excel('반불시간.xlsx', sheet_name='반불시간', header=1)
    except FileNotFoundError:
        print("Read file error")
    else:
        print("-> OK")

er_list = df_er.values.tolist()

# Convert datetime -> integer type
try:
    print("*** Convert '반불시간' dateTime -> int type ***")
    for k in range(0, len(er_list)):
        er_list[k][1] = str(er_list[k][1])
        er_list[k][1] = int(er_list[k][1][3:5])
except :
    print("Error")
else:
    print("-> OK")


# Read '최종스케줄' and create DataFrame
try:
    print("*** Read excel file '최종스케줄' ***")
    movie_schedule_df = pd.read_excel('최종스케줄.xls')
except FileNotFoundError:
    try:
        movie_schedule_df = pd.read_excel('최종스케줄.xlsx')

    except FileNotFoundError:
        print("Read file error")
    else:
        print("-> OK")

movie_time_list = movie_schedule_df['입/퇴장시간'].values.tolist()
movie_name_list = movie_schedule_df['영화명'].values.tolist()

# Convert datetime -> integer type
try:
    print("*** Convert '입/퇴장시간' dateTime -> int type ***")
    for k in range(0, len(movie_time_list)):
        movie_time_list[k] = str(movie_time_list[k])
        movie_time_list[k] = int(movie_time_list[k][0:2] + movie_time_list[k][3:5])
except :
    print("Error")
else:
    print("-> OK")

temp_list = movie_schedule_df['상영관'].values.tolist()
movie_theater_num_list = []
movie_work_class_list = []

# 상영관 이름, 입퇴장 을 읽어와서 공백을 기준으로 구분
for n in temp_list:
    tmp = n.split()
    movie_theater_num_list.append(tmp[0])
    movie_work_class_list.append(tmp[1])

# Create Assignment object
assignment_list = []
for i in range(0, len(movie_theater_num_list)):
    assignment_list.append(Assignment(movie_name_list[i],  # movie name
                                      movie_theater_num_list[i],  # theater number
                                      movie_work_class_list[i],  # work_class (입장 or 퇴장)
                                      movie_time_list[i],  # 입/퇴장시간
                                      er_list,  # 반불시간 리스트
                                      cleaning_term_dict  # 관 별 청소시간 dictionary
                                      ))


# ----------------------------------------------------------------------------------- ↑ 파일 읽어오기 및 object 생성
# ----------------------------------------------------------------------------------- ↓ 스케줄링 알고리즘


