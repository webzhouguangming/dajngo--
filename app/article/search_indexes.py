from haystack import indexes
from .models import BlogArticle


class BlogArticleIndex(indexes.SearchIndex, indexes.Indexable):
 """
 Article索引数据模型类
 """
 text = indexes.CharField(document=True, use_template=True)

 def get_model(self):
    """返回建⽴索引的模型类"""
    return BlogArticle

 def index_queryset(self, using=None):
    """返回要建⽴索引的数据查询集"""
    return self.get_model().objects.all()