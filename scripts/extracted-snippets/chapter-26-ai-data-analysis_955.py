# Source: chapter-26-ai-data-analysis.md
# Lines: 955-1028
# Language: python

import pandas as pd
import numpy as np

def auto_clean_dataframe(df, report=True):
    """
    自动清洗DataFrame
    
    参数：
        df: 输入的DataFrame
        report: 是否返回清洗报告
    
    返回：
        cleaned_df: 清洗后的DataFrame
        report: 清洗报告（如果report=True）
    """
    original_shape = df.shape
    cleaning_log = []
    
    # 1. 删除完全重复的行
    df = df.drop_duplicates()
    cleaning_log.append(f"删除重复行: {original_shape[0] - df.shape[0]} 行")
    
    # 2. 处理缺失值
    for col in df.columns:
        missing_count = df[col].isnull().sum()
        if missing_count > 0:
            if df[col].dtype in ['int64', 'float64']:
                # 数值型：用中位数填充
                fill_value = df[col].median()
                df[col].fillna(fill_value, inplace=True)
                cleaning_log.append(f"列 '{col}': 用中位数 {fill_value:.2f} 填充 {missing_count} 个缺失值")
            else:
                # 类别型：用众数填充
                mode_value = df[col].mode()
                if not mode_value.empty:
                    df[col].fillna(mode_value[0], inplace=True)
                    cleaning_log.append(f"列 '{col}': 用众数 '{mode_value[0]}' 填充 {missing_count} 个缺失值")
    
    # 3. 处理异常值（3-sigma原则）
    for col in df.select_dtypes(include=[np.number]).columns:
        mean = df[col].mean()
        std = df[col].std()
        lower_bound = mean - 3 * std
        upper_bound = mean + 3 * std
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col].count()
        if outliers > 0:
            df[col] = df[col].clip(lower_bound, upper_bound)
            cleaning_log.append(f"列 '{col}': 裁剪 {outliers} 个异常值到 [{lower_bound:.2f}, {upper_bound:.2f}]")
    
    # 4. 标准化列名
    original_columns = df.columns.tolist()
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
    if list(df.columns) != original_columns:
        cleaning_log.append(f"标准化列名: {original_columns} → {list(df.columns)}")
    
    if report:
        cleaning_report = {
            'original_shape': original_shape,
            'final_shape': df.shape,
            'rows_removed': original_shape[0] - df.shape[0],
            'cleaning_log': cleaning_log
        }
        return df, cleaning_report
    
    return df

# 使用示例
# cleaned_df, report = auto_clean_dataframe(df)
# print(f"清洗前: {report['original_shape']}, 清洗后: {report['final_shape']}")
# for log in report['cleaning_log']:
#     print(f"  - {log}")
