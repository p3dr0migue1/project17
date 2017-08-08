from haystack import indexes

from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    published_date = indexes.DateTimeField(model_attr='published_date')

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().published.all()
