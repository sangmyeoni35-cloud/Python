import random

# 자료 구조
word_list = ['APPLE', 'BANANA', 'MAN', 'WOMAN', 'TOMATO']
limit_error = 7

def select_word():
    word_list = ['APPLE', 'BANANA', 'MAN']
    return random.choice(word_list)

def UserError(user_input):
    global user_error
    global num_error
    user_error = user_error + user_input
    if user_error.count(user_input) > 1:
        if user_error.count(user_input) > 2:
            num_error += 1
            print(f'오답 : {num_error}회')
            return False
        print(f"{user_input} >> 이미 확인한 알파벳입니다.")
        return False
    else:
        return True

# 게임 로직
# 1. Com이 단어 선택하여 보여주기
target_word = select_word()
# print(">> 컴퓨터가 생각한 단어 : ", target_word)

blank_char = '_'
word_screen = blank_char * len(target_word) # 몇 글자인지 알려주기

num_error = 0
user_error = ""
while num_error < limit_error:
    # 2. 사용자 알파벳 입력
    user_input = input(">> 알파벳 입력 : ").upper() 
    if UserError(user_input):
        # 3. 게임 상태 업데이트
        if target_word.find(user_input) == -1: # 없으면 오류 횟수 증가
            num_error += 1
            print(f'오답 : {num_error}회')
        else: # 알파벳이 단어에 있으면 채워주기
            for i in range(len(target_word)):
                if target_word[i] == user_input:
                    word_screen = word_screen[:i] + user_input + word_screen[i+1:]
            print('정답 : ', word_screen)
                # 4. 단어를 다 맞췄으면(word_screen에 _ 가 없으면) 사용자 win
            if word_screen.count(blank_char) == 0:
                print('You win ~~~~ !!!')
                break
else: print('You loose ... : ', target_word)
# 5. 시도회수가 7번이 넘었으면 loose    
