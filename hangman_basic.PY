import random

# 1. 자료구조 및 초기화
word_list = ['apple', 'banana', 'man']
limit_error = 7
num_error = 0

# 2. com이 단어 선택 및 초기 빈칸 설정
target_word = random.choice(word_list) # 무작위 선택으로 변경
blank_char = '_'
# word_screen을 리스트로 만들어야 수정이 쉽습니다.
word_screen = [blank_char] * len(target_word) 

print("--- 행맨 게임을 시작합니다! ---")

# 3. 게임 루프
while num_error < limit_error:
    # 현재 진행 상태 보여주기
    print(f"\n현재 단어: {' '.join(word_screen)}")
    
    # 사용자 알파벳 입력
    user_input = input("알파벳 입력: ").lower()

    # 4. 게임 상태 업데이트 (Update Game)
    if target_word.find(user_input) == -1:
        # 단어에 알파벳이 없는 경우
        num_error += 1
        print(f'오답입니다! (현재 오답 횟수: {num_error}/{limit_error})')
    else:
        # 알파벳이 단어에 있는 경우: 모든 위치를 찾아 채워주기
        for i in range(len(target_word)):
            if target_word[i] == user_input: # 인덱스 i를 사용하여 비교
                word_screen[i] = user_input  # 해당 위치의 빈칸을 입력한 글자로 교체

    # 5. 승리 조건 판별 (빈칸이 없으면 승리)
    if word_screen.count(blank_char) == 0:
        print(f"\n축하합니다! 정답: {target_word}")
        print('YOU WIN!')
        break

# 6. 패배 조건 판별 (반복문 종료 후 오답 횟수 확인)
if num_error >= limit_error:
    print(f'\nYOU LOSE... 정답은: {target_word}였습니다.')