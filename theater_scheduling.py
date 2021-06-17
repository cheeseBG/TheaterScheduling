# -*- coding: UTF-8 -*-
import pandas as pd


def make_scheduling_file():
    excelType = 0

    try:
        # Read Usher schedule and create DataFrame
        print("*** Read excel file '어셔스케줄' ***")
        df = pd.read_excel('어셔스케줄.xls')
        df = df.drop("상영일자", axis=1)
        df = df.drop("퇴장크루", axis=1)
        df_list = df.values.tolist()
        excelType = 1
    except:
        try:
            df = pd.read_excel('어셔스케줄.xlsx')
            df = df.drop("상영일자", axis=1)
            df = df.drop("퇴장크루", axis=1)
            df_list = df.values.tolist()
            excelType = 2
        except:
            print("Read file error")
            return False
        else:
            print("-> OK")

    # Convert datetime -> string type
    try:
        print("*** Convert '어셔스케줄' dateTime -> string type ***")
        for i in range(0, len(df_list)):
            df_list[i][3] = str(df_list[i][3])
            df_list[i][3] = df_list[i][3][0:5]
            df_list[i][4] = str(df_list[i][4])
            df_list[i][4] = df_list[i][4][0:5]
    except:
        print("Error")
        return False
    else:
        print("-> OK")

    # Read ErrorTime.excel and create DataFrame
    try:
        print("*** Read excel file '반불시간' ***")
        df_er = pd.read_excel('반불시간.xls', sheet_name='반불시간', header=1)
        df_er_list = df_er.values.tolist()
    except:
        try:
            df_er = pd.read_excel('반불시간.xlsx', sheet_name='반불시간', header=1)
            df_er_list = df_er.values.tolist()
        except:
            print("Read file error")
            return False
        else:
            print("-> OK")

    # Convert datetime -> string type
    try:
        print("*** Convert '반불시간' dateTime -> string type ***")
        for i in range(0, len(df_er_list)):
            df_er_list[i][1] = str(df_er_list[i][1])
            df_er_list[i][1] = df_er_list[i][1][0:5]
    except:
        print("Error")
        return False
    else:
        print("-> OK")

    class MovieList:
        def __init__(self):
            self.kind = ""
            self.name = ""
            self.number = ""
            self.start = ""
            self.end = ""
            self.order = ""
            self.checkS = 0
            self.checkE = 0

    def initMovieList(df_list, i):
        list = MovieList()

        list.kind = df_list[i][0]
        list.name = str(df_list[i][1])
        list.number = df_list[i][2]
        list.start = df_list[i][3]
        list.end = df_list[i][4]
        list.order = df_list[i][5]

        return list

    # Initialize movie list set -> except '더부티크'
    try:
        print("*** Initialize '어셔스케줄' list (Except '더부티크') ***")
        m_list = []
        for i in range(0, len(df_list)):
            if df_list[i][2].find('더부티크') == -1:  # and df_list[i][2].find('스크린') == -1:
                m_list.append(initMovieList(df_list, i))

    except:
        print("Error")
        return False
    else:
        print("-> OK")

    class ErrorList:
        def __init__(self):
            self.name = ""
            self.time = ""
            self.rating = ""

    def initErrorList(df_er_list, i):
        list = ErrorList()

        list.name = str(df_er_list[i][0])
        list.time = df_er_list[i][1]
        list.rating = df_er_list[i][2]

        return list

    # Initialize error time list set
    try:
        print("*** Initialize '반불시간' list ***")
        er_list = []
        for i in range(0, len(df_er_list)):
            er_list.append(initErrorList(df_er_list, i))
    except:
        print("Error")
        return False
    else:
        print("-> OK")

    # Function : Check equal name of movie and return error time
    def equal_name_ert(m_list, er_list, i):
        result = int(0)

        for j in range(0, len(er_list)):
            # 3D Dolby 더빙
            if er_list[j].name.find(m_list[i].name) != -1 and m_list[i].kind.find('3D') != -1 and m_list[i].kind.find(
                    'Dolby') != -1 and m_list[i].kind.find('더빙') != -1 and er_list[j].name.find('3D Dolby 더빙') != -1:
                result = int(er_list[j].time[3:])
            # 3D Dolby
            elif er_list[j].name.find(m_list[i].name) != -1 and m_list[i].kind.find('3D') != -1 and m_list[i].kind.find(
                    'Dolby') != -1 and m_list[i].kind.find('더빙') == -1 and er_list[j].name.find('3D Dolby') != -1 and \
                    er_list[j].name.find('더빙') == -1:
                result = int(er_list[j].time[3:])
            # 3D 더빙
            elif er_list[j].name.find(m_list[i].name) != -1 and m_list[i].kind.find('3D') != -1 and m_list[i].kind.find(
                    'Dolby') == -1 and m_list[i].kind.find('더빙') != -1 and er_list[j].name.find('3D 더빙') != -1 and \
                    er_list[j].name.find('Dolby') == -1:
                result = int(er_list[j].time[3:])
            # 3D
            elif er_list[j].name.find(m_list[i].name) != -1 and m_list[i].kind.find('3D') != -1 and m_list[i].kind.find(
                    'Dolby') == -1 and m_list[i].kind.find('더빙') == -1 and er_list[j].name.find('3D') != -1 and er_list[
                j].name.find('Dolby') == -1 and er_list[j].name.find('더빙') == -1:
                result = int(er_list[j].time[3:])
            # 2D Dolby 더빙
            elif er_list[j].name.find(m_list[i].name) != -1 and m_list[i].kind.find('2D') != -1 and m_list[i].kind.find(
                    'Dolby') != -1 and m_list[i].kind.find('더빙') != -1 and er_list[j].name.find('Dolby 더빙') != -1 and \
                    er_list[j].name.find('3D') == -1:
                result = int(er_list[j].time[3:])
            # 2D Dolby
            elif er_list[j].name.find(m_list[i].name) != -1 and m_list[i].kind.find('2D') != -1 and m_list[i].kind.find(
                    'Dolby') != -1 and m_list[i].kind.find('더빙') == -1 and er_list[j].name.find('Dolby') != -1 and \
                    er_list[j].name.find('3D') == -1 and er_list[j].name.find('더빙') == -1:
                result = int(er_list[j].time[3:])
            # 2D 더빙
            elif er_list[j].name.find(m_list[i].name) != -1 and m_list[i].kind.find('2D') != -1 and m_list[i].kind.find(
                    'Dolby') == -1 and m_list[i].kind.find('더빙') != -1 and er_list[j].name.find('Dolby') == -1 and \
                    er_list[j].name.find('3D') == -1 and er_list[j].name.find('더빙') != -1:
                result = int(er_list[j].time[3:])
            # 2D
            elif er_list[j].name.find(m_list[i].name) != -1 and m_list[i].kind.find('2D') != -1 and m_list[i].kind.find(
                    'Dolby') == -1 and m_list[i].kind.find('더빙') == -1 and er_list[j].name.find('Dolby') == -1 and \
                    er_list[j].name.find('3D') == -1 and er_list[j].name.find('더빙') == -1:
                result = int(er_list[j].time[3:])

        return result

    # Set : start time -= 10 || end time -= error time
    def setTime(m_list, er_list):
        for i in range(0, len(m_list)):
            s_h = m_list[i].start[:2]
            s_m = m_list[i].start[3:]
            e_h = m_list[i].end[:2]
            e_m = m_list[i].end[3:]

            # start time - 10
            if int(s_m) - 10 == 0:
                m_list[i].start = s_h + ":00"
            elif int(s_m) - 10 > 0 and (int(s_m) - 10) // 10 == 0:
                m_list[i].start = s_h + ":0" + str(int(s_m) - 10)
            elif int(s_m) - 10 > 0:
                m_list[i].start = s_h + ":" + str(int(s_m) - 10)
            elif int(s_m) - 10 < 0:
                if (int(s_h) - 1) // 10 == 0:
                    s_h = "0" + str(int(s_h) - 1)
                    s_m = str(60 + (int(s_m) - 10))
                    m_list[i].start = s_h + ":" + s_m
                else:
                    s_h = str(int(s_h) - 1)
                    s_m = str(60 + (int(s_m) - 10))
                    m_list[i].start = s_h + ":" + s_m

            error = equal_name_ert(m_list, er_list, i)
            # end time - error time
            if int(e_m) - error == 0:
                m_list[i].end = e_h + ":00"
            elif int(e_m) - error > 0 and (int(e_m) - error) // 10 == 0:
                m_list[i].end = e_h + ":0" + str(int(e_m) - error)
            elif int(e_m) - error > 0:
                m_list[i].end = e_h + ":" + str(int(e_m) - error)
            elif int(e_m) - 10 < 0:
                if (int(e_h) - 1) // 10 == 0:
                    e_h = "0" + str(int(e_h) - 1)
                    e_m = str(60 + (int(e_m) - error))
                    m_list[i].end = e_h + ":" + e_m
                else:
                    e_h = str(int(e_h) - 1)
                    e_m = str(60 + (int(e_m) - error))
                    m_list[i].end = e_h + ":" + e_m

        return m_list

    # Set m_list time
    try:
        print("*** Set start,end time of movie ***")
        m_list = setTime(m_list, er_list)
    except:
        print("Error")
        return False
    else:
        print("-> OK")

    # Class : Output
    class Output:
        def __init__(self):
            self.time = ""
            self.SEtime = ""
            self.number = ""
            self.order = ""
            self.rating = ""
            self.name = ""

    # Function : Create output object
    def start_object(m_list, er_list):
        output = Output()

        output.SEtime = m_list.start

        if m_list.number.find('컴포트') != -1:
            output.number = m_list.number[4:] + " 입장"
        else:
            output.number = m_list.number + " 입장"

        output.order = m_list.order

        if m_list.kind.find('더빙') != -1:
            output.name = "(더빙) " + m_list.name
        elif m_list.kind.find('Dolby') != -1:
            output.name = "(Dolby) " + m_list.name
        else:
            output.name = m_list.name

        # Initialize rating
        for i in range(0, len(er_list)):
            if er_list[i].name.find(m_list.name) != -1:
                output.rating = er_list[i].rating

        return output

    def end_object(m_list, er_list):
        output = Output()

        output.SEtime = m_list.end

        if m_list.number.find('컴포트') != -1:
            output.number = m_list.number[4:] + " 퇴장"
        else:
            output.number = m_list.number + " 퇴장"

        output.order = m_list.order

        if m_list.kind.find('더빙') != -1:
            output.name = "(더빙) " + m_list.name
        elif m_list.kind.find('Dolby') != -1:
            output.name = "(Dolby) " + m_list.name
        else:
            output.name = m_list.name

        # Initialize rating
        for i in range(0, len(er_list)):
            if er_list[i].name.find(m_list.name) != -1:
                output.rating = er_list[i].rating

        return output

    # Function : Sort by earier time
    def sort_by_time(m_list, er_list):
        output = []
        cnt = int(1)

        while cnt <= len(m_list) * 2:
            min = 5000
            min_idx = [int(-1), 's']

            for i in range(len(m_list)):
                tmp_s = int(m_list[i].start[:2] + m_list[i].start[3:])
                tmp_e = int(m_list[i].end[:2] + m_list[i].end[3:])

                # Check start,end time
                if min > tmp_s and m_list[i].checkS == 0:
                    min = tmp_s
                    min_idx = [i, 's']
                elif min > tmp_e and m_list[i].checkE == 0:
                    min = tmp_e
                    min_idx = [i, 'e']

            if min_idx[1] == 's':
                output.append(start_object(m_list[min_idx[0]], er_list))
                m_list[min_idx[0]].checkS = 1
            elif min_idx[1] == 'e':
                output.append(end_object(m_list[min_idx[0]], er_list))
                m_list[min_idx[0]].checkE = 1
            else:
                print("Error : Object sorting error!")
            cnt += 1

        return output

    try:
        print("*** Sort by time ***")
        output = sort_by_time(m_list, er_list)
    except:
        print("Error")
        return False
    else:
        print("-> OK")

    # Set time line of output list
    try:
        print("*** Set timeline ***")
        clk = int(output[0].SEtime[0:2])
        for i in range(0, len(output)):
            if int(output[i].SEtime[0:2]) == clk:
                if clk >= 24:
                    output[i].time = str(clk - 24) + "시"
                else:
                    output[i].time = str(clk) + "시"
                clk += 1
    except:
        print("Error")
        return False
    else:
        print("-> OK")

    # Output DataFrame
    col_names = ['시간', '입/퇴장시간', '상영관', '회차', '등급', '영화명']

    values = []

    # Set values
    try:
        print("*** Set OutPut values ***")
        for i in range(0, len(output)):
            tmp_val = []
            tmp_val.append(output[i].time)
            tmp_val.append(output[i].SEtime)
            tmp_val.append(output[i].number)
            tmp_val.append(output[i].order)
            tmp_val.append(output[i].rating)
            tmp_val.append(output[i].name)
            values.append(tmp_val)
    except:
        print("Error")
        return False
    else:
        print("-> OK")

    try:
        print("*** Create OutPut DataFrame ***")
        df_test = pd.DataFrame(values, columns=col_names)
    except:
        print("Error")
        return False
    else:
        print("-> OK")

    try:
        print("*** Create '최종스케줄' ***")

        if excelType == 1:
            df_test.to_excel('최종스케줄.xls')
        elif excelType == 2:
            df_test.to_excel('최종스케줄.xlsx')
    except:
        print("Error")
        return False
    else:
        print("-> OK")

    print("*** 파일이 생성되었습니다 ***")

    return True
