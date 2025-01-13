import numpy as np

# 设置每组数据的长度为2
value_num = 2

# 生成从0到1的1000个点的数组x，y是1减去x
x = np.linspace(0, 1, 1000)
y = 1 - x

# 定义数组S和FRET
S = np.array([0, 0, 0.1568, 0.1566, 0.0752, 0.1303, 0.1540, 0.1540, 0.1996, 0.2115])
FRET = np.array([0, 0, 0.3431, 0.3146, 0.0735, 0.0258, 0.0318, 0.0318, 0.0218, 0.0668])

# 对S和FRET进行归一化处理，范围在0到1之间
S_normalized = (S - np.min(S)) / (np.max(S) - np.min(S))
FRET_normalized = (FRET - np.min(FRET)) / (np.max(FRET) - np.min(FRET))

n = len(S_normalized)
sum_Z = np.zeros_like(x)
var_Z = np.zeros_like(x)
average_Z = np.zeros((n // value_num, len(x)))
a_b = np.zeros((n // value_num, 2))
R_value = np.zeros((n // value_num, value_num))

k = 0  # Python使用0开始索引

# 第一个循环，计算每组的平均值average_Z
for i in range(0, n, value_num):
    temp_sum = np.zeros_like(x)
    for j in range(value_num):
        if i + j >= n:
            break
        # 计算Z值
        Z = (FRET_normalized[i + j] * x + 1) ** (S_normalized[i + j] * y) - 1
        temp_sum += Z
    # 计算平均值
    average_Z[k, :] = temp_sum / value_num
    k += 1

# 重置k，开始第二个循环，计算方差var_Z和最大值及其位置
k = 0
for i in range(0, n, value_num):
    temp_var = np.zeros_like(x)
    for j in range(value_num):
        if i + j >= n:
            break
        # 计算Z值
        Z = (FRET_normalized[i + j] * x + 1) ** (S_normalized[i + j] * y) - 1
        # 计算方差
        Z1 = (Z - average_Z[k, :]) ** 2
        temp_var += Z1
    # 计算方差的均值
    temp_var /= (value_num - 1)
    # 找到最大方差值及其位置
    max_val = np.max(temp_var)
    position_max = np.argmax(temp_var)
    print(position_max)
    a_b[k, 0] = max_val
    a_b[k, 1] = position_max / 1000
    k += 1
print(a_b)
# 重置k，开始第三个循环，计算R_value
k = 0
for i in range(0, n, value_num):
    for j in range(value_num):
        if i + j >= n:
            break
        # 计算R值
        R = 100 * ((FRET_normalized[i + j] * a_b[k, 1] + 1) ** (S_normalized[i + j] * (1 - a_b[k, 1])) - 1)
        R_value[k, j] = R
    k += 1
# print(R_value)
# 定义数组C，包含对数值
C = np.array([-np.log10(1e-6), -np.log10(1e-6), -np.log10(1e-6), -np.log10(1e-4), -np.log10(0.6)])

# 定义数组t
t = np.array([5, 11, 5, 11, 5, 11, 1, 2, 1, 2])

# 对t进行z-score标准化
normalized_data = (t - np.mean(t)) / np.std(t)

Z_value = np.zeros((n // value_num, 1))
B_value = np.zeros((n // value_num, value_num))

k = 0
# 最终循环，计算Z_value和B_value
for i in range(0, n, value_num):
    for j in range(value_num):
        if i + j >= n:
            break
        # 计算y_B
        y_B = (C[k] ** (-normalized_data[i + j])) / (1 + C[k] ** (-normalized_data[i + j]))
        B_value[k, j] = y_B
        Z_value[k, 0] += y_B * R_value[k, j]
    k += 1