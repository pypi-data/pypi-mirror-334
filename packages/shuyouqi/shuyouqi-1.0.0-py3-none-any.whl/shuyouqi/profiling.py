from io import StringIO, BytesIO
import uuid
import json

def check_module_exists(module_name):
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False
    
def build(df, name = '', api_key = '', option = {}):        
    import requests
    import urllib3
    urllib3.disable_warnings()
    #if not check_module_exists('requests'):    
    #    await micropip.install('requests')
    #    import requests
    #if not check_module_exists('pandas'):
    #    await micropip.install('pandas')    
    if not name:
        name = str(uuid.uuid4())    
        
    # 创建示例DataFrame
    '''
    df = pd.DataFrame({
        'Column1': ['A', 'B', 'C'],
        'Column2': [1, 2, 3],
        'Column3': [True, False, True]
    })
    '''
    if 'format' in option and option['format'] == 'excel':
        import pandas as pd
        # 将DataFrame写入内存中的Excel文件
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)
        excel_buffer.seek(0)  # 回到缓冲区的开始
        files = {'file': (name + '.xlsx', excel_buffer.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
    else:
        # 将DataFrame序列化为CSV格式的字符串
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
        csv_buffer.seek(0)  # 移动到文件开头
        files = {'file': (name + '.csv', csv_buffer.getvalue(), 'text/csv;charset=utf-8;')}
    data = {
        'api_key': api_key,
        'option': json.dumps(option)
    }
    # 准备文件上传
    url = "https://erp.juguandian.com/upload"  # 替换为目标URL
    # 发送POST请求
    response = requests.post(url, files=files, data = data)

    # 处理响应
    if response.status_code == 200 and response.text.endswith('.html'):
        return 'https://erp.juguandian.com/upload/' + response.text
    else:
        raise ValueError(response.text)