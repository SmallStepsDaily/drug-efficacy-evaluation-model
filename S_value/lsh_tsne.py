import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.spatial.distance import pdist, squareform
from sklearn.manifold import TSNE
import os
import matplotlib
from sklearn.preprocessing import StandardScaler

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
os.environ['LOKY_MAX_CPU_COUNT'] = '4'  # 设置为你机器的实际核心数

def tsne_distance(drug_df, control_df):
    # 合并数据框并添加标签
    merged_df = pd.concat([drug_df.assign(label=1), control_df.assign(label=0)], ignore_index=True)

    # 提取特征数据和标签
    X = merged_df.drop('label', axis=1)
    labels = merged_df['label']

    # 特征归一化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 进行t-SNE降维
    tsne = TSNE(n_components=2, random_state=0)
    X_tsne = tsne.fit_transform(X_scaled)

    # 合并降维坐标和标签
    tsne_df = pd.DataFrame(X_tsne, columns=['x', 'y'])
    tsne_df['label'] = labels

    # 分离drug和control的降维坐标
    drug_tsne = tsne_df[tsne_df['label'] == 1]
    control_tsne = tsne_df[tsne_df['label'] == 0]

    # 计算两类的中心点
    drug_center = drug_tsne[['x', 'y']].mean()
    control_center = control_tsne[['x', 'y']].mean()

    # 计算两个中心点之间的距离l
    l = np.linalg.norm(drug_center - control_center)

    # 计算图像中所有点之间的最大距离d
    points = tsne_df[['x', 'y']].values
    dist_matrix = squareform(pdist(points))
    d = dist_matrix.max()

    # 获取最大距离的索引
    i, j = np.unravel_index(np.argmax(dist_matrix), dist_matrix.shape)

    # 获取这两个点的坐标
    point1 = points[i]
    point2 = points[j]

    # 计算表型表征值
    phenotype_representation = l / d

    # 设置更大的图形大小
    plt.figure(figsize=(10, 8))

    # 画散点图，分别绘制drug和control
    plt.scatter(drug_tsne['x'], drug_tsne['y'], c='#90EE90', label='drug', alpha=0.7)
    plt.scatter(control_tsne['x'], control_tsne['y'], c='#FF5733', label='control', alpha=0.7)

    # 标注两类的中心点
    plt.scatter(drug_center['x'], drug_center['y'], marker='*', s=200, color='red', label='drug center')
    plt.scatter(control_center['x'], control_center['y'], marker='*', s=200, color='#228B22', label='control center')

    # 用红色线连接两个中心点
    plt.plot([drug_center['x'], control_center['x']], [drug_center['y'], control_center['y']], 'r--', label='center distance')

    # 绘制最大距离的直线
    plt.plot([point1[0], point2[0]], [point1[1], point2[1]], 'b--', label='max distance')

    # 在图像下方显示表型表征值
    plt.figtext(0.05, 0.05, f'表型表征值: {phenotype_representation:.4f}', ha='left', fontsize=16)

    # 添加图例，并放在右上角
    plt.legend(loc='upper right')
    # plt.title('t-SNE Visualization with Class Centers and Phenotype Representation')

    # 显示图形
    plt.show()


if __name__ == "__main__":
    # 读取CSV文件
    file_path = r'C:\Code\python\csv_data\hql\phenotypic_feature\Mit\hql_H1975_2h_Mit.csv'
    df = pd.read_csv(file_path)

    # 数据清理
    df.dropna(inplace=True)

    # 提取特征和标签
    metadata_columns = [col for col in df.columns if col.startswith('Metadata_')]
    metadata_columns.extend(['ImageNumber', 'ObjectNumber'])

    # 特征列
    feature_columns = [col for col in df.columns if col not in metadata_columns]

    # 加药组
    d_df = df[df['Metadata_treatment'] == 'osimertinib'][feature_columns]
    d_df['label'] = 1  # 添加数值型标签

    # 对照组
    c_df = df[df['Metadata_treatment'] == 'control'][feature_columns]
    c_df['label'] = 0  # 添加数值型标签

    # 调用函数
    tsne_distance(d_df, c_df)