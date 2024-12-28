import requests
import parsel
import os
import merge_my_html as mh
# HTML 和 LaTeX 模板
html_str = r'''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <script>
        window.MathJax = { tex: { inlineMath: [['$', '$'], ['\$', '\$']], }, chtml: { scale: 0.8 }};
    </script>
    <script src='https://cdn.jsdelivr.net/npm/mathjax@3.0.1/es5/tex-mml-chtml.js'></script>
</head>
<body>
{article}
</body>
</html>
'''
# 创建文件夹
html_folder = 'html'
if not os.path.exists(html_folder):
    os.mkdir(html_folder)
pages = int(input("请输入要抓取的文章数量: "))
path = []
for i in range(pages):
    # 输入知乎 ID 进行爬取
    zhihu_id = input(f"请输入第 {i+1} 篇文章的知乎 ID: ")
    url = f'https://zhuanlan.zhihu.com/p/{zhihu_id}'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        continue
    selector = parsel.Selector(response.text)
    # 提取标题和正文
    title = selector.css('.Post-Title::text').get()
    content = selector.css('.css-376mun .RichText').get()
    # 处理图片
    img_tags = selector.css('img::attr(src)').getall()
    for img_url in img_tags:
        content = content.replace(f'src="{img_url}"', f'src="{img_url}"')
    # 处理 LaTeX 公式
    formula_tags = selector.css('[data-tex]::attr(data-tex)').getall()
    for formula in formula_tags:
        content = content.replace(f'data-tex="{formula}"', f'${formula}$')
    html_path = os.path.join(html_folder, f"{title}.html")
    with open(html_path, mode='w', encoding='utf-8') as f:
        f.write(html_str.format(title=title, article=content))
    path.append(html_path)
    print(f"{title} 保存成功")
# 合并所有 HTML 文件
mh.merge_my_html.merge(path)
print("所有文章已成功合并为 collection.html")