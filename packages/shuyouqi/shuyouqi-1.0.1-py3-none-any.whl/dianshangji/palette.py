# color
import colorsys

color_text = '''#f9c1ce,赫尔莫萨粉,Hermosa Pink
#f8b6ba,科林斯粉,Corinthian Pink
#e0b3b6,卡梅欧粉,Cameo Pink
#d1b0a7,小鹿色,Fawn
#b59392,浅棕色,Light Brown Drab
#f58e84,珊瑚红,Coral Red
#f6917e,新鲜色,Fresh Color
#f48067,格拉纳丁粉,Grenadine Pink
#f37f94,玫瑰粉,Eosine Pink
#f27291,锆红,Spinel Red
#d46d7a,古老玫瑰色,Old Rose
#e2625e,优金尼亚红-A,Eugenia Red-A
#da525d,优金尼亚红-B,Eugenia Red-B
#bb7125,生土黄,Raw Sienna
#c56127,葡萄酒黄褐色,Vinaceous Tawny
#eb5324,玛瑙红,Jasper Red
#e31f26,光谱红,Spectrum Red
#dd4027,红橙色,Red Orange
#c55347,伊特鲁里亚红,Etruscan Red
#ae5224,焚烧土黄,Burnt Sienna
#ab544d,赭红色,Ochre Red
#cb2f43,猩红色,Scarlet
#cc1236,绯红,Carmine
#c53c69,印度湖,Indian Lake
#b73f74,罗索兰紫,Rosolanc Purple
#b71f57,石榴紫,Pomegranite Purple
#a94151,绣球红,Hydrangea Red
#a84222,砖红色,Brick Red
#a62c37,绯红色,Carmine Red
#ab2439,庞贝红,Pompeian Red
#a72144,红色,Red
#7c4226,棕色,Brown
#793327,干草色,Hay's Russet
#82241f,范迪克红,Vandyke Red
#7d133a,紫罗兰紫,Pansy Purple
#802626,浅烧湖色,Pale Burnt Lake
#642d5e,紫红色,Violet Red
#6d4145,维斯托里斯湖色,Vistoris Lake
#f5ecc2,硫磺黄,Sulpher Yellow
#ffefae,浅柠檬黄,Pale Lemon Yellow
#fbe6a0,那不勒斯黄,Naples Yellow
#ebd3a2,象牙色,Ivory Buff
#fdd4bd,海贝粉,Seashell Pink
#fcc79b,浅粉肉桂色,Light Pinkish Cinnamon
#eeb480,粉肉桂色,Pinkish Cinnamon
#fdc57e,肉桂色,Cinnamon Buff
#fdbf68,奶油黄,Cream Yellow
#f3a257,金黄色,Golden Yellow
#eea78c,葡萄肉桂色,Vinaceous Cinnamon
#d8a37b,赭红色三文鱼,Ochraceous Salmon
#c5a56e,伊莎贝拉色,Isabella Color
#c59f6b,枫木色,Maple
#c1c494,橄榄色,Olive Buff
#c2ae93,厚棕色,Ecru
#fff200,黄色,Yellow
#f8ed43,柠檬黄,Lemon Yellow
#ffdd00,杏黄色,Apricot Yellow
#cab356,黄铁矿黄,Pyrite Yellow
#d6b43e,橄榄赭色,Olive Ocher
#e2b540,黄赭色,Yellow Ocher
#fcb315,橙黄色,Orange Yellow
#f99d1b,黄橙色,Yellow Orange
#f68c50,杏橙色,Apricot Orange
#f37420,橙色,Orange
#f15a30,桃红色,Peach Red
#d96629,英国红,English Red
#c27544,肉桂红褐色,Cinnamon Rufous
#c16b27,橙红褐色,Orange Rufous
#c19f2c,硫磺黄,Sulphine Yellow
#bc892b,卡其色,Khaki
#b2b73e,柠檬黄,Citron Yellow
#b09f36,黄水晶色,Citrine
#96874d,淡黄水晶色,Buffy Citrine
#8b835b,深黄水晶色,Dark Citrine
#848061,浅灰橄榄色,Light Grayish Olive
#84875e,克朗贝格绿,Krongbergs Green
#837e31,橄榄色,Olive
#986f2d,橙黄水晶色,Orange Citrine
#a36752,苏丹棕色,Sudan Brown
#6b7140,橄榄绿,Olive Green
#806e4b,浅棕橄榄色,Light Brownish Olive
#635a3a,深灰橄榄色,Deep Grayish Olive
#71502f,浅生赭色,Pale Raw Umber
#644b1e,褐色,Sepia
#762c19,茜草棕,Madder Brown
#653514,火星棕烟草色,Mars Brown Tobacco
#4b3317,范迪克棕,Vandyke Brown
#b5decc,绿松石绿,Turquoise Green
#b4cdc2,苍绿色,Glaucous Green
#b7c2a9,深绿苍色,Dark Greenish Glaucous
#afd472,黄绿色,Yellow Green
#c7d14f,浅绿色黄,Light Green Yellow
#87c540,夜绿,Night Green
#a6a159,橄榄黄,Olive Yellow
#709390,艾草绿,Artemesia Green
#6d7e77,安多佛绿,Andover Green
#8fa071,雨蛙绿,Rainette Green
#719470,铬绿,Chromium Green
#648f7b,开心果绿,Pistachio Green
#00b49b,海绿色,Sea Green
#00978d,苯绿色,Benzol Green
#00908a,浅瓷绿色,Light Porcelain Green
#489b6e,绿色,Green
#009465,暗绿,Dull Viridian Green
#819238,油绿色,Oil Green
#1a7444,二胺绿,Diamine Green
#437742,哥萨克绿,Cossack Green
#555832,林肯绿,Lincoln Green
#42533e,黑橄榄色,Blackish Olive
#253122,深石板橄榄色,Deep Slate Olive
#bce4e5,尼罗蓝,Nile Blue
#a7d4e4,浅国王蓝,Pale King's Blue
#a5c8d1,浅灰蓝,Light Glaucous Blue
#97acc8,鼠尾草蓝,Salvia Blue
#96d1aa,钴绿,Cobalt Green
#78cdd0,锌蓝,Calamine BLue
#62c6bf,威尼斯绿,Venice Green
#0093a5,天青蓝,Cerulian Blue
#00939b,孔雀蓝,Peacock Blue
#099197,绿蓝色,Green Blue
#5a82b3,奥林匹克蓝,Olympic Blue
#006eb8,蓝色,Blue
#007190,安特卫普蓝,Antwarp Blue
#005b8d,瑞士蓝,Helvetia Blue
#547076,深梅迪奇蓝,Dark Medici Blue
#004f46,昏暗绿色,Dusky Green
#1c4286,深里昂蓝,Deep Lyons Blue
#40456a,紫蓝色,Violet Blue
#064f6e,瓦尔达·波尔蓝,Vandar Poel's Blue
#12354e,深泰利安蓝,Dark Tyrian Blue
#1e0e3f,暗紫黑,Dull Violet Black
#051230,深靛蓝,Deep Indigo
#112f2c,深石板绿,Deep Slate Green
#b5b1d8,灰熏紫-A,Grayish Lavender-A
#c0a9b3,灰熏紫-B,Grayish Lavender-B
#ca92a8,莱丽亚粉,Laelia Pink
#b984af,丁香色,Lilac
#bf5892,贯叶金莲花紫,Eupatorium Purple
#9a72aa,浅紫红色,Light Mauve
#a36aa5,乌头紫,Aconite Violet
#80719e,暗蓝紫色,Dull Blue Violet
#66629c,深柔紫色,Dark Soft Violet
#6450a1,蓝紫色,Blue Violet
#84565b,紫褐色,Purple Drab
#70727c,深紫色 / 铅色,Deep Violet / Plumbeous
#8c4c62,维罗尼亚紫,Veronia Purple
#704357,深石板紫,Dark Slate Purple
#7a4456,褐灰色,Taupe Brown
#713b4c,紫绯色,Violet Carmine
#4f4086,紫色,Violet
#59256a,红紫色,Red Violet
#501345,孔雀紫,Cotinga Purple
#4e1d4c,昏暗茜草紫,Dusky Madder Violet
#ffffff,白色,White
#b6bfc1,中性色灰,Neutral Gray
#a2b0ad,矿物灰,Mineral Gray
#a1a39a,暖灰色,Warm Gray
#34454c,石板色,Slate Color
#111314,黑色,Black'''

def hex_to_rgb(hex_color):
    """将十六进制颜色值转换为RGB元组"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """将RGB颜色值转换为十六进制"""
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))

def get_hue(rgb):
    """从RGB元组计算色调(Hue)"""
    hue, _, _ = colorsys.rgb_to_hsv(*rgb)
    return hue

def sort_by_hue(two_d_list):
    """根据第一个元素（颜色值）的色调对二维列表进行排序"""
    return sorted(two_d_list, key=lambda x: get_hue(hex_to_rgb(x[0])))

color_table = sort_by_hue([color.split(',') for color in color_text.split('\n')])

#print(color_table)

def color_names(lang = 'cn'):
    return [color[1] if lang == 'cn' else color[2] for color in color_table]
        
def color_picker(color_name, color_number = 5, hex_only = False):
    primary_index = 0
    for row_index, row in enumerate(color_table):
        if color_name == row[1] or color_name == row[2]:
            primary_index = row_index
            break
    segment = round(len(color_table) / color_number)
    color_values = []
    color_total = len(color_table)
    for i in range(0, color_number):
        if hex_only:            
            color_values.append(color_table[(i * segment + primary_index) % color_total][0])        
        else:
            color_values.append(color_table[(i * segment + primary_index) % color_total])        

    return color_values

def set_saturation(hex_color, new_s):
    """根据给定的十六进制颜色值，返回饱和度为100%的新颜色值"""
    # 转换为RGB
    r, g, b = hex_to_rgb(hex_color)
    
    # 调整饱和度到100%
    new_rgb = adjust_saturation_from_rgb((r, g, b), new_s)
    
    # 返回新的十六进制颜色值
    return rgb_to_hex(new_rgb)

def set_brightness(hex_color, new_v):
    """根据给定的十六进制颜色值，返回亮度为100%的新颜色值"""
    # 转换为RGB
    r, g, b = hex_to_rgb(hex_color)
    
    # 调整饱和度到100%
    new_rgb = adjust_brightness_from_rgb((r, g, b), new_v)
    
    # 返回新的十六进制颜色值
    return rgb_to_hex(new_rgb)

def adjust_saturation_from_rgb(rgb, new_s = 1.0):
    """从RGB三元组开始调整饱和度到100%"""
    # 将RGB转换为HSV
    h, s, v = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2] )
    
    # 将饱和度设置为1（即100%）
    # new_s = 1.0
    
    # 根据新的HSV值获取RGB值
    new_rgb = colorsys.hsv_to_rgb(h, new_s, v)
    
    return new_rgb[0], new_rgb[1], new_rgb[2]

def adjust_brightness_from_rgb(rgb, new_v = 1.0):
    """从RGB三元组开始调整饱和度到100%"""
    # 将RGB转换为HSV
    h, s, v = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2] )
    
    # 将饱和度设置为1（即100%）
    # new_s = 1.0
    
    # 根据新的HSV值获取RGB值
    new_rgb = colorsys.hsv_to_rgb(h, s, new_v)
    
    return new_rgb[0], new_rgb[1], new_rgb[2]

def color_plot(colors):    
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    # 示例颜色列表，格式为 #ababab    
    if isinstance(colors[0], list) and len(colors[0]) == 3:
        colors = [color[0] for color in colors]
        
    # 创建图像和轴
    fig, ax = plt.subplots()

    # 设置每个颜色块的宽度和高度
    width = 100
    height = 10

    # 绘制每个颜色块
    for i, color in enumerate(colors):
        y_position = i * height  # 每个新块在前一个之下，因此乘以i
        rect = patches.Rectangle((0, y_position), width, height, color=color)
        ax.add_patch(rect)

    # 设置坐标轴范围
    ax.set_xlim(0, width)
    ax.set_ylim(0, len(colors) * height)

    # 移除坐标轴显示
    ax.axis('off')

    plt.show()
    
def color_plotall():
    color_plot([color[0] for color in color_table])