import pandas as pd

# Danh sách ban đầu
data = [{'SDT': '099592344', 'HoTenNguoiNhan': 'Hung'}, {'SDT': '113', 'HoTenNguoiNhan': 'Hung'}]

# Chuyển đổi thành DataFrame
df = pd.DataFrame(data)

# Đổi tên cột
df = df.rename(columns={'HoTenNguoiNhan': 'Họ tên người nhận', 'SDT': 'SĐT'})

# Đổi thứ tự cột để "Họ tên người nhận" ở vị trí đầu tiên
df = df[['Họ tên người nhận', 'SĐT']]

# Hiển thị DataFrame
print(df)
