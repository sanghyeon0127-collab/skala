def main():
    while True:
        user_input = input("문장을 입력하세요 (종료하려면 !quit 입력): ")
        if user_input == "!quit":
            print("프로그램을 종료합니다.")
            break
        print("입력하신 문장은 다음과 같습니다:")
        print(user_input)


if __name__ == "__main__":
    main()
