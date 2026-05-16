# game_logic.py
from config import BOARD_SIZE, WIN_COUNT, EMPTY, PLAYER_X, AI_O

def create_board():
    """Khởi tạo bàn cờ trống"""
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def print_board(board):
    """Hiển thị bàn cờ ra màn hình Console"""
    print("\n   " + " ".join(str(i) for i in range(BOARD_SIZE)))
    for r in range(BOARD_SIZE):
        print(f"{r}  " + " ".join(board[r][c] for c in range(BOARD_SIZE)))
    print()

def is_board_full(board):
    """Kiểm tra bàn cờ đầy (Hòa cờ)"""
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == EMPTY:
                return False
    return True

def check_win(board, player):
    """Kiểm tra điều kiện kết thúc: 4 quân liên tiếp theo 4 hướng"""
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Ngang, Dọc, Chéo xuôi, Chéo ngược
    
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] != player:
                continue
            for dr, dc in directions:
                count = 1
                for i in range(1, WIN_COUNT):
                    nr, nc = r + dr * i, c + dc * i
                    if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == player:
                        count += 1
                    else:
                        break
                if count == WIN_COUNT:
                    return True
    return False

def get_valid_moves(board):
    """
    Tối ưu nâng cao: Chỉ sinh các nước đi nằm trong bán kính 2 ô lân cận 
    xung quanh các quân cờ đã đánh để thu hẹp không gian tìm kiếm, tránh treo máy.
    """
    moves = []
    has_pieces = False
    
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] != EMPTY:
                has_pieces = True
                for dr in range(-2, 3):
                    for dc in range(-2, 3):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                            if board[nr][nc] == EMPTY and (nr, nc) not in moves:
                                moves.append((nr, nc))
                                
    # Nếu đầu ván (bàn cờ trống), ưu tiên chọn ô chính giữa bàn cờ
    if not has_pieces:
        return [(BOARD_SIZE // 2, BOARD_SIZE // 2)]
        
    return moves