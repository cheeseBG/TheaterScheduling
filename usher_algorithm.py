'''
  입장, 퇴장의 평균을 구하여 균등하게 분배,
  남는 work는 지원으로 채우기
  짝수, 홀수 관에 따라 입장시간이 겹치는 경우 threshold를 설정하여 동시 work 할당
'''


def usher_scheduling_algorithm(crew_list, assignment_list):
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