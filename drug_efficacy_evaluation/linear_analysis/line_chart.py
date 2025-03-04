import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 读取Excel文件
file_path = 'hql靶向药物.xlsx'
df = pd.read_excel(file_path, engine='openpyxl', header=0)

# 检查DataFrame结构
if '干扰' not in df.columns:
    raise ValueError("DataFrame中未找到'干扰'列，请检查您的Excel文件。")

# 设置时间作为x轴
time_points = df.columns[1:]  # 排除第一列"干扰"

fig, axes = plt.subplots(2, 1, figsize=(10, 8))


def plot_lines_for_disturbance(disturbance, ax, title):
    # 获取特定干扰类型的数据
    df_subset = df[df['干扰'] == disturbance]

    if df_subset.empty:
        print(f"DataFrame中未找到'{disturbance}'相关数据。")
        return

    # 对每一行绘制折线图
    for index, row in df_subset.iterrows():
        y_values = row.iloc[1:].values  # 忽略第一列（干扰）
        sns.lineplot(x=time_points, y=y_values, ax=ax, label=f'Line {index}')

    ax.set_title(title)
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.legend()


# 对于osimertinib
ax1 = axes[0]
plot_lines_for_disturbance('osimertinib', ax1, 'Osimertinib')

# 对于gefitinib
ax2 = axes[1]
plot_lines_for_disturbance('gefitinib', ax2, 'Gefitinib')

plt.tight_layout()
plt.show()