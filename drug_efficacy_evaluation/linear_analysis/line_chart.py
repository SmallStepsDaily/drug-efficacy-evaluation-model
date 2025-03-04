import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
data = pd.read_csv(r"C:\Code\python\csv_data\hql\2、4、6h药效评估.csv")

# 获取所有唯一的Metadata_treatment标签（排除control）
treatments = data['Metadata_treatment'].unique()
treatments = treatments[treatments != 'control']

# 创建图形和子图
fig, axs = plt.subplots(len(treatments), 1, figsize=(12, 7 * len(treatments)))

# 全局字体设置
plt.rcParams.update({'font.size': 14})

for i, treatment in enumerate(treatments):
    # 筛选出当前处理的数据
    df_treatment = data[data['Metadata_treatment'] == treatment]

    # 绘制S和E的折线图
    axs[i].plot(df_treatment['Metadata_hour'], df_treatment['S'], color='blue', label='S')
    axs[i].plot(df_treatment['Metadata_hour'], df_treatment['E'], color='red', label='E')

    # 设置标题和标签，并增加字体大小
    axs[i].set_title(f'Treatment: {treatment}', fontsize=18)
    axs[i].set_xlabel('Time (hours)', fontsize=16)
    axs[i].set_ylabel('Different Eigenvalues', fontsize=16)

    # 添加图例到右上角，并增加字体大小
    axs[i].legend(loc='upper right', fontsize=14)

# 调整布局以防止重叠
plt.tight_layout()

# 显示图形
plt.show()