import random

import sys
import io

# Thiết lập UTF-8 để xử lý Unicode
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

random.seed(42)

def hill_climbing_knapsack(weights, values, capacity, num_restarts=20):
    n = len(weights)

    if all(weight > capacity for weight in weights):
        return 0, []

    best_overall_value = 0
    best_overall_solution = []

    for restart in range(num_restarts):
        # Khởi tạo giải pháp ngẫu nhiên
        current_solution = [random.choice([0, 1]) for _ in range(n)]
        current_value, current_weight = calculate_solution(weights, values, current_solution, capacity)

        step = 0
        stuck_count = 0

        while True:
            print(f"\nBước {step}: Giải pháp hiện tại: {current_solution}, Giá trị: {current_value}, Trọng lượng: {current_weight}".encode('utf-8', errors='replace').decode('utf-8'))
            neighbors = generate_neighbors(current_solution)
            best_neighbor = current_solution
            best_value = current_value
            best_weight = current_weight

            improved = False

            for neighbor in neighbors:
                neighbor_value, neighbor_weight = calculate_solution(weights, values, neighbor, capacity)
                print(f"  Hàng xóm: {neighbor}, Giá trị: {neighbor_value}, Trọng lượng: {neighbor_weight}".encode('utf-8', errors='replace').decode('utf-8'))

                if neighbor_weight <= capacity and neighbor_value > best_value:
                    best_neighbor = neighbor
                    best_value = neighbor_value
                    best_weight = neighbor_weight
                    improved = True

            if not improved:
                stuck_count += 1
                if stuck_count >= 2:
                    break
            else:
                stuck_count = 0

            current_solution = best_neighbor
            current_value = best_value
            current_weight = best_weight
            step += 1

        # Cập nhật giải pháp tốt nhất trong tất cả các lần chạy
        if current_value > best_overall_value:
            best_overall_value = current_value
            best_overall_solution = current_solution

    selected_items = [(weights[i], values[i]) for i in range(n) if best_overall_solution[i] == 1]
    return best_overall_value, selected_items

def calculate_solution(weights, values, solution, capacity):
    total_value = sum(values[i] for i in range(len(solution)) if solution[i] == 1)
    total_weight = sum(weights[i] for i in range(len(solution)) if solution[i] == 1)
    if total_weight > capacity:
        return 0, float('inf')
    return total_value, total_weight


def generate_neighbors(solution):
    neighbors = []
    for i in range(len(solution)):
        neighbor = solution[:]
        neighbor[i] = 1 - neighbor[i]
        neighbors.append(neighbor)
    return neighbors