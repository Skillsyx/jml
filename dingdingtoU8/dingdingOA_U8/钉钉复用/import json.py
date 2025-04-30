# 首先安装：pip install stdlib-list
from stdlib_list import stdlib_list

stdlib = stdlib_list("3.12")
print("是否为标准库:", "json" in stdlib)  # True
print("是否为标准库:", "requests" in stdlib)  # False
