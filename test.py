def is_all_digits(s):
    return s.isnumeric()

# Ví dụ sử dụng
s1 = "12345"
s2 = "123a45"
s3 = "12.34"

print(is_all_digits(s1))  # True
print(is_all_digits(s2))  # False
print(is_all_digits(s3))  # False
