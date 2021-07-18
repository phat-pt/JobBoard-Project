
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from employer.models import *
from elasticsearch_dsl import analyzer, tokenizer
from django.contrib.auth.models import User
from applicant.models import Profile

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

@registry.register_document
class ProfileDocument(Document):
    # Name of the Elasticsearch index
    skill = fields.TextField(
        analyzer = html_strip,
        fields = {'raw': fields.TextField(), }
    )
    class Index:
        
        # Name of the Elasticsearch index
        name = 'applicants'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}


    class Django:
        model = Profile # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = ['id','tag_line','location']