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


class Assignment:
    def __init__(self, movie_name, theater_num, work_class, time, theater_cleaning_term=None):
        self.movie_name = movie_name  # 영화이름
        self.theater_num = theater_num  # 영화관 번호
        self.work_class = work_class  # 입장 or 퇴장
        self.start_time = 0
        self.end_time = 0

        if work_class == '입장':
            self.start_time = time - 10  # 입장 시간
            self.end_time = time + 10  # 입장 마감 시간
        elif work_class == '퇴장':
            self.start_time = time
            self.end_time = time + theater_cleaning_term

        self.name = None  # 담당어셔 이름

    def assign_work(self, crew_object):
        self.name = crew_object.name


