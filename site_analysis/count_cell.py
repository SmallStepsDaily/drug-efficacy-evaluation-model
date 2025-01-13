import os
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

def count_site_cell_sum(csv_path):

    # 获取文件夹中所有CSV文件
    csv_files = [f for f in os.listdir(csv_path) if f.endswith('.csv')]

    # 读取所有CSV文件并拼接成一个DataFrame
    dfs = []
    for file in csv_files:
        file_path = os.path.join(csv_path, file)
        df = pd.read_csv(file_path)
        dfs.append(df)

    # 拼接所有DataFrame
    combined_df = pd.concat(dfs, ignore_index=True)

    # 按 Metadata_hour 和 Metadata_treatment 分组，并计算 Metadata_site 的平均值
    result = combined_df.groupby(['Metadata_hour', 'Metadata_treatment'])['Metadata_site'].mean().reset_index()

    # 打印结果
    draw_line_hist(result)


def draw_line_hist(result_df):
    # 设置 seaborn 样式
    sns.set(style='whitegrid', font_scale=1.2)

    # 获取唯一的时间点和处理方式
    hours = sorted(result_df['Metadata_hour'].unique())
    treatments = result_df['Metadata_treatment'].unique()
    n = len(treatments)

    # 设置绘图参数
    fig, ax = plt.subplots(figsize=(12, 8))
    bar_width = 0.8 / n
    index = range(len(hours))

    # 获取颜色列表
    palette = sns.color_palette('Set1', n)

    # 绘制分组柱状图
    for i, treatment in enumerate(treatments):
        subset = result_df[result_df['Metadata_treatment'] == treatment]
        bars = ax.bar([x + i * bar_width for x in index], subset['Metadata_site'], bar_width, label=treatment,
                      color=palette[i], alpha=0.5)
        # 添加数据标签
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points above the bar
                        textcoords='offset points',
                        ha='center', va='bottom')

    # 绘制每个 treatment 的折线图
    for i, treatment in enumerate(treatments):
        subset = result_df[result_df['Metadata_treatment'] == treatment]
        x_line = [x + i * bar_width for x in index]  # 柱子的中心位置
        ax.plot(x_line, subset['Metadata_site'], marker='o', color=palette[i], label=f'{treatment} Line',
                linestyle='--')

    # 设置轴标签和图例
    ax.set_xticks([x + bar_width * (n - 1) / 2 for x in index])
    ax.set_xticklabels(hours)
    ax.set_xlabel('Hour')
    ax.set_ylabel('Average Number of Cells')
    ax.set_title('Average Number of Cells by Hour and Treatment in the Site')
    ax.legend(title='Treatment', loc='upper right')
    ax.grid(True)

    # 设置y轴的范围和刻度
    ax.set_ylim(0, 20)
    ax.set_yticks(range(0, 21, 5))

    plt.show()


if __name__ == "__main__":
    csv_path = r'C:\Code\python\csv_data\hql\phenotypic_feature\BF'
    count_site_cell_sum(csv_path)