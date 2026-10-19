import streamlit as st
import random

# Cài đặt trang
st.set_page_config(page_title="Bốc Lì Xì May Mắn", page_icon="🧧", layout="centered")

# Hàm khởi tạo lại trò chơi
def reset_game():
    # Tạo danh sách 20 bao theo số lượng mới
    # 9 bao 10k, 7 bao 20k, 2 bao 30k, 2 bao 50k
    values = [10000] * 9 + [20000] * 7 + [30000] * 2 + [50000] * 2
    random.shuffle(values) # Xáo trộn ngẫu nhiên
    
    st.session_state.envelopes = values
    st.session_state.opened = [False] * 20
    st.session_state.turns_left = 4
    st.session_state.total_won = 0
    st.session_state.history = []

# Khởi tạo dữ liệu lần đầu tiên
if 'envelopes' not in st.session_state:
    reset_game()

# Hàm xử lý khi người dùng bấm mở bao
def open_envelope(index):
    if st.session_state.turns_left > 0 and not st.session_state.opened[index]:
        value = st.session_state.envelopes[index]
        st.session_state.opened[index] = True
        st.session_state.turns_left -= 1
        st.session_state.total_won += value
        st.session_state.history.append(value)

# --- GIAO DIỆN CHÍNH ---
st.title("🧧 Hái Lộc Đầu Xuân - Bốc Bao Lì Xì 🧧")

# Hiển thị trạng thái
col1, col2 = st.columns(2)
with col1:
    st.subheader(f"🎯 Lượt bốc còn lại: {st.session_state.turns_left} / 4")
with col2:
    st.subheader(f"💰 Tổng tiền: {st.session_state.total_won:,}đ")

st.markdown("---")

# Vẽ lưới 20 bao lì xì (4 hàng, mỗi hàng 5 bao)
cols = st.columns(5)
for i in range(20):
    col_index = i % 5
    with cols[col_index]:
        if st.session_state.opened[i]:
            # Nếu đã mở thì hiển thị số tiền và vô hiệu hóa nút
            st.button(f"{st.session_state.envelopes[i]:,}đ", key=f"btn_{i}", disabled=True, use_container_width=True)
        else:
            # Nếu chưa mở
            st.button("🧧 Mở", key=f"btn_{i}", on_click=open_envelope, args=(i,), disabled=(st.session_state.turns_left == 0), use_container_width=True)

st.markdown("---")

# Hiển thị thông báo khi hết lượt
if st.session_state.turns_left == 0:
    st.success("🎉 Bạn đã dùng hết lượt bốc! Chúc mừng năm mới! 🎉")
    st.write("**Chi tiết các bao bạn đã bốc được:**")
    st.info(" + ".join([f"{v:,}đ" for v in st.session_state.history]))

# Nút chơi lại
st.button("🔄 Chơi lại từ đầu", on_click=reset_game, type="primary")
