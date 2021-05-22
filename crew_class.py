class Crew:
    def __init__(self, name, start_time, end_time, idx):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.idx = idx
        self.enter_count = 0
        self.exit_count = 0


    def do_enter(self):
        self.enter_count += 1
        return self.enter_count

    def do_exit(self):
        self.exit_count += 1
        return self.exit_count

    def total_review(self):
        return self.enter_count, self.exit_count
