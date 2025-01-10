import pandas as pd



def E_standardization(control, drug):
    control_mean = control.mean()
    control_std = control.std()
    single_cell_drug_E_value = (drug-control_mean) / control_std
    single_cell_control_E_value = (control-control_mean) / control_std
    return abs(single_cell_drug_E_value.mean()), single_cell_drug_E_value, single_cell_control_E_value


if __name__ == '__main__':
    # 读取CSV文件
    data_df = pd.read_csv('../data/Ed/hql_H1975_4h_Ed.csv')  # 替换为你的CSV文件路径
    control_E_feature = data_df[data_df['Metadata_treatment'] == 'control']
    drug_E_feature = data_df[data_df['Metadata_treatment'] == 'gefitinib']
    E_value, drug_E_value, control_E_value = E_standardization(control_E_feature['Ed_agg_top_25_value'].values, drug_E_feature['Ed_agg_top_25_value'].values)
    pass