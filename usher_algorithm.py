'''
  입장, 퇴장의 평균을 구하여 균등하게 분배,
  남는 work는 지원으로 채우기
  짝수, 홀수 관에 따라 입장시간이 겹치는 경우 threshold를 설정하여 동시 work 할당
  크루인덱스는 0부터


  ** 필요변수 **
  threshold -> 같은 홀수 혹은 짝수관 입장을 받을때 threshold 아래인 경우 일 중복할당 가능 (최대 3개 관)
  max_enter_num -> 최대 동시 입장받는 관 수
  working_crew_list -> 일하고 있는 크루들을 담아두는 리스트 크루 object 저장

  ** 필요함수 **
  refresh_working_crew_list -> 현재 할당을 기다리는 work 시간 기준으로 크루 출근, 크루 퇴근
  searching_working_num -> 일 횟수 searching 후 가장 적당한 크루 return
  check_can_enter -> 동시에 입장받을 수 있는지 확인하는 함수
  assign_working -> 실행과 동시에 refresh, 일횟수 searching, 동시에 입장받을 수 있는지 check(평균 입장수 넘어가면 pass), 적당한 크루에게 일 할당

'''


# working_crew_list 로 넘어간 object는 crew_list에서 제거
def refresh_working_crew_list(work_obj, working_crew_list, crew_list):
    current_time = work_obj.start_time

    # 새벽 1시에서 5시 사이인경우 2500~2900으로 시간을 바꿔서 계산 편리하도록
    if 100 <= current_time < 500:
        current_time += 2400

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

    return new_working_crew_list, new_crew_list






def usher_scheduling_algorithm(crew_list, assignment_list):
    threshold = 5
    max_enter_num = 3
    working_crew_list = []

    odd_or_even_dict = {
        '돌비시네마관': 'odd',
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

