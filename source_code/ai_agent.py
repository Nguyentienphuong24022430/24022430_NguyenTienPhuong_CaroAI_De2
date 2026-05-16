# ai_agent.py
import math
from config import WIN_COUNT, EMPTY, PLAYER_X, AI_O, BOARD_SIZE
from game_logic import check_win, get_valid_moves, is_board_full

def evaluate_line(line, player):
    """Hàm Heuristic chấm điểm cho một đoạn gồm 4 ô liên tiếp"""
    opponent = PLAYER_X if player == AI_O else AI_O
    p_count = line.count(player)
    e_count = line.count(EMPTY)
    o_count = line.count(opponent)
    
    if p_count == 4: return 100000        # Chuỗi 4 quân: Thắng tuyệt đối
    if p_count == 2 and e_count == 2:     
        return 200
    if o_count == 3 and e_count == 1:     # Địch có 3 quân: Phạt cực nặng
        return -50000                      
    if o_count == 2 and e_count == 2:     # Địch mới có 2 quân thoáng: Phạt mạnh để ép AI chặn ngay!
        return -3000
    return 0

def evaluate_board(board):
    """Đánh giá tổng thể bàn cờ dưới góc nhìn của AI (MAX)"""
    score = 0
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            # Hàng ngang
            if c <= BOARD_SIZE - WIN_COUNT:
                line = [board[r][c+i] for i in range(WIN_COUNT)]
                score += evaluate_line(line, AI_O) - evaluate_line(line, PLAYER_X)
            # Hàng dọc
            if r <= BOARD_SIZE - WIN_COUNT:
                line = [board[r+i][c] for i in range(WIN_COUNT)]
                score += evaluate_line(line, AI_O) - evaluate_line(line, PLAYER_X)
            # Chéo xuôi
            if r <= BOARD_SIZE - WIN_COUNT and c <= BOARD_SIZE - WIN_COUNT:
                line = [board[r+i][c+i] for i in range(WIN_COUNT)]
                score += evaluate_line(line, AI_O) - evaluate_line(line, PLAYER_X)
            # Chéo ngược
            if r <= BOARD_SIZE - WIN_COUNT and c >= WIN_COUNT - 1:
                line = [board[r+i][c-i] for i in range(WIN_COUNT)]
                score += evaluate_line(line, AI_O) - evaluate_line(line, PLAYER_X)
    return score

class CaroAI:
    def __init__(self):
        self.state_count = 0  # Đếm số trạng thái đã xét phục vụ Level 3

    def minimax(self, board, depth, is_max):
        self.state_count += 1
        
        if check_win(board, AI_O): return 1000000 + depth, None
        if check_win(board, PLAYER_X): return -1000000 - depth, None
        if is_board_full(board) or depth == 0:
            return evaluate_board(board), None

        moves = get_valid_moves(board)
        best_move = None

        if is_max:
            best_score = -math.inf
            for move in moves:
                r, c = move
                board[r][c] = AI_O
                score, _ = self.minimax(board, depth - 1, False)
                board[r][c] = EMPTY  # Hoàn tác
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move
        else:
            best_score = math.inf
            for move in moves:
                r, c = move
                board[r][c] = PLAYER_X
                score, _ = self.minimax(board, depth - 1, True)
                board[r][c] = EMPTY
                if score < best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move

    def alpha_beta(self, board, depth, alpha, beta, is_max):
        self.state_count += 1
        
        if check_win(board, AI_O): return 1000000 + depth, None
        if check_win(board, PLAYER_X): return -1000000 - depth, None
        if is_board_full(board) or depth == 0:
            return evaluate_board(board), None

        moves = get_valid_moves(board)
        best_move = None

        if is_max:
            best_score = -math.inf
            for move in moves:
                r, c = move
                board[r][c] = AI_O
                score, _ = self.alpha_beta(board, depth - 1, alpha, beta, False)
                board[r][c] = EMPTY
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # Cắt nhánh MIN
            return best_score, best_move
        else:
            best_score = math.inf
            for move in moves:
                r, c = move
                board[r][c] = PLAYER_X
                score, _ = self.alpha_beta(board, depth - 1, alpha, beta, True)
                board[r][c] = EMPTY
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # Cắt nhánh MAX
            return best_score, best_move