
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from employer.models import *
from elasticsearch_dsl import analyzer, tokenizer
from django.contrib.auth.models import User
from applicant.models import Profile

# Analyzer for searched term indexing
my_completion_analyzer = analyzer('my_analyzer',
    tokenizer=tokenizer('trigram', 'edge_ngram', min_gram=3, max_gram=20, token_chars=['letter', 'digit']),
    char_filter=['html_strip'], # remove html entities
    filter=["lowercase", "snowball"]
)

@registry.register_document
class ProfileDocument(Document):
    
    tag_line = fields.CompletionField()
    location = fields.CompletionField()

    class Index:
        # Name of the Elasticsearch index
        name = 'applicants'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Profile # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = ['id','skill']