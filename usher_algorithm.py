'''
  입장, 퇴장의 평균을 구하여 균등하게 분배,
  남는 work는 지원으로 채우기
  짝수, 홀수 관에 따라 입장시간이 겹치는 경우 threshold를 설정하여 동시 work 할당
  크루인덱스는 0부터


  ** 필요변수 **
  threshold -> 같은 홀수 혹은 짝수관 입장을 받을때 threshold 아래인 경우 일 중복할당 가능 (최대 3개 관)  ok
  max_enter_num -> 최대 동시 입장받는 관 수  ok
  working_crew_list -> 출근한 크루들을 담아두는 리스트 크루 object 저장  ok

  ** 필요함수 **
  calculate_avg_work_num -> 평균
  refresh_working_crew_list -> 현재 할당을 기다리는 work 시간 기준으로 크루 출근, 크루 퇴근   ok
  searching_working_num -> 일 횟수 searching 후 가장 적당한 크루 return
  check_enter_working -> 홀수 또는 짝수 또는 스크린관 정보를 parameter로 받아서 해당 영역 관 입장을 받고 있는 크루 리스트 출력
  enable_enter_crew -> 동시에 입장받을 수 있는지 확인하는 함수 // 스크린 A,B인 경우 동시 퇴장도 가능  크루 한명 return
  assign_work -> 일횟수 searching, 동시에 입장받을 수 있는지 check(평균 입장수 넘어가면 pass), 적당한 크루에게 일 할당

'''


# 입/퇴장 수가 크루 수로 정확히 안눠질경우 버림 -> 나머지는 지원으로
def calculate_avg_work_num(assignment_list, crew_list):
    assignment_num = len(assignment_list)
    crew_num = len(crew_list)

    avg_num = int((assignment_num / 2) / crew_num)  # 평균 입/퇴장 받기 수

    return avg_num


# working_crew_list 로 넘어간 object는 crew_list에서 제거
def refresh_working_crew_list(work_obj, working_crew_list, crew_list):
    current_time = work_obj.start_time

    # 새벽 1시에서 5시 사이인경우 2500~2900으로 시간을 바꿔서 계산 편리하도록
    if 100 <= current_time < 500:
        current_time += 2400

    # 현재 시간을 기준으로 업무를 할당받은 크루들의 work_end_time이 지났으면 working_done 실행
    for i in range(0, len(working_crew_list)):
        work_end_time = working_crew_list[i].work_end_time

        # 새벽 1시에서 5시 사이인경우 2500~2900으로 시간을 바꿔서 계산 편리하도록
        if 100 <= work_end_time < 500:
            work_end_time += 2400

        if work_end_time < current_time:
            working_crew_list[i].working_done()

    # 크루 출근
    new_crew_list = crew_list.copy()
    for crew in crew_list:
        if crew.start_time <= current_time:
            working_crew_list.append(crew)
            new_crew_list.remove(crew)

    # 크루 퇴근
    new_working_crew_list = working_crew_list.copy()
    for crew in working_crew_list:
        if crew.end_time <= current_time:
            new_working_crew_list.remove(crew)

    # 현재 시간을 기준으로 출근한 크루들의 휴게상태 변경
    for i in range(0, len(new_working_crew_list)):
        rest_start_time = new_working_crew_list[i].rest_time
        rest_end_time = new_working_crew_list[i].rest_end_time

        # 새벽 1시에서 5시 사이인경우 2500~2900으로 시간을 바꿔서 계산 편리하도록
        if 100 <= rest_start_time < 500:
            rest_start_time += 2400

        if 100 <= rest_end_time < 500:
            rest_end_time += 2400

        if rest_start_time <= current_time <= rest_end_time:
            new_working_crew_list[i].rest_state = True
        else:
            new_working_crew_list[i].rest_state = False

    return new_working_crew_list, new_crew_list


def check_enter_working(odd_or_even, working_crew_list):
    enable_list = []

    for crew in working_crew_list:
        if crew.work_info == odd_or_even:
            enable_list.append(crew)

    if len(enable_list) == 0:
        return 0
    else:
        return enable_list


def enable_enter_crew(work_obj, crew_list, threshold, max_enter_num, avg_enter_num):
    work_start_time = work_obj.start_time
    odd_or_even = work_obj.odd_or_even

    enable_crew_list = []
    for crew in crew_list:
        crew_work_start_time = crew.work_start_time
        crew_odd_or_even = crew.work_info

        # 새벽 1시에서 5시 사이인경우 2500~2900으로 시간을 바꿔서 계산 편리하도록
        if 100 <= work_start_time < 500:
            work_start_time += 2400

        if 100 <= crew_work_start_time < 500:
            crew_work_start_time += 2400

        # 크루 입장 시작시간과 현재 할당해야하는 업무 입장시간의 차이 계산
        work_hour = int(work_start_time / 100)
        crew_hour = int(crew_work_start_time / 100)
        error_hour_to_minute = (work_hour - crew_hour) * 60
        work_minute = (work_start_time % 100) + error_hour_to_minute
        crew_minute = crew_work_start_time % 100

        calc_minute = abs(crew_minute - work_minute)

        # 스크린A,B 인경우 입/퇴장 상관없이 중복으로 가능
        if crew.end_time >= work_obj.end_time and odd_or_even == 'etc' and work_obj.work_class == '입장' and crew.rest_state is False:
            if odd_or_even == crew_odd_or_even and crew.working < max_enter_num and calc_minute <= threshold and crew.enter_count < avg_enter_num:
                if work_start_time <= crew.rest_time and crew.rest_time >= work_obj.end_time:
                    enable_crew_list.append(crew)
                elif work_start_time >= crew.rest_time and work_start_time >= crew.rest_end_time:
                    enable_crew_list.append(crew)
        elif crew.end_time >= work_obj.end_time and odd_or_even == 'etc' and work_obj.work_class == '퇴장' and crew.rest_state is False:
            if odd_or_even == crew_odd_or_even and crew.working < max_enter_num and calc_minute <= threshold and crew.exit_count < avg_enter_num:
                if work_start_time <= crew.rest_time and crew.rest_time >= work_obj.end_time:
                    enable_crew_list.append(crew)
                elif work_start_time >= crew.rest_time and work_start_time >= crew.rest_end_time:
                    enable_crew_list.append(crew)
        # 스크린 A,B 아닌 경우
        elif crew.end_time >= work_obj.end_time and work_obj.work_class == '입장' and crew.work_class != '퇴장' and crew.rest_state is False:
            if odd_or_even == crew_odd_or_even and crew.working < max_enter_num and calc_minute <= threshold and crew.enter_count < avg_enter_num:
                if work_start_time <= crew.rest_time and crew.rest_time >= work_obj.end_time:
                    enable_crew_list.append(crew)
                elif work_start_time >= crew.rest_time and work_start_time >= crew.rest_end_time:
                    enable_crew_list.append(crew)

    if len(enable_crew_list) == 0:
        return 0
    else:
        # 가능한 크루는 한명만 있을 수 밖에 없다
        return enable_crew_list[0]


def searching_working_num(working_crew_list, work_class, work_start_time, work_end_time, avg_num):
    # 일을 하지않고 있는 크루 리스트 뽑기
    none_working_list = []
    for crew in working_crew_list:
        if crew.working == 0:
            none_working_list.append(crew)

    # 모두 일하고 있을 경우 return 0
    if len(none_working_list) == 0:
        return 0

    enable_crew_list = []
    # 일을 하지않고 있는 크루 중 입/퇴장에 따라 평균횟수 안넘은, 일 종료시간 > 퇴근시간 크루 리스트 뽑기
    for crew in none_working_list:
        if crew.end_time >= work_end_time and work_class == '입장' and crew.enter_count < avg_num and crew.rest_state is False:
            if work_start_time <= crew.rest_time and crew.rest_time >= work_end_time:
                enable_crew_list.append(crew)
            elif work_start_time >= crew.rest_time and work_start_time >= crew.rest_end_time:
                enable_crew_list.append(crew)
        elif crew.end_time >= work_end_time and work_class == '퇴장' and crew.exit_count < avg_num and crew.rest_state is False:
            if work_start_time <= crew.rest_time and crew.rest_time >= work_end_time:
                enable_crew_list.append(crew)
            elif work_start_time >= crew.rest_time and work_start_time >= crew.rest_end_time:
                enable_crew_list.append(crew)

    # 모두 평균 횟수 넘을경우 return 0
    if len(enable_crew_list) == 0:
        return 0
    # 가능한 크루 중 인덱스가 가장낮은 크루 (출근을 가장 빨리한 크루) 리턴
    else:
        return enable_crew_list[0]


def assign_work(work_obj, working_crew_list, threshold, max_enter_num, avg_num):
    work_class = work_obj.work_class  # 입장 or 퇴장
    work_start_time = work_obj.start_time
    work_end_time = work_obj.end_time

    # 스크린 A,B 일인 경우 입퇴장을 하고있는 크루가 있으면 동시작업 가능여부 파악 후 할당
    if work_obj.odd_or_even == 'etc':
        current_list = check_enter_working(work_obj.odd_or_even, working_crew_list)

        # 입퇴장을 받고있는 크루가 있으면 동시작업 가능한지 확인
        if current_list != 0:
            crew = enable_enter_crew(work_obj, current_list, threshold, max_enter_num, avg_num)

            if crew != 0:
                work_obj.assign_work(crew)
                # 크루 상태정보 갱신
                crew.do_enter(work_obj)
                return work_obj, crew

    # 스크린 A,B가 아닌경우/ 입장을 받고있는 크루가 있으면 동시작업 가능여부 파악 후 할당
    if work_class == '입장':
        # 현재 입장받고있는 크루가 있으면 리스트 뽑기
        current_list = check_enter_working(work_obj.odd_or_even, working_crew_list)

        # 입장받고 있는 크루가 있으면 동시 입장받을 수 있는 지 확인
        if current_list != 0:
            crew = enable_enter_crew(work_obj, current_list, threshold, max_enter_num, avg_num)

            if crew != 0:
                work_obj.assign_work(crew)
                # 크루 상태정보 갱신
                crew.do_enter(work_obj)
                return work_obj, crew

        # 입장 받고있는 크루가 없는경우
        crew = searching_working_num(working_crew_list, work_class, work_start_time, work_end_time, avg_num)

        if crew != 0:
            work_obj.assign_work(crew)
            # 크루 상태정보 갱신
            crew.do_enter(work_obj)
            return work_obj, crew
        else:
            # 현재 일 할수 있는 크루가 없는경우
            return 0, 0
    elif work_class == '퇴장':
        crew = searching_working_num(working_crew_list, work_class, work_start_time, work_end_time, avg_num)

        if crew != 0:
            work_obj.assign_work(crew)
            # 크루 상태정보 갱신
            crew.do_exit(work_obj)
            return work_obj, crew
        else:
            # 현재 일 할수 있는 크루가 없는경우
            return 0, 0


def usher_scheduling_algorithm(crew_list, assignment_list, avg_threshold):
    threshold = 20  # 중복입장 경계값
    max_enter_num = 3  # 최대 중복입장 가능 수
    working_crew_list = []  # 출근한 크루 리스트
    tmp_crew_list = crew_list.copy()

    # 평균 입/퇴장 수 계산
    print('평균 입/퇴장 횟수 계산')
    avg_num = calculate_avg_work_num(assignment_list, crew_list)
    avg_num -= avg_threshold  # 평균에서 일정 수 빼기 -> 뒤에 더 배분될 수 있도록
    print('-> OK')

    # 각각의 work에 대해 크루 할당
    print('입/퇴장 할당')
    new_assignment_list = []
    for work in assignment_list:
        # 출근한 크루 리스트 업데이트
        working_crew_list, crew_list = refresh_working_crew_list(work, working_crew_list, crew_list)

        assigned_work, update_crew = assign_work(work, working_crew_list, threshold, max_enter_num, avg_num)

        # 할당된 업무는 리스트에 추가
        if assigned_work != 0:
            new_assignment_list.append(assigned_work)

            # working 크루 리스트 update 된 크루정보로 변경
            for i in range(0, len(working_crew_list)):
                if working_crew_list[i].idx == update_crew.idx:
                    working_crew_list[i] = update_crew

                # 임시저장 크루 리스트 update -> 나중에 total 횟수 확인 위해
                for j in range(0, len(tmp_crew_list)):
                    if tmp_crew_list[j].idx == update_crew.idx:
                        tmp_crew_list[j] = update_crew

        else:
            work.name = ' '  # 지원은 빈칸으로
            new_assignment_list.append(work)
    print('-> OK')

    return new_assignment_list, tmp_crew_list



