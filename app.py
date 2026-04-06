import streamlit as st
import math
import matplotlib.pyplot as plt

# Cấu hình trang
st.set_page_config(page_title="KNN Visualizer", layout="wide")

st.title("🤖 Minh họa Thuật toán KNN")
st.write("Thay vì nhập code, hãy kéo thanh trượt để thấy kết quả thay đổi trực tiếp!")

# ===== 1. LOAD DỮ LIỆU =====
def load_data():
    return [(16, 13, "A"), (24, 34, "A"), (23, 37, "A"), (15, 26, "A"),
        (34, 75, "A"), (3, 3, "A"), (4, 2, "A"), (6, 3, "A"),
        (41, 45, "A"), (37, 73, "A"), (34, 71, "A"), (46, 42, "A"),
        (42, 46, "A"), (3, 7, "A"), (4, 4, "A"),
           (66, 37, "B"), (60, 50, "B"), (50, 60, "B"), (62, 38, "B"),
        (69, 59, "B"), (58, 68, "B"), (61, 31, "B"), (46, 45, "B"),
        (35, 36, "B"), (61, 35, "B"), (7, 7, "B"), (8, 6, "B"),
        (6, 6, "B"), (6, 5, "B"), (5, 6, "B")]

def compute_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# ===== GIAO DIỆN BÊN TRÁI (SIDEBAR) =====
st.sidebar.header("Cài đặt thông số")
x_test = st.sidebar.slider("Tọa độ X của điểm Test", 0.0, 100.0, 5.0)
y_test = st.sidebar.slider("Tọa độ Y của điểm Test", 0.0, 100.0, 5.0)
k = st.sidebar.number_input("Giá trị K (số láng giềng)", min_value=1, max_value=10, value=3)

new_point = (x_test, y_test)
data = load_data()

# Xử lý Logic
distances = []
for x, y, label in data:
    d = compute_distance((x, y), new_point)
    distances.append((d, label, (x, y)))

distances.sort()
neighbors = distances[:k]
labels = [label for _, label, _ in neighbors]
result = max(set(labels), key=labels.count)

# ===== HIỂN THỊ KẾT QUẢ =====
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Đồ thị trực quan")
    fig, ax = plt.subplots()
    xA, yA = [p[0] for p in data if p[2]=="A"], [p[1] for p in data if p[2]=="A"]
    xB, yB = [p[0] for p in data if p[2]=="B"], [p[1] for p in data if p[2]=="B"]
    
    ax.scatter(xA, yA, color="#3498db", label="Lớp A", s=100)
    ax.scatter(xB, yB, color="#2ecc71", label="Lớp B", s=100)
    ax.scatter(x_test, y_test, color="#e74c3c", marker="X", s=300, label="Điểm cần đoán")

    # Khoanh tròn láng giềng
    for d, label, point in neighbors:
        circle = plt.Circle(point, 0.3, color='black', fill=False)
        ax.add_patch(circle)

    ax.set_xlabel("Trục X")
    ax.set_ylabel("Trục Y")
    ax.legend()
    ax.grid(alpha=0.3)
    st.pyplot(fig)

with col2:
    st.subheader("🔍 Kết quả phân tích")
    st.metric(label="Dự đoán lớp", value=f"Lớp {result}")
    
    st.write("**Danh sách láng giềng gần nhất:**")
    for d, label, point in neighbors:
        st.write(f"- Điểm {point}: Lớp {label} (Khoảng cách: {round(d, 2)})")

    st.info(f"Dựa trên K={k}, điểm đỏ thuộc về lớp có đa số láng giềng xung quanh.")
