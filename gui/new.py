import random
from tkinter import Tk, Label, Entry, Button, Text, messagebox, Spinbox, Canvas, Frame, Scrollbar, StringVar

# 3. Áp dụng thuật toán Hill Climbing vào bài toán cái túi

# Hàm giải bài toán cái túi bằng phương pháp Hill Climbing
def hill_climbing_knapsack(weights, values, capacity):
    n = len(weights)
    
    # Khởi tạo giải pháp ngẫu nhiên
    current_solution = [random.choice([0, 1]) for _ in range(n)]
    current_value, current_weight = calculate_solution(weights, values, current_solution, capacity)
    
    step = 0  # Biến đếm số bước
    while True:
        print(f"\nBước {step}: Giải pháp hiện tại: {current_solution}, Giá trị: {current_value}, Trọng lượng: {current_weight}")
        
        # Tạo danh sách các giải pháp hàng xóm
        neighbors = generate_neighbors(current_solution)
        improved = False
        
        # Duyệt qua các hàng xóm và chọn hàng xóm tốt nhất
        for neighbor in neighbors:
            neighbor_value, neighbor_weight = calculate_solution(weights, values, neighbor, capacity)
            print(f"  Hàng xóm: {neighbor}, Giá trị: {neighbor_value}, Trọng lượng: {neighbor_weight}")
            
            # Cập nhật nếu có hàng xóm tốt hơn
            if neighbor_weight <= capacity and neighbor_value > current_value:
                current_solution = neighbor
                current_value = neighbor_value
                current_weight = neighbor_weight
                improved = True
                break
        
        # Dừng nếu không có cải thiện
        if not improved:
            break
        step += 1

    # Chọn các đồ vật trong giải pháp tốt nhất
    selected_items = [(weights[i], values[i]) for i in range(n) if current_solution[i] == 1]
    return current_value, selected_items

# Hàm tính tổng giá trị và trọng lượng của một giải pháp
def calculate_solution(weights, values, solution, capacity):
    total_value = sum(values[i] for i in range(len(solution)) if solution[i] == 1)
    total_weight = sum(weights[i] for i in range(len(solution)) if solution[i] == 1)
    return total_value, total_weight

# Hàm tạo các láng giềng của một giải pháp
def generate_neighbors(solution):
    neighbors = []
    for i in range(len(solution)):
        neighbor = solution[:]
        neighbor[i] = 1 - neighbor[i]  # Lật giá trị của phần tử tại vị trí i
        neighbors.append(neighbor)
    return neighbors

# Hàm tính toán và hiển thị kết quả
def calculate():
    try:
        weights = [int(weight_entries[i].get()) for i in range(len(weight_entries))]
        values = [int(value_entries[i].get()) for i in range(len(value_entries))]
        capacity = int(capacity_spinbox.get())
        
        max_value, selected_items = hill_climbing_knapsack(weights, values, capacity)
        
        # Hiển thị kết quả
        result_text.delete(1.0, 'end')
        result_text.insert('end', f'Tối đa giá trị đạt được: {max_value}\n')
        result_text.insert('end', 'Danh sách đồ vật được chọn:\n')
        for i, (weight, value) in enumerate(selected_items, start=1):
            result_text.insert('end', f' - Đồ vật {i}: Trọng lượng = {weight}, Giá trị = {value}\n')
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# Hàm xóa một dòng (xóa đồ vật tại vị trí index)
def delete_row(index):
    item_labels[index].grid_forget()
    weight_entries[index].grid_forget()
    value_entries[index].grid_forget()
    delete_buttons[index].grid_forget()
    
    item_labels.pop(index)
    weight_entries.pop(index)
    value_entries.pop(index)
    delete_buttons.pop(index)

    num_items_var.set(len(weight_entries))
    update_entries_layout()

# Hàm cập nhật các ô nhập liệu khi thay đổi số lượng đồ vật
def update_entries(*args):
    num_items = int(num_items_var.get())
    
    for widget in item_frame.winfo_children():
        widget.destroy()

    item_labels.clear()
    weight_entries.clear()
    value_entries.clear()
    delete_buttons.clear()

    Label(item_frame, text="Trọng lượng", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)
    Label(item_frame, text="Giá trị", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)

    for i in range(num_items):
        item_label = Label(item_frame, text=f"Đồ vật {i + 1}", font=("Arial", 10))
        item_label.grid(row=i + 1, column=0, padx=5, pady=5)
        item_labels.append(item_label)

        weight_entry = Entry(item_frame, font=("Arial", 10), width=10)
        weight_entry.grid(row=i + 1, column=1, padx=5, pady=5)
        weight_entries.append(weight_entry)

        value_entry = Entry(item_frame, font=("Arial", 10), width=10)
        value_entry.grid(row=i + 1, column=2, padx=5, pady=5)
        value_entries.append(value_entry)

        delete_button = Button(item_frame, text="Xóa", command=lambda i=i: delete_row(i), font=("Arial", 10), bg="#FF5733", fg="white")
        delete_button.grid(row=i + 1, column=3, padx=5, pady=5)
        delete_buttons.append(delete_button)

    item_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def update_entries_layout():
    for i, (item_label, weight_entry, value_entry, delete_button) in enumerate(zip(item_labels, weight_entries, value_entries, delete_buttons)):
        item_label.config(text=f"Đồ vật {i + 1}")
        item_label.grid(row=i + 1, column=0, padx=5, pady=5)
        weight_entry.grid(row=i + 1, column=1, padx=5, pady=5)
        value_entry.grid(row=i + 1, column=2, padx=5, pady=5)
        delete_button.grid(row=i + 1, column=3, padx=5, pady=5)

# Khởi tạo cửa sổ ứng dụng
window = Tk()
window.title("Bài Toán Cái Túi - Hill Climbing")
window.geometry("500x600")
window.configure(bg="#F0F0F0")

Label(window, text="Số loại đồ vật:", font=("Arial", 12)).place(x=20, y=10)
Label(window, text="Trọng lượng balo:", font=("Arial", 12)).place(x=220, y=10)

num_items_var = StringVar(value="4")
num_items_var.trace("w", update_entries)

num_items_spinbox = Spinbox(window, from_=1, to=20, textvariable=num_items_var, font=("Arial", 12), width=5)
num_items_spinbox.place(x=130, y=10)

capacity_spinbox = Spinbox(window, from_=1, to=100, font=("Arial", 12), width=5)
capacity_spinbox.place(x=350, y=10)

canvas = Canvas(window, width=450, height=300)
canvas.place(x=20, y=50)

scrollbar = Scrollbar(window, orient="vertical", command=canvas.yview)
scrollbar.place(x=470, y=50, height=300)

canvas.configure(yscrollcommand=scrollbar.set)

item_frame = Frame(canvas)
canvas.create_window((0, 0), window=item_frame, anchor="nw")

item_labels = []
weight_entries = []
value_entries = []
delete_buttons = []

update_entries()

calculate_button = Button(window, text="Tính", command=calculate, bg="#4A90E2", fg="white", font=("Arial", 12))
calculate_button.place(x=200, y=380)

result_text = Text(window, height=10, width=55, font=("Arial", 12))
result_text.place(x=20, y=420)

reset_button = Button(window, text="Đặt lại", command=lambda: [entry.delete(0, 'end') for entry in weight_entries + value_entries] + [result_text.delete(1.0, 'end')], bg="#F44336", fg="white", font=("Arial", 12))
reset_button.place(x=100, y=380)

window.mainloop()
