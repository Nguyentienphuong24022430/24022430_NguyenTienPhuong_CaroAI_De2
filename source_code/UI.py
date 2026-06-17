import tkinter as tk
from tkinter import messagebox, ttk
import time

# Import các cấu hình và logic từ thư mục source_code
from config import PLAYER_X, AI_O, EMPTY, BOARD_SIZE
from game_logic import check_win, is_board_full, create_board
from ai_agent import CaroAI

class CaroGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CHƯƠNG TRÌNH CỜ CARO AI - NGUYỄN TIẾN PHƯƠNG")
        
        # Khởi tạo ma trận bàn cờ và AI
        self.board = create_board()
        self.ai = CaroAI()
        
        # Cấu hình mặc định
        self.ai_mode = "alpha_beta"
        self.depth_limit = 2
        self.first_turn = "Người (X)"  # Mặc định người đi trước
        
        # Thiết lập giao diện
        self.setup_menu()
        self.setup_board_ui()
        
    def setup_menu(self):
        """Tạo thanh điều khiển cấu hình thuật toán, độ sâu và lượt đi trước"""
        # Sử dụng ttk.Frame để không bị lỗi thuộc tính padding
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        # 1. Chọn thuật toán
        tk.Label(control_frame, text="Thuật toán:").grid(row=0, column=0, padx=5, sticky="w")
        self.mode_var = tk.StringVar(value="Alpha-Beta Pruning")
        mode_cb = ttk.Combobox(control_frame, textvariable=self.mode_var, 
                               values=["Minimax gốc", "Alpha-Beta Pruning"], 
                               state="readonly", width=18)
        mode_cb.grid(row=0, column=1, padx=5)
        mode_cb.bind("<<ComboboxSelected>>", self.change_config)
        
        # 2. Chọn độ sâu
        tk.Label(control_frame, text="Độ sâu (Depth):").grid(row=0, column=2, padx=5, sticky="w")
        self.depth_var = tk.IntVar(value=2)
        depth_cb = ttk.Combobox(control_frame, textvariable=self.depth_var, 
                                values=[1, 2, 3], 
                                state="readonly", width=5)
        depth_cb.grid(row=0, column=3, padx=5)
        depth_cb.bind("<<ComboboxSelected>>", self.change_config)
        
        # 3. CHỌN AI HAY NGƯỜI ĐI TRƯỚC (Tính năng mới thêm)
        tk.Label(control_frame, text="Đi trước:").grid(row=0, column=4, padx=5, sticky="w")
        self.turn_var = tk.StringVar(value="Người (X)")
        self.turn_cb = ttk.Combobox(control_frame, textvariable=self.turn_var, 
                               values=["Người (X)", "Máy (O)"], 
                               state="readonly", width=10)
        self.turn_cb.grid(row=0, column=5, padx=5)
        self.turn_cb.bind("<<ComboboxSelected>>", self.change_config)
        
        # 4. Nút bấm Reset ván mới
        reset_btn = ttk.Button(control_frame, text="Ván Mới", command=self.reset_game)
        reset_btn.grid(row=0, column=6, padx=15)
        
        # Khu vực hiển thị LOG thực nghiệm trực tiếp lên giao diện
        self.log_label = tk.Label(self.root, text="Hệ thống sẵn sàng. Hãy bấm 'Ván Mới' hoặc chọn ô để đánh cờ!", 
                                  fg="blue", font=("Arial", 10, "italic"))
        self.log_label.pack(side=tk.BOTTOM, pady=5)
        
    def setup_board_ui(self):
        """Khởi tạo lưới ma trận các nút bấm đại diện cho bàn cờ 9x9"""
        self.board_frame = ttk.Frame(self.root)
        self.board_frame.pack(padx=10, pady=10)
        
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                btn = tk.Button(self.board_frame, text="", font=("Arial", 14, "bold"), 
                                width=4, height=2, bg="#F0F0F0",
                                command=lambda row=r, col=c: self.player_move(row, col))
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[r][c] = btn
                
    def change_config(self, event=None):
        """Cập nhật các giá trị cấu hình khi người dùng thay đổi trên menu"""
        choice = self.mode_var.get()
        self.ai_mode = "alpha_beta" if choice == "Alpha-Beta Pruning" else "minimax"
        self.depth_limit = int(self.depth_var.get())
        self.first_turn = self.turn_var.get()

    def player_move(self, r, c):
        """Xử lý khi người dùng click chuột đánh cờ"""
        if self.board[r][c] != EMPTY:
            return
            
        # Khóa ô chọn đi trước lại khi ván đấu đang diễn ra để tránh lỗi logic
        self.turn_cb.config(state="disabled")
        
        # --- LƯỢT NGƯỜI CHƠI (X) ---
        self.board[r][c] = PLAYER_X
        self.buttons[r][c].config(text=PLAYER_X, fg="red", state=tk.DISABLED)
        
        if check_win(self.board, PLAYER_X):
            messagebox.showinfo("Kết quả", "Chúc mừng! Bạn đã thắng cuộc (X)!")
            self.freeze_board()
            return
            
        if is_board_full(self.board):
            messagebox.showinfo("Kết quả", "Kết quả: Hòa cờ! Bàn cờ đã đầy.")
            return
            
        self.root.update()
        self.ai_move()
        
    def ai_move(self):
        """Kích hoạt AI suy nghĩ và đánh cờ"""
        self.log_label.config(text=f"AI [{self.ai_mode.upper()}] đang suy nghĩ...", fg="orange")
        self.root.update()
        
        self.ai.state_count = 0
        start = time.time()
        
        if self.ai_mode == "minimax":
            score, best_move = self.ai.minimax(self.board, self.depth_limit, True)
        else:
            score, best_move = self.ai.alpha_beta(self.board, self.depth_limit, float('-inf'), float('inf'), True)
            
        runtime = (time.time() - start) * 1000
        
        # --- LƯỢT MÁY TÍNH (O) ---
        if best_move:
            r, c = best_move
            self.board[r][c] = AI_O
            self.buttons[r][c].config(text=AI_O, fg="blue", state=tk.DISABLED, bg="#EAEAEA")
            
            # Đẩy log thực nghiệm (Level 3) xuống góc dưới màn hình GUI
            self.log_label.config(text=f"[LOG]: Ô đánh: {r} {c} | Điểm: {score} | Trạng thái xét: {self.ai.state_count} | Thời gian: {runtime:.2f} ms", fg="green")
            
            if check_win(self.board, AI_O):
                messagebox.showinfo("Kết quả", "AI (O) đã thắng cuộc! Hẹn gặp lại ván sau.")
                self.freeze_board()
                return
                
            if is_board_full(self.board):
                messagebox.showinfo("Kết quả", "Kết quả: Hòa cờ! Bàn cờ đã đầy.")
                return

    def freeze_board(self):
        """Khóa bàn cờ khi kết thúc ván"""
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.buttons[r][c].config(state=tk.DISABLED)
        self.turn_cb.config(state="readonly")

    def reset_game(self):
        """Làm mới bàn cờ và áp dụng cấu hình đi trước mới"""
        self.board = create_board()
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.buttons[r][c].config(text="", state=tk.NORMAL, bg="#F0F0F0")
                
        # Mở khóa ô chọn đi trước cho ván mới
        self.turn_cb.config(state="readonly")
        self.change_config()
        
        # Nếu chọn Máy đi trước thì kích hoạt AI đi ngay lập tức
        if self.first_turn == "Máy (O)":
            self.log_label.config(text="Máy (O) được quyền đi trước!", fg="blue")
            self.root.update()
            self.ai_move()
        else:
            self.log_label.config(text="Lượt mới bắt đầu! Bạn đi trước (X).", fg="blue")

if __name__ == "__main__":
    root = tk.Tk()
    app = CaroGUI(root)
    root.mainloop()