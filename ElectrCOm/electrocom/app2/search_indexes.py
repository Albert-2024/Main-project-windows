from haystack import indexes
from app2.models import Book

class BookIndex(indexes.SearchIndex,indexes.Indexable):
    text=indexes.CharField(document=True,use_template=True,template_name="search/book_text.txt")
    title=indexes.CharField(model_attr='title')
    authors=indexes.CharField()

    def get_model(self):
        return Book
    
    def prepare_authors(self,obj):
        return [ author.name for a in obj.authors.all()]