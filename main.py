import os
from theater_scheduling import make_scheduling_file
from usher_scheduling import make_usher_scheduling_file

# Start massage
print("*** Program Start ***\n")
run = True

while run:
    print("===== 리스트 ======\n\n"
          " 1.영화 스케줄링\n"
          " 2.크루 스케줄링\n"
          " 3.프로그램 종료\n\n"
          "==================")
    print("> 실행할 번호를 입력해 주세요: ")
    menu = input()

    if menu == '1':
        success1 = make_scheduling_file()

        if success1:
            print("> 영화 스케줄링 파일이 생성되었습니다(Press Enter Key)")
            input()
            os.system('cls')
        else:
            print("> 파일 생성 오류 (Press Enter Key)")
            input()
            os.system('cls')

    elif menu == '2':
        success2, crew_list = make_usher_scheduling_file()

        if success2:
            print("\n\n ######## 크루 입/퇴장 수 ####### \n")
            for crew in crew_list:
                enter, exit_num = crew.total_review()
                print(crew.name + ' 입장: ' + str(enter) + ' 퇴장: ' + str(exit_num))
            print('###############################\n')
            print("> 어셔반영스케줄 파일이 생성되었습니다(Press Enter Key)")
            input()
            os.system('cls')
        else:
            print("> 파일 생성 오류 (Press Enter Key)")
            input()
            os.system('cls')
    elif menu == '3':
        print("> 프로그램을 종료합니다(Press Enter Key)")
        input()
        run = False
    else:
        print("> 없는 번호입니다. 다시 입력해 주세요.(Press Enter Key)")
        input()
        os.system('cls')

