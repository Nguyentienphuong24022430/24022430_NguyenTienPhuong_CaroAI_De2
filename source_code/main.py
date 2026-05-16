# main.py
import time
from config import PLAYER_X, AI_O, EMPTY, BOARD_SIZE
from game_logic import print_board, create_board, check_win, is_board_full
from ai_agent import CaroAI

def main():
    board = create_board()
    print("=== CHƯƠNG TRÌNH CỜ CARO AI ===")
    print("Chọn thuật toán AI:\n1. Minimax gốc (Level 1)\n2. Alpha-Beta Pruning (Level 2)")
    choice = input("Nhập lựa chọn (1 hoặc 2): ").strip()
    ai_mode = "alpha_beta" if choice == "2" else "minimax"
    
    depth_limit = int(input("Nhập độ sâu tìm kiếm (Khuyên dùng: 2 hoặc 3): ").strip())
    ai = CaroAI()

    print("\n--- BẮT ĐẦU VÁN ĐẤU ---")
    print_board(board)

    while True:
        # ================= LƯỢT NGƯỜI CHƠI (X) =================
        while True:
            try:
                move_str = input("Lượt của bạn (Nhập dạng: 'dòng cột', VD: 4 4): ")
                r, c = map(int, move_str.split())
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == EMPTY:
                    board[r][c] = PLAYER_X
                    break
                print("Vị trí không hợp lệ hoặc đã có quân cờ! Thử lại.")
            except ValueError:
                print("Vui lòng nhập đúng định dạng 2 số cách nhau bằng khoảng trắng.")

        print_board(board)
        if check_win(board, PLAYER_X):
            print("Chúc mừng! Bạn đã thắng cuộc (X)!")
            break
        if is_board_full(board):
            print("Kết quả: Hòa cờ! Bàn cờ đã đầy."); break

        # ================= LƯỢT MÁY TÍNH (O) =================
        print(f"AI [{ai_mode.upper()}] đang suy nghĩ...")
        ai.state_count = 0
        start = time.time()

        if ai_mode == "minimax":
            score, best_move = ai.minimax(board, depth_limit, True)
        else:
            score, best_move = ai.alpha_beta(board, depth_limit, float('-inf'), float('inf'), True)

        runtime = (time.time() - start) * 1000  # Quy đổi sang miligiây (ms)

        if best_move:
            board[best_move[0]][best_move[1]] = AI_O
            print(f"-> AI quyết định đánh vào ô: {best_move}")
            # Xuất log thông số thực nghiệm đầy đủ theo yêu cầu chức năng
            print(f"   [LOG]: Điểm đánh giá: {score} | Trạng thái đã xét: {ai.state_count} | Thời gian: {runtime:.2f} ms")
        
        print_board(board)
        if check_win(board, AI_O):
            print("AI (O) đã thắng cuộc! Hẹn gặp lại ván sau.")
            break
        if is_board_full(board):
            print("Kết quả: Hòa cờ! Bàn cờ đã đầy."); break

if __name__ == "__main__":
    main()