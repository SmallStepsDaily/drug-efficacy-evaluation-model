
import numpy as np
import pandas as pd
from scipy.spatial.distance import jensenshannon
from scipy.stats import gaussian_kde

def js_divergence(control, drug, draw=False):
    # 删除小于0.05的值
    control = control[control >= 0]
    drug = drug[drug >= 0]

    # 检查过滤后的数据
    print("control过滤后的数据量:", len(control))
    print("drug过滤后的数据量:", len(drug))

    # 计算概率密度函数（PDF）
    def compute_pdf(data, x_range):
        kde = gaussian_kde(data)
        pdf = kde(x_range)
        return pdf / pdf.sum()  # 归一化

    # 定义x轴范围（根据数据范围动态调整）
    x_range = np.linspace(min(min(control), min(drug)), max(max(control), max(drug)), 1000)

    # 计算两个类别的概率分布
    pdf_control = compute_pdf(control, x_range)
    pdf_drug = compute_pdf(drug, x_range)

    # 计算JS散度
    js_divergence_value = jensenshannon(pdf_control, pdf_drug, base=2)  # base=2表示结果在[0, 1]之间
    if draw:
        draw_plt(x_range, pdf_control, pdf_drug)
    print(f"JS散度: {js_divergence_value:.4f}")
    return js_divergence_value


def draw_plt(x_range, pdf_control, pdf_drug):
    # 可视化两个分布
    import matplotlib.pyplot as plt

    plt.plot(x_range, pdf_control, label='control')
    plt.plot(x_range, pdf_drug, label='gefitinib')
    plt.yticks([])  # 隐藏y轴刻度标签
    plt.xlabel('Feature Value')
    plt.ylabel('Probability Density')
    plt.title('Probability Distribution of Two Treatments')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    # 读取CSV文件
    data = pd.read_csv(r'D:\data\hql\2024.10.21 g o c 1vs3\Ed_features.csv')  # 替换为你的CSV文件路径
    # 时间
    data = data[data['Metadata_hour'] == 2]
    # 根据metadata_treatment进行分类
    treatment_1 = data[data['Metadata_treatment'] == 'control']  # 替换为实际的treatment值
    # gefitinib osimertinib
    treatment_2 = data[data['Metadata_treatment'] == 'gefitinib']  # 替换为实际的treatment值

    # 提取需要分析的列（假设为'feature_column'）
    feature_1 = treatment_1['Ed_agg_top_25_value'].values  # 替换为实际的列名
    feature_2 = treatment_2['Ed_agg_top_25_value'].values  # 替换为实际的列名
    js_divergence(feature_1, feature_2)