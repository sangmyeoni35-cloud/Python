# 데이터
board_screen = ' 0 | 1 | 2\n 3 | 4 | 5\n 6 | 7 | 8' # 화면에 보여주는 보드판
board_blank = {0,1,2,3,4,5,6,7,8} # 컴퓨터가 뽑을 것들
board = [" "] * 9 # 실제 계산되는 보드판
win_status = [(0,1,2), (3,4,5), (6,7,8), # 누군가 이기는 경우
              (0,3,6), (1,4,7), (2,5,8),
              (0,4,8), (2,4,6)]
human = 'O' # 사람
computer = 'X' # 컴퓨터

# 함수
def showBoard(): # 현재 보드의 상태를 화면에 보여줌
    print(board_screen) # 보드 출력

def updateGame(who, number): # 보드에 플레이어에 따라 해당하는 칸에 문자를 입력함
    global board, board_screen # 실제 데이터(전역 변수)를 바꿀것임
    board[number] = who # 실제 보드판의 입력받은 칸에 플레이어에 대응하는 문자 저장
    board_screen = board_screen.replace(str(number), who) # 화면 보드판의 입력받은 칸을 플레이어 문자로 바꿈
    board_blank.discard(number) # 컴퓨터가 뽑을 것들 중 누군가 칠한 칸은 삭제
    # 전역 변수 선언은 메서드를 사용할 경우엔 하지 않아도 됨

import random # random 사용할것임
def getComputerNumber(): # 컴퓨터가 칠할 칸을 정함
    if board_blank: # 컴퓨터가 뽑을 것이 남아있다면
        return random.choice(list(board_blank)) # 그 중 랜덤으로 하나 선택, 
    return -1 # 없다면 -1

def isWin(turn): # 누구 차례인지 입력받고 그 플레이어가 이겼는지 확인
    for status in win_status: # 이길 경우의 튜플 하나씩 가져와서 확인
        if board[status[0]] == board[status[1]] == board[status[2]] == turn:
            return True # 가져온 튜플의 칸 하나씩 보드의 칸과 일치하는지 확인
    return False

# 3. 메인 로직
# 3-1. 필요한 자료구조 초기화
print('=============== Tic-Tac-Toe ===============')
# 3-2. 보드를 보여줌
showBoard()
while True:
    # 3-3. human 차례
    # human 입력 받아서 처리
    human_input = int(input('>> 숫자를 입력하세요 : '))
    updateGame(human, human_input)
    showBoard()

    if isWin(human):
        print('You Win ~~~~~~~ !!!')
        break

    # 3-4. 컴퓨터 차례
    # computer 가 놓을 자리를 선택
    computer_input = getComputerNumber()
    if computer_input == -1:
        print('The gamed ended in a tie ~~~~~~~ !!!')
        break
    updateGame(computer, computer_input)
    print(">> 컴퓨터의 선택 : ", computer_input)
    showBoard()
    if isWin(computer):
        print('You loose ~~~~~~~ !!!')
        break
