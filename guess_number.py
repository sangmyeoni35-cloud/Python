1 #1. 컴퓨터가 숫자를 생각한다.(1~50)
2 #2. 사용자가 숫자를 말한다.
3 #3. 숫자가 맞으면 사용자 win
4 #4. 틀리면 컴퓨터가 up, down을 알려준다.
5 #5. 2~4번까ㅣ 7번 반복
6 #6.7번 내에 맞추지 못하면 compter win

import random
scret_number = random.randint(1,100)
attempts = 0
while True:
    try:
        user_guess = int(input("숫자 입력: "))
        attempts += 1


        if user_guess < scret_number:
            print("up! 더 큰 숫자입니다.")
        elif user_guess > scret_number:
            print("DOWN! 더 작은 숫자입니다.")
        else:
            print(f"정답입니다.! {attempts}번 만에 맞혔습니다.")
            break
    except ValueError:
        print("올바른 숫자를 입력하세요")

if __name__ == "__main--":
    guess_number_game()
