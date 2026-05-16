# benchmark.py
import json
import os
import time
from ai_agent import CaroAI

def load_test_states():
    """Tự động tìm và đọc file dữ liệu kiểm thử từ thư mục tests"""
    test_file = os.path.join(os.path.dirname(__file__), "..", "tests", "test_states.json")
    with open(test_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_benchmark():
    data = load_test_states()
    ai = CaroAI()
    
    print(f"\n{'Trạng Thái':<18} | {'Depth':<5} | {'Thuật Toán':<12} | {'Nước Đi':<10} | {'Điểm':<8} | {'Số Trạng Thái':<13} | {'Thời Gian (ms)':<15}")
    print("-" * 95)
    
    for state in data["states"]:
        name = state["name"]
        board = state["board"]
        
        # Duyệt qua các mốc độ sâu 1, 2, 3 để phân tích biến động thời gian
        for depth in [1, 2, 3]:  
            # Kiểm thử Minimax
            ai.state_count = 0
            start = time.time()
            score_mm, move_mm = ai.minimax(board, depth, True)
            time_mm = (time.time() - start) * 1000
            count_mm = ai.state_count
            
            # Kiểm thử Alpha-Beta Pruning
            ai.state_count = 0
            start = time.time()
            score_ab, move_ab = ai.alpha_beta(board, depth, float('-inf'), float('inf'), True)
            time_ab = (time.time() - start) * 1000
            count_ab = ai.state_count
            
            print(f"{name:<18} | {depth:<5} | {'Minimax':<12} | {str(move_mm):<10} | {score_mm:<8} | {count_mm:<13} | {time_mm:.2f}")
            print(f"{'':<18} | {'':<5} | {'Alpha-Beta':<12} | {str(move_ab):<10} | {score_ab:<8} | {count_ab:<13} | {time_ab:.2f}")
        print("-" * 95)

if __name__ == "__main__":
    run_benchmark()