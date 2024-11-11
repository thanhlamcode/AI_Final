import random
from tkinter import Tk, Label, Entry, Button, Text, messagebox, Spinbox, Canvas, Frame, Scrollbar, StringVar

# 3. Áp dụng thuật toán Hill Climbing vào bài toán cái túi

# 3.1. Khởi tạo Knapsack Problem
# Hàm giải bài toán cái túi bằng phương pháp Hill Climbing
def hill_climbing_knapsack(weights, values, capacity):
    n = len(weights)
    
    # 3.2. Khởi tạo giải pháp ngẫu nhiên
    # Tạo giải pháp hiện tại bằng cách chọn ngẫu nhiên các đồ vật
    current_solution = [random.choice([0, 1]) for _ in range(n)]
    current_value, current_weight = calculate_solution(weights, values, current_solution, capacity)
    
    # 3.6. Tạo thuật toán Hill Climbing
    while True:
        # 3.4. Tạo function khởi tạo tất cả các giải pháp hàng xóm
        # Tạo danh sách các giải pháp láng giềng
        neighbors = generate_neighbors(current_solution)
        improved = False
        
        # 3.5. Tạo function tìm hàng xóm tốt nhất và giải pháp tối ưu
        # Duyệt qua các láng giềng và chọn láng giềng tốt nhất
        for neighbor in neighbors:
            neighbor_value, neighbor_weight = calculate_solution(weights, values, neighbor, capacity)
            # Cập nhật nếu có láng giềng tốt hơn
            if neighbor_weight <= capacity and neighbor_value > current_value:
                current_solution = neighbor
                current_value = neighbor_value
                current_weight = neighbor_weight
                improved = True
                break
        # Dừng nếu không có cải thiện
        if not improved:
            break

    # Chọn các đồ vật trong giải pháp tốt nhất
    selected_items = [(weights[i], values[i]) for i in range(n) if current_solution[i] == 1]
    return current_value, selected_items

# 3.3. Tạo hàm tính giá trị và trọng lượng của túi
# Hàm tính tổng giá trị và trọng lượng của một giải pháp
def calculate_solution(weights, values, solution, capacity):
    total_value = sum(values[i] for i in range(len(solution)) if solution[i] == 1)
    total_weight = sum(weights[i] for i in range(len(solution)) if solution[i] == 1)
    return total_value, total_weight

# 3.4. Tạo function khởi tạo tất cả các giải pháp hàng xóm
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
    # Xóa nhãn, ô nhập liệu, và nút xóa của đồ vật tại vị trí index
    item_labels[index].grid_forget()
    weight_entries[index].grid_forget()
    value_entries[index].grid_forget()
    delete_buttons[index].grid_forget()
    
    # Xóa đồ vật khỏi danh sách
    item_labels.pop(index)
    weight_entries.pop(index)
    value_entries.pop(index)
    delete_buttons.pop(index)

    # Cập nhật lại giá trị trong Spinbox để phản ánh số lượng đồ vật mới
    num_items_var.set(len(weight_entries))

    # Cập nhật lại giao diện các hàng còn lại
    update_entries_layout()

# Hàm cập nhật các ô nhập liệu khi thay đổi số lượng đồ vật
def update_entries(*args):
    # Lấy số lượng đồ vật hiện tại từ Spinbox
    num_items = int(num_items_var.get())
    
    # Xóa các widget cũ
    for widget in item_frame.winfo_children():
        widget.destroy()

    # Xóa danh sách cũ
    item_labels.clear()
    weight_entries.clear()
    value_entries.clear()
    delete_buttons.clear()

    # Thêm tiêu đề cột
    Label(item_frame, text="Trọng lượng", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)
    Label(item_frame, text="Giá trị", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)

    for i in range(num_items):
        # Tạo nhãn, ô nhập trọng lượng, ô nhập giá trị và nút xóa cho mỗi đồ vật
        item_label = Label(item_frame, text=f"Đồ vật {i + 1}", font=("Arial", 10))
        item_label.grid(row=i + 1, column=0, padx=5, pady=5)
        item_labels.append(item_label)

        weight_entry = Entry(item_frame, font=("Arial", 10), width=10)
        weight_entry.grid(row=i + 1, column=1, padx=5, pady=5)
        weight_entries.append(weight_entry)

        value_entry = Entry(item_frame, font=("Arial", 10), width=10)
        value_entry.grid(row=i + 1, column=2, padx=5, pady=5)
        value_entries.append(value_entry)

        # Tạo nút xóa với chỉ số index đúng
        delete_button = Button(item_frame, text="Xóa", command=lambda i=i: delete_row(i), font=("Arial", 10), bg="#FF5733", fg="white")
        delete_button.grid(row=i + 1, column=3, padx=5, pady=5)
        delete_buttons.append(delete_button)

    item_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Hàm cập nhật lại giao diện khi xóa một đồ vật
def update_entries_layout():
    # Cập nhật giao diện sau khi xóa
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

# Tiêu đề
Label(window, text="Số loại đồ vật:", font=("Arial", 12)).place(x=20, y=10)
Label(window, text="Trọng lượng balo:", font=("Arial", 12)).place(x=220, y=10)

# Biến theo dõi số lượng đồ vật trong Spinbox
num_items_var = StringVar(value="4")  # Giá trị mặc định là 4
num_items_var.trace("w", update_entries)  # Theo dõi thay đổi của biến

# Cấu hình Spinbox với biến theo dõi
num_items_spinbox = Spinbox(window, from_=1, to=20, textvariable=num_items_var, font=("Arial", 12), width=5)
num_items_spinbox.place(x=130, y=10)

capacity_spinbox = Spinbox(window, from_=1, to=100, font=("Arial", 12), width=5)
capacity_spinbox.place(x=350, y=10)

# Khu vực cuộn cho các đồ vật
canvas = Canvas(window, width=450, height=300)
canvas.place(x=20, y=50)

scrollbar = Scrollbar(window, orient="vertical", command=canvas.yview)
scrollbar.place(x=470, y=50, height=300)

canvas.configure(yscrollcommand=scrollbar.set)

# Khung chứa các ô nhập liệu cho đồ vật
item_frame = Frame(canvas)
canvas.create_window((0, 0), window=item_frame, anchor="nw")

# Danh sách để lưu các ô nhập liệu và nút xóa
item_labels = []
weight_entries = []
value_entries = []
delete_buttons = []

# Khởi tạo các ô nhập liệu
update_entries()

# Nút tính toán
calculate_button = Button(window, text="Tính", command=calculate, bg="#4A90E2", fg="white", font=("Arial", 12))
calculate_button.place(x=200, y=380)

# Hiển thị kết quả
result_text = Text(window, height=10, width=55, font=("Arial", 12))
result_text.place(x=20, y=420)

# Nút đặt lại
reset_button = Button(window, text="Đặt lại", command=lambda: [entry.delete(0, 'end') for entry in weight_entries + value_entries] + [result_text.delete(1.0, 'end')], bg="#F44336", fg="white", font=("Arial", 12))
reset_button.place(x=100, y=380)

window.mainloop()