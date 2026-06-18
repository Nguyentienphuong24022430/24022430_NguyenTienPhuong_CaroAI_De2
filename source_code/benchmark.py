import json
import os
import time
import copy  
from ai_agent import CaroAI

def load_test_states():
    """Tự động tìm và đọc file dữ liệu kiểm thử từ thư mục tests hoặc cùng cấp"""
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "tests", "test_states.json"),
        os.path.join(os.path.dirname(__file__), "test_states.json"),
        "test_states.json"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
    raise FileNotFoundError("Không tìm thấy file test_states.json! Hãy chắc chắn bạn đã tạo file này trong thư mục tests.")

def run_benchmark():
    data = load_test_states()
    ai = CaroAI()
    
    print(f"\n{'Trạng Thái':<18} | {'Depth':<5} | {'Thuật Toán':<12} | {'Nước Đi':<10} | {'Điểm':<8} | {'Số Trạng Thái':<13} | {'Thời Gian (ms)':<15}")
    print("-" * 95)
    
    for state in data["states"]:
        name = state["name"]
        original_board = state["board"]
        
        for depth in [1, 2, 3, 4]:
            
            # --- KIỂM THỬ MINIMAX ---
            if depth <= 3:
                board_mm = copy.deepcopy(original_board)
                ai.state_count = 0
                start = time.time()
                score_mm, move_mm = ai.minimax(board_mm, depth, True)
                time_mm = (time.time() - start) * 1000
                count_mm = ai.state_count
            else:
                score_mm, move_mm, count_mm, time_mm = "N/A", "N/A", "N/A", 0.0
            
            # --- KIỂM THỬ ALPHA-BETA PRUNING ---
            board_ab = copy.deepcopy(original_board)
            ai.state_count = 0
            start = time.time()
            score_ab, move_ab = ai.alpha_beta(board_ab, depth, float('-inf'), float('inf'), True)
            time_ab = (time.time() - start) * 1000
            count_ab = ai.state_count
            
            time_mm_str = f"{time_mm:.2f}" if isinstance(time_mm, float) and time_mm > 0 else "0.00"
            if score_mm == "N/A": time_mm_str = "N/A"
            
            print(f"{name:<18} | {depth:<5} | {'Minimax':<12} | {str(move_mm):<10} | {score_mm:<8} | {count_mm:<13} | {time_mm_str}")
            print(f"{'':<18} | {'':<5} | {'Alpha-Beta':<12} | {str(move_ab):<10} | {score_ab:<8} | {count_ab:<13} | {time_ab:.2f}")
        print("-" * 95)

if __name__ == "__main__":
    run_benchmark()