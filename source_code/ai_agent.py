import math
from config import WIN_COUNT, EMPTY, PLAYER_X, AI_O, BOARD_SIZE
from game_logic import check_win, get_valid_moves, is_board_full

def evaluate_line(line):
    """
    Hàm Heuristic quy ước: Chấm điểm trực tiếp cho AI (MAX).
    Trả về điểm dương nếu lợi thế thuộc về AI_O.
    Trả về điểm âm nếu lợi thế thuộc về PLAYER_X.
    """
    ai_count = line.count(AI_O)
    player_count = line.count(PLAYER_X)
    empty_count = line.count(EMPTY)
    
    if ai_count == 4: 
        return 100000              
    if ai_count == 3 and empty_count == 1: 
        return 5000                
    if ai_count == 2 and empty_count == 2: 
        return 200                 

    if player_count == 4: 
        return -100000            
    if player_count == 3 and empty_count == 1: 
        return -50000              
    if player_count == 2 and empty_count == 2: 
        return -3000              

    return 0

def evaluate_board(board):
    """Đánh giá tổng thể bàn cờ theo các cửa sổ kích thước WIN_COUNT"""
    score = 0
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if c <= BOARD_SIZE - WIN_COUNT:
                line = [board[r][c+i] for i in range(WIN_COUNT)]
                score += evaluate_line(line)
            if r <= BOARD_SIZE - WIN_COUNT:
                line = [board[r+i][c] for i in range(WIN_COUNT)]
                score += evaluate_line(line)
            if r <= BOARD_SIZE - WIN_COUNT and c <= BOARD_SIZE - WIN_COUNT:
                line = [board[r+i][c+i] for i in range(WIN_COUNT)]
                score += evaluate_line(line)
            if r <= BOARD_SIZE - WIN_COUNT and c >= WIN_COUNT - 1:
                line = [board[r+i][c-i] for i in range(WIN_COUNT)]
                score += evaluate_line(line)
    return score

class CaroAI:
    def __init__(self):
        self.state_count = 0 

    def minimax(self, board, depth, is_max):
        self.state_count += 1
        
        if check_win(board, AI_O): return 1000000 + depth, None
        if check_win(board, PLAYER_X): return -1000000 - depth, None
        if is_board_full(board) or depth == 0:
            return evaluate_board(board), None

        moves = get_valid_moves(board)
        
        center = BOARD_SIZE // 2
        moves.sort(key=lambda m: abs(m[0] - center) + abs(m[1] - center))

        if is_max:
            best_score = -math.inf
            for move in moves:
                r, c = move
                board[r][c] = AI_O
                score, _ = self.minimax(board, depth - 1, False)
                board[r][c] = EMPTY  
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
                    break  
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
                    break  
            return best_score, best_move