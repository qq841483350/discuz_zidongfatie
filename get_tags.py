#coding:utf8
import requests,re
def get_tags(subject="帖子标题"):
    tags_url="http://www.aixihuabbs.com/forum.php?mod=relatekw&subjectenc=%s"%subject
    html=requests.get(tags_url).content

    if """tags""" in html:
        tags=re.findall('var inssplit = "([\s\S]*?)";\s+var returnsplit',html)[0]
        return tags
    else:
        tags=''
        return tags
if __name__=="__main__":
    subject="seo搜索引擎是什么意思"
    get_tags(subject)