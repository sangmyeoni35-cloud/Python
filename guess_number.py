import random
def Number(limit):
    return random.randint(1, limit)

def UpDown(computer, human, a):
    if a != 0:
        if computer > human:
            return print("Up!",end=" ")
        else:
            return print("Down!",end=" ")

limit = int(input(">> 범위 : "))
ttry = int(input(">> 기회 : "))

computer = Number(limit)

while ttry != 0:
    human = int(input(">> 숫자를 입력하세요 : "))
    ttry -= 1
    
    if computer == human:
        print("정답입니다!")
        break
    else:
        UpDown(computer, human, ttry)
        if ttry != 0:
            print("남은 기회 : ", ttry)
else: print("X! 정답 : ",computer)
