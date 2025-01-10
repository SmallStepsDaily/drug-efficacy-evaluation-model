import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from E_value.pc_standardization import E_standardization


def load_Ed_csv(file_folder_path):
    # 初始化一个空列表，用于存储所有 CSV 文件的数据
    all_data = []

    # 遍历文件夹中的所有文件
    for file_name in os.listdir(file_folder_path):
        # 检查文件是否为 CSV 文件
        if file_name.endswith('.csv'):
            # 构建文件的完整路径
            file_path = os.path.join(file_folder_path, file_name)

            # 读取 CSV 文件
            df = pd.read_csv(file_path)

            # 将数据添加到列表中
            all_data.append(df)

    # 将所有 CSV 文件的数据拼接成一个数据表格
    combined_df = pd.concat(all_data, ignore_index=True)
    return combined_df

def draw_E_value_box(path):
    data_df = load_Ed_csv(path)
    hours = data_df['Metadata_hour'].unique()
    treatments = [treatment for treatment in data_df['Metadata_treatment'].unique() if treatment != 'control']
    result_str = ''
    for hour in hours:
        control_Ed = data_df.loc[
            (data_df['Metadata_hour'] == hour) &  # 筛选 Metadata_hour 等于 hour 的行
            (data_df['Metadata_treatment'] == 'control'),  # 筛选 Metadata_treatment 等于 treatment 的行
            'Ed_agg_top_25_value'  # 选择 Ed_agg_top_25_value 列
        ]

        for treatment in treatments:
            # 筛选数据
            drug_Ed = data_df.loc[
                (data_df['Metadata_hour'] == hour) &  # 筛选 Metadata_hour 等于 hour 的行
                (data_df['Metadata_treatment'] == treatment),  # 筛选 Metadata_treatment 等于 treatment 的行
                'Ed_agg_top_25_value'  # 选择 Ed_agg_top_25_value 列
            ]
            # 采用pc的算法计算E_value值
            E_value, drug_E_value, control_E_value = E_standardization(control_Ed, drug_Ed)
            result_str += f'{hour}h {treatment} 加药组效率表征值为 {E_value}, 注意：该值以单细胞的E_value均值的绝对值求出\n'
            # 将 drug_E_value 赋值到对应的行
            data_df.loc[
                (data_df['Metadata_hour'] == hour) &  # 筛选 Metadata_hour 等于 hour 的行
                (data_df['Metadata_treatment'] == treatment),  # 筛选 Metadata_treatment 等于 treatment 的行
                'E_value'  # 选择 E_value 列
            ] = drug_E_value
            data_df.loc[
                (data_df['Metadata_hour'] == hour) &  # 筛选 Metadata_hour 等于 hour 的行
                (data_df['Metadata_treatment'] == 'control'),  # 筛选 Metadata_treatment 等于 treatment 的行
                'E_value'  # 选择 Ed_agg_top_25_value 列
            ] = control_E_value

    # 按照特征名称（列名）由大到小排序
    data_df_sorted = data_df.sort_index(axis=1, ascending=False)
    data_df_sorted.to_csv(path + "/result.csv", index=False)
    # 创建图形和子图
    fig, ax = plt.subplots(figsize=(12, 6))
    # 绘制图像
    # 设置绘图风格
    sns.set(style="whitegrid", font_scale=1.2)  # 设置全局样式和字体大小
    treatment_order = ['control'] + treatments
    # 绘制箱型图
    sns.boxplot(
        data=data_df_sorted,
        x='Metadata_hour',  # x轴：时间
        y='E_value',  # y轴：Ed_agg_top_25_value的值
        hue='Metadata_treatment',  # 分组：处理类型
        hue_order=treatment_order,
        palette='Set2',  # 颜色主题
        showfliers=True,  # 是否显示异常值
        linewidth=1.5  # 箱型图边框线宽
    )

    # 设置标题和标签
    ax.set_title('E Value Distribution by Hour and Treatment', fontsize=18, pad=20)
    ax.set_xlabel('Hour', fontsize=16, labelpad=10)
    ax.set_ylabel('E Value', fontsize=16, labelpad=10)

    # 显示图例
    plt.legend(title='Treatment', loc='upper right', fontsize=14, title_fontsize=16)

    # 添加刻度线和网格线
    plt.grid(True, linestyle='--', alpha=0.6)  # 添加网格线
    sns.despine(left=False, bottom=False, top=True, right=True)  # 移除上、右轴线，保留左、下轴线

    # 设置刻度线样式
    plt.tick_params(axis='both', which='major', labelsize=14, length=6, width=1.5)

    # 显示图形
    plt.tight_layout()
    plt.savefig(path + "\E_value_result.jpg", dpi=300)
    plt.close()
    # 将字符串保存为 txt 文件
    with open(path + "\\E_value_result.txt", 'w', encoding='utf-8') as file:
        file.write(result_str)

    print(f"文件已保存到: {path}")

def draw_FRET_Efficiency_box(data, feature="Ed_agg_top_25_value"):
    # 创建图形和子图
    fig, ax = plt.subplots(figsize=(12, 6))

    # 定义treatment的顺序，确保control在最左边
    treatment_order = [treatment for treatment in data['Metadata_treatment'].unique() if treatment != 'control']  # 替换为实际的treatment值
    treatment_order = ['control'] + treatment_order

    # 设置绘图风格
    sns.set(style="whitegrid", font_scale=1.2)  # 设置全局样式和字体大小
    # 绘制箱型图
    sns.boxplot(
        data=data,
        x='Metadata_hour',  # x轴：时间
        y=feature,  # y轴：Ed_agg_top_25_value的值
        hue='Metadata_treatment',  # 分组：处理类型
        hue_order=treatment_order,
        palette='Set2',  # 颜色主题
        showfliers=True,  # 是否显示异常值
        linewidth=1.5  # 箱型图边框线宽
    )

    # 设置标题和标签
    ax.set_title('FRET Efficiency Distribution by Hour and Treatment', fontsize=18, pad=20)
    ax.set_xlabel('Hour', fontsize=16, labelpad=10)
    ax.set_ylabel('FRET Efficiency ', fontsize=16, labelpad=10)

    # 显示图例
    plt.legend(title='Treatment', loc='upper right', fontsize=14, title_fontsize=16)

    # 设置y轴刻度线
    plt.yticks(np.arange(0, 0.81, 0.1))  # 从0到0.8，间隔为0.1
    ax.set_ylim(0, 0.8)  # 设置y轴范围

    # 添加刻度线和网格线
    plt.grid(True, linestyle='--', alpha=0.6)  # 添加网格线
    sns.despine(left=False, bottom=False, top=True, right=True)  # 移除上、右轴线，保留左、下轴线

    # 设置刻度线样式
    plt.tick_params(axis='both', which='major', labelsize=14, length=6, width=1.5)

    # 显示图形
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # 定义文件夹路径
    folder_path = r'C:\Code\python\csv_data\hql\efficiency_feature'
    draw_E_value_box(folder_path)