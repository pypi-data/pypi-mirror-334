import pandas as pd
import re
from collections import defaultdict

# 处理月销量字段的函数
def clean_month_sales(sales_str):   
    if pd.isna(sales_str):
        return None
    
    sales_str = str(sales_str).strip()
    
    # 根据不同的格式估算月销量
    if "本月行业热销" in sales_str:
        return 1000
    elif "万+" in sales_str:
        match = re.search(r'(\d+)', sales_str)
        if match:
            return int(match.group(1)) * 10000  # 假设每万+表示的销量为数字乘以10000
    elif "+人" in sales_str:
        match = re.search(r'(\d+)', sales_str)
        if match:
            return int(match.group(1))  # 假设+人后跟的是具体的销量数字
    
    try:
        return int(sales_str)  # 尝试将字符串转为整数
    except ValueError:
        return None


def process_data(df, field_id = '商品ID', field_x = '价格', field_y = '月销量', field_attribute = '属性', max_x = 1000, max_y = 10000):
    df['月销量'] = df['月销量'].apply(clean_month_sales)      
    # 筛选出“价格”小于等于1000元的记录
    df = df[df[field_x] <= max_x]
    #print("筛选出“价格”小于等于1000元的记录")
    #print(df.head(5))

    # 筛选出“属性”存在的记录
    df = df[df[field_attribute].apply(lambda x: isinstance(x, str))]

    # 筛选出“月销量”大于等于0，小于等于5000的记录
    df = df[df[field_y].apply(lambda x: (0 <= x <= max_y))]
    #print("筛选出“月销量”小于等于5000的记录")
    #print(df.head(5))  

    # 检查商品ID是否有重复记录
    if df[field_id].duplicated().any():
        #print("存在重复的商品ID记录，正在去除重复条目...")
        df = df.drop_duplicates(subset=[field_id], keep='first')
    #else:
        #print("没有重复的商品ID记录。")

    # 打印前5条记录以检查结果
    #print(df.head(5))

    #print("有效记录总数：", len(df))
    return df

def process_attribute(df, field_attribute = '属性'):
    # 使用defaultdict来存储结果，使得可以自动处理不存在的键
    attribute_dict = defaultdict(set)

    attribute_weight = {}

    data = df[field_attribute]

    attributes = {}
    
    for line in data:
        if not isinstance(line, str):
            continue
        # 按照'|'分割每一行    
        items = line.split('|')
        for item in items:
            if item.find(':') > 0:
                key, value = item.split(':')
            else:
                key = field_attribute
                value = item
                item = key + ':' + value
            attribute_dict[key].add(value)        
            if item in attribute_weight:
                attribute_weight[item] += 1
            else:
                attribute_weight[item] = 1			
    
    for key, values in attribute_dict.items():
        sorted_values = sorted(values, key=lambda x: 0-attribute_weight[key + ':' + x])
        attributes[key] = sorted_values
    
    return attributes
