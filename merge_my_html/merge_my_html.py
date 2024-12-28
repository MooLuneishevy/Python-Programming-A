from bs4 import BeautifulSoup
import os
def merge(paths):
    # 检查并创建输出文件夹
    html_folder = 'html'
    if not os.path.exists(html_folder):
        os.mkdir(html_folder)
    # 读取并解析第一个文件
    with open(paths[0], 'r', encoding='utf-8') as file_0:
        html_0 = file_0.read()
    bs_0 = BeautifulSoup(html_0, "html.parser")
    for path in paths[1:]:
        with open(path, 'r', encoding='utf-8') as file_i:
            html_i = file_i.read()
        bs_i = BeautifulSoup(html_i, "html.parser")
        if bs_i.head is not None:
            for tag in bs_i.head.contents:
                bs_0.head.append(tag)
        if bs_i.body is not None:
            for tag in bs_i.body.contents:
                bs_0.body.append(tag)
    output_path = os.path.join(html_folder, 'collection.html')
    with open(output_path, 'w', encoding="utf-8") as f:
        f.write(bs_0.prettify())
    print(f'累计合并 {len(paths)} 个文件，合并成功')