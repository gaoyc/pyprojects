"""
利用Python和goagent代理爬取1024帖子所有图片

"""
import urllib.request
import re
import os


def download(html_url):
    # 打开页面返回源代码
    img_html = urllib.request.urlopen(html_url).read().decode('gb2312', 'ignore')

    # 创建文件夹
    folder_name = re.findall('<h4>(.+)</h4>', img_html)[0].replace('|', '&').replace('/', '&').replace('\\',
                                                                                                       '&').replace('?',
                                                                                                                    '？').replace(
        ':', '：')

    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        print('创建文件夹:', folder_name)
    os.chdir(folder_name)

    # 把页面地址信息写入txt
    with open('页面地址.txt', 'w') as j:
        j.write(html_url)
        j.close()
        print('已保存页面地址到文本')

    # 获取图片url列表
    img_url_list = re.findall("<input type='image' src='(http[^']+\.(?:jpg|jpeg|png|gif))", img_html)
    # print(img_url_list)

    # 储存图片
    img_name = 0

    for each in img_url_list:

        img_name += 1

        if not os.path.exists('%d' % img_name + '.jpg'):

            try:
                img = urllib.request.urlopen(each).read()

                print('正在保存第', img_name, '张图片:', each)

                with open('%d' % img_name + '.jpg', 'wb') as f:
                    f.write(img)

            except:
                print('图片地址失效！')

        else:
            print('图片已存在')

    print('帖子:' + folder_name + '#图片下载完毕#' + '\n')


def main():
    # 创建and进入子文件夹：“社会主义核心价值观”
    if not os.path.exists('社会主义核心价值观'):
        os.mkdir('社会主义核心价值观')

    os.chdir('社会主义核心价值观')

    # 安装代理opener
    proxies = urllib.request.ProxyHandler(
        {'http': '127.0.0.1:8087', 'https': '127.0.0.1:8087'})  # 此处为代理地址和端口号，需要根据自己的情况自行设置
    opener = urllib.request.build_opener(proxies)
    urllib.request.install_opener(opener)

    # 运行函数
    html_url = input('请输入帖子地址:')
    download(html_url)


if __name__ == '__main__':
    main()
