class Crew:
    def __init__(self, name, start_time, end_time, idx):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.idx = idx
        self.working = False
        self.enter_count = 0
        self.exit_count = 0

    def do_enter(self):
        self.enter_count += 1
        self.working = True
        return self.enter_count

    def do_exit(self):
        self.exit_count += 1
        self.working = True
        return self.exit_count

    def working_done(self):
        self.working = False

    def total_review(self):
        return self.enter_count, self.exit_count


'''
 입장시간은 10분전, 10분후까지
 퇴장시간은 영화끝나기 5분전 ~ 영화끝난후 관마다 정해진 청소시간까지
'''
class Assignment:
    def __init__(self, movie_name, theater_num, work_class, time, err_time_list, cleaning_term_dict):
        self.movie_name = movie_name  # 영화이름
        self.theater_num = theater_num  # 영화관 번호
        self.work_class = work_class  # 입장 or 퇴장
        self.start_time = 0
        self.end_time = 0

        if work_class == '입장':
            # 입장 시간
            self.start_time = time - 10
            if self.start_time % 100 > 60:  # -10분해서 시간이 바뀌는경우
                self.start_time = self.start_time - 40
                if self.start_time < 100:  # 새벽 1시에서 -10분 = 24시로 되는경우
                    self.start_time += 2400

            # 입장 마감 시간
            self.end_time = time + 10
            if self.start_time % 100 >= 60:  # +10분해서 시간이 바뀌는경우
                self.start_time = self.start_time + 40
                if self.start_time >= 2500:  # 24시에서 +10 = 새벽 1시로 되는경우
                    self.start_time -= 2400

        elif work_class == '퇴장':
            # 퇴장 시작시간
            self.start_time = time - 5  # 미리 퇴장 5분전에
            if self.start_time % 100 > 60:  # -5분해서 시간이 바뀌는경우
                self.start_time = self.start_time - 40
                if self.start_time < 100:  # 새벽 1시에서 -5분 = 24시로 되는경우
                    self.start_time += 2400

            # 반불시간 리스트에서 반불시간 가져오기
            err_time = 0
            for i in range(0, len(err_time_list)):
                flag = 0
                if self.movie_name == err_time_list[i][0]:
                    err_time = err_time_list[i][1]
                    flag = 1
                # 반불시간이 없는 경우 알림
                if i == len(err_time_list) - 1 and flag == 0:
                    print(self.movie_name + '의 반불시간이 없습니다!')

            # 퇴장 마감시간
            self.end_time = time + cleaning_term_dict[self.theater_num] + err_time
            if self.start_time % 100 >= 60:  # +해서 시간이 바뀌는경우
                self.start_time = self.start_time + 40
                if self.start_time >= 2500:  # 24시에서 + = 새벽 1시로 되는경우
                    self.start_time -= 2400

        self.name = None  # 담당어셔 이름

    def assign_work(self, crew_object):
        self.name = crew_object.name


