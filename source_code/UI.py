import tkinter as tk
from tkinter import messagebox, ttk
import time
from config import PLAYER_X, AI_O, EMPTY, BOARD_SIZE
from game_logic import check_win, is_board_full, create_board
from ai_agent import CaroAI

class CaroGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CHƯƠNG TRÌNH CỜ CARO AI - NGUYỄN TIẾN PHƯƠNG")

        self.root.geometry("620x720")
        self.root.configure(bg="#F8F9FA")
        
        # Khởi tạo ma trận bàn cờ và AI
        self.board = create_board()
        self.ai = CaroAI()
        
        self.ai_mode = "alpha_beta"
        self.depth_limit = 4  
        self.first_turn = "Người (X)"
        self.game_started = False  
        
        self.setup_styles()
        self.setup_menu()
        self.setup_board_ui()
        
    def setup_styles(self):
        """Định nghĩa style hiện đại cho các thành phần UI"""
        style = ttk.Style()
        style.theme_use("clam")  
        style.configure("Top.TFrame", background="#ECEFF1")
        style.configure("TLabel", background="#ECEFF1", font=("Segoe UI", 10))
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), foreground="white", background="#2A9D8F")
        style.map("Action.TButton", background=[("active", "#21867A")])

    def setup_menu(self):
        """Tạo thanh điều khiển cấu hình thuật toán, độ sâu và lượt đi trước"""
        control_frame = ttk.Frame(self.root, style="Top.TFrame", padding=12)
        control_frame.pack(side=tk.TOP, fill=tk.X)
    
        ttk.Label(control_frame, text="Thuật toán:").grid(row=0, column=0, padx=4, sticky="w")
        self.mode_var = tk.StringVar(value="Alpha-Beta Pruning")
        self.mode_cb = ttk.Combobox(control_frame, textvariable=self.mode_var, 
                               values=["Minimax gốc", "Alpha-Beta Pruning"], 
                               state="readonly", width=16, font=("Segoe UI", 9))
        self.mode_cb.grid(row=0, column=1, padx=4)
        self.mode_cb.bind("<<ComboboxSelected>>", self.change_config)
        
        ttk.Label(control_frame, text="Độ sâu:").grid(row=0, column=2, padx=4, sticky="w")
        self.depth_var = tk.IntVar(value=4)
        self.depth_cb = ttk.Combobox(control_frame, textvariable=self.depth_var, 
                                values=[1, 2, 3, 4], 
                                state="readonly", width=3, font=("Segoe UI", 9))
        self.depth_cb.grid(row=0, column=3, padx=4)
        self.depth_cb.bind("<<ComboboxSelected>>", self.change_config)
        
        ttk.Label(control_frame, text="Đi trước:").grid(row=0, column=4, padx=4, sticky="w")
        self.turn_var = tk.StringVar(value="Người (X)")
        self.turn_cb = ttk.Combobox(control_frame, textvariable=self.turn_var, 
                               values=["Người (X)", "Máy (O)"], 
                               state="readonly", width=9, font=("Segoe UI", 9))
        self.turn_cb.grid(row=0, column=5, padx=4)
        self.turn_cb.bind("<<ComboboxSelected>>", self.change_config)
        
        reset_btn = ttk.Button(control_frame, text="Ván Mới", style="Action.TButton", command=self.reset_game)
        reset_btn.grid(row=0, column=6, padx=12)
        
        self.log_label = tk.Label(self.root, text="Hệ thống sẵn sàng. Hãy chọn cấu hình cấu hình rồi bấm 'Ván Mới'!", 
                                  bg="#F8F9FA", fg="#4A5568", font=("Segoe UI", 10, "italic"))
        self.log_label.pack(side=tk.BOTTOM, fill=tk.X, pady=8)
        
    def setup_board_ui(self):
        """Khởi tạo lưới ma trận các nút bấm phẳng, bo góc nhẹ đại diện cho bàn cờ 9x9"""
        self.board_wrapper = tk.Frame(self.root, bg="#D1D5DB", bd=1, relief=tk.FLAT)
        self.board_wrapper.pack(padx=20, pady=25)
        
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                btn = tk.Button(self.board_wrapper, text="", font=("Segoe UI", 13, "bold"), 
                                width=4, height=2, bg="#FFFFFF", fg="#FFFFFF",
                                activebackground="#E9ECEF", relief=tk.FLAT, bd=0)
                btn.grid(row=r, column=c, padx=1, pady=1) 
                
                btn.bind("<Enter>", lambda event, button=btn: self.on_hover(button))
                btn.bind("<Leave>", lambda event, button=btn: self.on_leave(button))
                btn.config(command=lambda row=r, col=c: self.player_move(row, col))
                
                self.buttons[r][c] = btn
                
    def on_hover(self, button):
        """Hiệu ứng đổi màu nhẹ khi di chuột vào ô trống"""
        if button['state'] == tk.NORMAL:
            button.config(bg="#E9ECEF")

    def on_leave(self, button):
        """Trả lại màu trắng khi di chuột ra ngoài ô trống"""
        if button['state'] == tk.NORMAL:
            button.config(bg="#FFFFFF")
                
    def change_config(self, event=None):
        """Cập nhật cấu hình khi người dùng chọn trên combobox"""
        choice = self.mode_var.get()
        self.ai_mode = "alpha_beta" if choice == "Alpha-Beta Pruning" else "minimax"
        self.depth_limit = int(self.depth_var.get())
        self.first_turn = self.turn_var.get()

    def lock_controls(self):
        """Khóa toàn bộ combo chọn cấu hình thuật toán, độ sâu và lượt đi khi game đang chạy"""
        self.game_started = True
        self.mode_cb.config(state="disabled")
        self.depth_cb.config(state="disabled")
        self.turn_cb.config(state="disabled")

    def unlock_controls(self):
        """Mở khóa combo chọn khi ván game kết thúc hoặc bấm làm mới"""
        self.game_started = False
        self.mode_cb.config(state="readonly")
        self.depth_cb.config(state="readonly")
        self.turn_cb.config(state="readonly")

    def player_move(self, r, c):
        """Xử lý khi người dùng click chuột đánh cờ"""
        if self.board[r][c] != EMPTY:
            return
            
        if not self.game_started:
            self.lock_controls()
        
        # --- LƯỢT NGƯỜI CHƠI (X)
        self.board[r][c] = PLAYER_X
        self.buttons[r][c].config(text=PLAYER_X, fg="#E63946", bg="#F8D7DA", state=tk.DISABLED)
        
        if check_win(self.board, PLAYER_X):
            messagebox.showinfo("Kết quả", "Chúc mừng! Bạn đã thắng cuộc (X)!")
            self.freeze_board()
            return
            
        if is_board_full(self.board):
            messagebox.showinfo("Kết quả", "Kết quả: Hòa cờ! Bàn cờ đã đầy.")
            self.unlock_controls()
            return
            
        self.root.update()
        self.ai_move()
        
    def ai_move(self):
        """Kích hoạt AI suy nghĩ và đánh cờ"""
        self.log_label.config(text=f"AI [{self.ai_mode.upper()}] đang tính toán ở Depth {self.depth_limit}...", fg="#D97706")
        self.root.update()
        
        self.ai.state_count = 0
        start = time.time()
        
        if self.ai_mode == "minimax":
            score, best_move = self.ai.minimax(self.board, self.depth_limit, True)
        else:
            score, best_move = self.ai.alpha_beta(self.board, self.depth_limit, float('-inf'), float('inf'), True)
            
        runtime = (time.time() - start) * 1000
        
        # --- LƯỢT MÁY TÍNH (O) 
        if best_move:
            r, c = best_move
            self.board[r][c] = AI_O
            self.buttons[r][c].config(text=AI_O, fg="#1D3557", bg="#CCE5FF", state=tk.DISABLED)
            
            self.log_label.config(text=f"[LOG]: Ô đánh: ({r}, {c}) | Điểm: {score} | Duyệt: {self.ai.state_count} trạng thái | Thời gian: {runtime:.2f} ms", fg="#2563EB")
            
            if check_win(self.board, AI_O):
                messagebox.showinfo("Kết quả", "AI (O) đã thắng cuộc! Hẹn gặp lại ván sau.")
                self.freeze_board()
                return
                
            if is_board_full(self.board):
                messagebox.showinfo("Kết quả", "Kết quả: Hòa cờ! Bàn cờ đã đầy.")
                self.unlock_controls()
                return

    def freeze_board(self):
        """Khóa toàn bộ bàn cờ khi kết thúc ván"""
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.buttons[r][c].config(state=tk.DISABLED)
        self.unlock_controls()

    def reset_game(self):
        """Làm mới bàn cờ và giải phóng trạng thái khóa của menu cấu hình"""
        self.board = create_board()
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.buttons[r][c].config(text="", state=tk.NORMAL, bg="#FFFFFF")
                
        self.unlock_controls()
        self.change_config()
        
        if self.first_turn == "Máy (O)":
            self.lock_controls()
            self.log_label.config(text="Máy (O) được quyền đi trước và đang tính toán...", fg="#2563EB")
            self.root.update()
            self.ai_move()
        else:
            self.log_label.config(text="Ván mới bắt đầu! Hãy chọn ô trên lưới để đi nước đầu tiên (X).", fg="#059669")

if __name__ == "__main__":
    root = tk.Tk()
    app = CaroGUI(root)
    root.mainloop()