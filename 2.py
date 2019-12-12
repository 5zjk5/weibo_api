from weibopy import WeiboOauth2, WeiboClient
import webbrowser
import time
import re
import jieba
import wordcloud


client_key = '' # 你的 app key
client_secret = '' # 你的 app secret
redirect_url = 'https://api.weibo.com/oauth2/default.html'
auth = WeiboOauth2(client_key, client_secret, redirect_url)
# 获取认证 code
webbrowser.open_new(auth.authorize_url)
code = input('输入 code:')
# 使用 code 获取 token
token = auth.auth_access(code)
# token 是刚刚获得的 token，可以一直使用
client = WeiboClient(token['access_token'])

comment_text_list = [] # 保存所有评论正文


# 共获取 10 页 * 每页最多 200 条评论
for i in range(1, 11):
    result = client.get('comments/show.json', params={'id': 4448468472919660, 'count': 200,})

    comments = result['comments']
    if not len(comments):
        break

    for comment in comments:
        text = re.sub('回复.*?:', '', str(comment['text']))
        comment_text_list.append(text)
        print(text)

    print('已抓取评论 {} 条'.format(len(comment_text_list)))
    time.sleep(1)



# 读取文本内容
txt = ''.join(comment_text_list)

# 处理成一个个词汇
ls = jieba.lcut(txt)
txt = ' '.join(ls)

# 词云生成
w = wordcloud.WordCloud(background_color='white',
                        width=1000, height=700,
                        font_path='msyh.ttc',
                        max_words=200)
w.generate(txt)
w.to_file('comments.png')








