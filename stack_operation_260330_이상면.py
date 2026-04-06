stack =[]
capacity = 5
def isFull():
    if len(stack) == capacity:
        return True
    else:
        return False

def isEmty():
    if len(stack) == 0:
        return True
    else:
        return False

def push(data):
    if isFull():
        print('stack이 차 있어서 더 이상 추가할 수 없습니다.')
    else:
        stack.append(data) 

def pop():
    if isEmty():
        print()
        return -1
    else:
        return stack.pop()

def peek():
    if isEmty():
        print()
        return -1
    else:
        return stack[-1]
print('================================================================')
print(f'[정수형 스택 연산 실습(용량:{capacity})]') 
print('1.push 2.pop 3.peek 0.exit')  
print('================================================================')

while True:
    menu = int(input('> 메뉴선택:'))
    if menu == 0:
        break
    elif menu == 1:
        data = int(input('[Push] 데이터 입력'))
        push(data)
    elif menu == 2:
        data = pop()
        print('[Pop] 가져온 데이터 :',data)
    elif menu == 3:
        data = peek()
        print('top 데이터 확인:', data) 
    print('> 현재 스택 상태', stack)
print('[[정수형 스택 연산 실습 종료]]')   

    
