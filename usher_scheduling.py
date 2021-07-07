# -*- coding: UTF-8 -*-
import pandas

from crew_class import Crew, Assignment
from usher_algorithm import usher_scheduling_algorithm
import pandas as pd


def make_usher_scheduling_file(avg_threshold):
    # Theater cleaning term dictionary
    cleaning_term_dict = {
        'Dolby Cinema': 10,
        '2관': 8,
        '3관': 8,
        '4관': 8,
        '5관': 8,
        '6관': 8,
        '7관': 8,
        '8관': 8,
        '9관': 8,
        '10관': 8,
        '11관': 8,
        '스크린A': 5,
        '스크린B': 5
    }

    # Theater num is odd or even
    odd_or_even_dict = {
            'Dolby Cinema': 'odd',
            '2관': 'even',
            '3관': 'odd',
            '4관': 'even',
            '5관': 'odd',
            '6관': 'even',
            '7관': 'odd',
            '8관': 'even',
            '9관': 'odd',
            '10관': 'even',
            '11관': 'odd',
            '스크린A': 'etc',
            '스크린B': 'etc'
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
            return False, 0
        else:
            print("-> OK")

    crew_name_list = usher_time_df['크루'].values.tolist()
    crew_time_list = usher_time_df['출근시간'].values.tolist()  # int type
    crew_rest_time_list = usher_time_df['휴게시간'].values.tolist()

    # Create Crew object
    try:
        print("*** Create Crew object ***")
        crew_list = []
        for i in range(0, len(crew_name_list)):
            if pandas.isna(crew_rest_time_list[i]):
                crew_rest_time_list[i] = crew_time_list[i] + 300  # 칸 비어있을경우 출근 후 3시간뒤 휴게
                if crew_rest_time_list[i] >= 2500:  # +3시간 해서 새벽 1시 이후로 되는경우
                    crew_rest_time_list[i] -= 2400
            crew_list.append(Crew(crew_name_list[i],  # name
                             crew_time_list[i] + 5,  # start time (5분 미팅시간)
                             crew_time_list[i] + 625,  # Work during 06:30 - 5(퇴근전 5분 여유)
                             crew_rest_time_list[i],  # 휴게 시작시간
                             i))  # index

            # Calculate over the 60 minute
            if crew_list[i].start_time % 100 >= 60:
                crew_list[i].start_time += 40  # - 60minute, + 1hour

            # Calculate over the 24 hour
            if crew_list[i].start_time >= 2500:
                crew_list[i].start_time -= 2400

            # Calculate over the 60 minute
            if crew_list[i].end_time % 100 >= 60:
                crew_list[i].end_time += 40  # - 60minute, + 1hour

            # # Calculate over the 24 hour
            # if crew_list[i].end_time >= 2500:
            #     crew_list[i].end_time -= 2400
    except:
        print("Error")
        return False, 0
    else:
        print("-> OK")

    # Read ErrorTime.excel and create DataFrame
    try:
        print("*** Read excel file '반불시간' ***")
        df_er = pd.read_excel('반불시간.xls', sheet_name='반불시간', header=1)
    except FileNotFoundError:
        try:
            df_er = pd.read_excel('반불시간.xlsx', sheet_name='반불시간', header=1)
        except FileNotFoundError:
            print("Read file error")
            return False, 0
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
        return False, 0
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
            return False, 0
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
        return False, 0
    else:
        print("-> OK")

    temp_list = movie_schedule_df['상영관'].values.tolist()
    movie_theater_num_list = []
    movie_work_class_list = []

    # 상영관 이름, 입퇴장 을 읽어와서 공백을 기준으로 구분
    try:
        print("*** Slicing '상영관' ***")
        for n in temp_list:
            tmp = n.split()
            if tmp[0] == 'Dolby':
                movie_theater_num_list.append(tmp[0] + ' ' + tmp[1])
                movie_work_class_list.append(tmp[2])
            else:
                movie_theater_num_list.append(tmp[0])
                movie_work_class_list.append(tmp[1])
    except:
        print("Error")
        return False, 0
    else:
        print("-> OK")

    # Create Assignment object
    try:
        print("*** Create Assignment object ***")
        assignment_list = []
        for i in range(0, len(movie_theater_num_list)):
            assignment_list.append(Assignment(movie_name_list[i],  # movie name
                                              movie_theater_num_list[i],  # theater number
                                              movie_work_class_list[i],  # work_class (입장 or 퇴장)
                                              movie_time_list[i],  # 입/퇴장시간
                                              er_list,  # 반불시간 리스트
                                              cleaning_term_dict,  # 관 별 청소시간 dictionary
                                              odd_or_even_dict[movie_theater_num_list[i]]  # 짝수관 or 홀수관 or etc
                                              ))
    except:
        print("Error")
        return False, 0
    else:
        print("-> OK")

    # ----------------------------------------------------------------------------------- ↑ 파일 읽어오기 및 object 생성
    # ----------------------------------------------------------------------------------- ↓ 스케줄링 알고리즘
    # Dolby Cinema를 Dolby 로 변경
    name_change_dict = {'Dolby Cinema': 'Dolby'}
    theater_name_list = temp_list.copy()
    i = 0
    for n in temp_list:
        tmp = n.split()
        if tmp[0] == 'Dolby':
            new_theater_name = tmp[0] + ' ' + tmp[2]
            theater_name_list[i] = new_theater_name
        i += 1
    movie_schedule_df['상영관'] = theater_name_list

    try:
        print('*** Process usher scheduling algorithm ***')
        assigned_list, crew_list = usher_scheduling_algorithm(crew_list, assignment_list, avg_threshold)
    except:
        print("Error")
        return False, 0
    else:
        print("----> OK")


    # 입/퇴장 담당자 리스트 만들기
    try:
        print("*** Create OutPut DataFrame ***")
        worker = []
        for work in assigned_list:
            worker.append(work.name)

        movie_schedule_df = movie_schedule_df.drop([movie_schedule_df.columns[0]], axis='columns')
        movie_schedule_df['담당자'] = worker
    except:
        print("Error")
        return False, 0
    else:
        print("-> OK")

    try:
        print("*** Create '어셔반영스케줄' ***")

        if excelType == 1:
            movie_schedule_df.to_excel('어셔반영스케줄.xls')
        elif excelType == 2:
            movie_schedule_df.to_excel('어셔반영스케줄.xlsx')
    except:
        print("Error")
        return False, 0
    else:
        print("-> OK")

    print("*** 파일이 생성되었습니다 ***")

    return True, crew_list
