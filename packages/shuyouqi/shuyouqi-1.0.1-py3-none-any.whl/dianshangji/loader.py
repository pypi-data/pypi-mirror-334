import pandas
import pyodide
import micropip

font = None
async def init():
    global font
    await micropip.install("/pypi/et_xmlfile-2.0.0-py3-none-any.whl")
    await micropip.install("/pypi/openpyxl-3.1.5-py2.py3-none-any.whl")
    await micropip.install("/pypi/pyfonts-0.0.2-py3-none-any.whl")
    from pyfonts import load_font
    #print("开始初始化数据分析和可视化的运行环境,请稍候……")
    # 文件的URL
    file_url = '/assets/fonts/NotoSansSC-Regular.ttf'  # 请将此URL替换为实际文件的URL
    # 本地保存路径
    local_file_path = '/NotoSansSC-Regular.ttf'
    # 下载文件并保存到本地
    try:
        response = await pyodide.http.pyfetch(file_url)
        # Return the response body as a bytes object
        image_data = await response.bytes()
        with open(local_file_path, 'wb') as f:
            f.write(image_data)
        print(f"中文字体文件: {local_file_path}")
    except Exception as e:
        print(f"下载文件时出错: {e}")

    font = load_font(font_path="/NotoSansSC-Regular.ttf")
    #print(font)
    #print("数据分析和可视化的运行环境已经就绪。可以进行第1步了。")
    return font
    
def get_font():
    global font
    return font    