def print_board(board):
    """보드 상태 출력"""
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board):
    """승리 조건 확인"""
    # 가로, 세로 확인
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i]
    
    # 대각선 확인
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    
    return None

def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    
    print("--- 틱택토 게임을 시작합니다! ---")
    
    for turn in range(9):
        print_board(board)
        print(f"플레이어 {current_player}의 차례입니다.")
        
        try:
            row, col = map(int, input("행과 열을 입력하세요 (0, 1, 2 중 선택, 예: 0 1): ").split())
            
            if board[row][col] != " ":
                print("이미 차 있는 칸입니다. 다시 선택하세요.")
                continue
        except (ValueError, IndexError):
            print("잘못된 입력입니다. 0~2 사이의 숫자 두 개를 입력하세요.")
            continue

        board[row][col] = current_player
        
        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"축하합니다! 플레이어 {winner}가 승리했습니다!")
            return

        current_player = "O" if current_player == "X" else "X"
    
    print_board(board)
    print("무승부입니다!")

if __name__ == "__main__":
    play_game()