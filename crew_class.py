class Crew:
    def __init__(self, name, start_time, end_time, rest_time, idx):
        self.name = name  # 크루 이름
        self.start_time = int(start_time)  # 출근시간
        self.end_time = int(end_time)  # 퇴근시간
        self.rest_time = int(rest_time)  # 휴게시간

        tmp = rest_time + 30 + 2

        if tmp % 100 >= 60:  # +32분해서 시간이 바뀌는경우
            tmp = tmp + 40
            if tmp >= 2500:  # 24시에서 +32 = 새벽 1시로 되는경우
                tmp -= 2400

        self.rest_end_time = tmp  # 휴식시간 30분 + 이동시간 2분
        self.rest_state = False

        self.idx = idx  # 고유 번호
        self.working = 0  # 현재 수행하고있는 일 수
        self.enter_count = 0  # 입장 처리 수
        self.exit_count = 0  # 퇴장 처리 수
        self.work_start_time = 0  # 입/퇴장 시작 시간
        self.work_end_time = 0  # 입/퇴장 종료 시간
        self.work_class = ''
        self.work_info = ''  # 일하는 관이 짝수? 홀수?

    def do_enter(self, work_obj):
        self.enter_count += 1
        self.working += 1
        self.work_class = '입장'
        self.work_start_time = work_obj.start_time
        self.work_end_time = work_obj.end_time
        self.work_info = work_obj.odd_or_even

    def do_exit(self, work_obj):
        self.exit_count += 1
        self.working += 1
        self.work_class = '퇴장'
        self.work_start_time = work_obj.start_time
        self.work_end_time = work_obj.end_time
        self.work_info = work_obj.odd_or_even

    def working_done(self):
        self.working = 0
        self.work_start_time = 0
        self.work_end_time = 0
        self.work_class = ''
        self.work_info = ''

    def total_review(self):
        return self.enter_count, self.exit_count


'''
 입장시간은 10분전, 10분후까지
 퇴장시간은 영화끝나기 5분전 ~ 영화끝난후 관마다 정해진 청소시간까지
'''
class Assignment:
    def __init__(self, movie_name, theater_num, work_class, time, err_time_list, cleaning_term_dict, odd_or_even):
        self.movie_name = movie_name  # 영화이름
        self.theater_num = theater_num  # 영화관 번호
        self.work_class = work_class  # 입장 or 퇴장
        self.start_time = 0
        self.end_time = 0
        self.odd_or_even = odd_or_even

        if work_class == '입장':
            # 입장 시간
            self.start_time = time - 10
            if self.start_time % 100 > 60:  # -10분해서 시간이 바뀌는경우
                self.start_time = self.start_time - 40
                if self.start_time < 100:  # 새벽 1시에서 -10분 = 24시로 되는경우
                    self.start_time += 2400

            # 입장 마감 시간
            self.end_time = time + 10 + 5  # 5는 온도체크 시간
            if self.end_time % 100 >= 60:  # +15분해서 시간이 바뀌는경우
                self.end_time = self.end_time + 40
                if self.end_time >= 2500:  # 24시에서 +10 = 새벽 1시로 되는경우
                    self.end_time -= 2400

        elif work_class == '퇴장':
            # 퇴장 시작시간
            self.start_time = time - 5  # 미리 퇴장 5분전에
            if self.start_time % 100 > 60:  # -5분해서 시간이 바뀌는경우
                self.start_time = self.start_time - 40
                if self.start_time < 100:  # 새벽 1시에서 -5분 = 24시로 되는경우
                    self.start_time += 2400

            # 반불시간 리스트에서 반불시간 가져오기
            err_time = 0
            flag = 0
            for i in range(0, len(err_time_list)):
                if self.movie_name == err_time_list[i][0]:
                    err_time = err_time_list[i][1]
                    flag = 1
                # 반불시간이 없는 경우 알림
                if i == len(err_time_list) - 1 and flag == 0:
                    print(self.movie_name + '의 반불시간이 없습니다!')

            # 퇴장 마감시간
            self.end_time = time + cleaning_term_dict[self.theater_num] + err_time
            if self.end_time % 100 >= 60:  # +해서 시간이 바뀌는경우
                self.end_time = self.end_time + 40
                if self.end_time >= 2500:  # 24시에서 + = 새벽 1시로 되는경우
                    self.end_time -= 2400

        self.name = None  # 담당어셔 이름

    def assign_work(self, crew_object):
        self.name = crew_object.name


