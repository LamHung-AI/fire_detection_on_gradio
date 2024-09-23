import argparse

parser = argparse.ArgumentParser(description="Tạo tài khoản mới")

parser.add_argument("-a", "--account", type=str, required=True, help="Nhập tài khoản")
parser.add_argument("-p", "--password", type=str, required=True, help="Nhập mật khẩu")

# Thêm dòng này để parse các tham số từ dòng lệnh
args = parser.parse_args()

print(args.account, args.password)