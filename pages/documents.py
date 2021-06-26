from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from employer.models import *
from elasticsearch_dsl import analyzer, tokenizer
from elasticsearch_dsl import FacetedSearch, TermsFacet, DateHistogramFacet

# Analyzer for searched term indexing
my_completion_analyzer = analyzer('my_analyzer',
    tokenizer=tokenizer('trigram', 'edge_ngram', min_gram=3, max_gram=20, token_chars=['letter', 'digit']),
    char_filter=['html_strip'], # remove html entities
    filter=["lowercase", "snowball"]
)

@registry.register_document
class JobPostDocument(Document):
    
    job_title = fields.CompletionField()

    class Index:
        # Name of the Elasticsearch index
        name = 'jobs'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = JobPost # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = ['ID','job_location','job_description','job_salary','job_summary','job_time','company_name','job_type']


# class JobPostDocument(FacetedSearch):
#     doc_types = [JobPost, ]
#     name = 'jobs'

#     job_title = fields.CompletionField()
#     job_location = fields.CompletionField()
#     # fields that should be searched
#     fields = ['ID','job_description','job_salary','job_summary','job_time','company_name','job_type']

#     facets = {
#         # use bucket aggregations to define facets
#         'job_title': TermsFacet(field='job_title'),
#         'job_location': TermsFacet(field='job_location'),
#     }

#     def search(self):
#         # override methods to add custom pieces
#         s = super().search()
#         return s.filter('range', publish_from={'lte': 'now/h'})