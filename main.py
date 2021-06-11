import os
from theater_scheduling import make_scheduling_file

# Start massage
print("*** Program Start ***\n")
run = True

while run:
    print("===== 리스트 ======\n\n"
          " 1.영화 스케줄링\n"
          " 2.크루 리스트\n"
          " 3.크루 추가\n"
          " 4.크루 제거\n"
          " 5.크루 스케줄링\n"
          " 6.프로그램 종료\n\n"
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
        print("커밍순!")
        input()
        os.system('cls')
    elif menu == '3':
        print("커밍순!")
        input()
        os.system('cls')
    elif menu == '4':
        print("커밍순!")
        input()
        os.system('cls')
    elif menu == '5':
        print("커밍순!")
        input()
        os.system('cls')
    elif menu == '6':
        print("> 프로그램을 종료합니다(Press Enter Key)")
        input()
        run = False
    else:
        print("> 없는 번호입니다. 다시 입력해 주세요.(Press Enter Key)")
        input()
        os.system('cls')

