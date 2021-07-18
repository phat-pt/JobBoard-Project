
from employer.models import *

from elasticsearch_dsl import analyzer
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl.connections import connections

# Analyzer for searched term indexing
html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

@registry.register_document
class JobPostDocument(Document):
    
    job_title = fields.CompletionField()
    # Name of the Elasticsearch index
    job_description = fields.TextField(
        analyzer = html_strip,
        fields = {'raw': fields.TextField(), }
    )
    
    
    class Index:
        name = 'jobs'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = JobPost # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = ['ID','job_location','job_salary','job_summary','job_time','company_name','job_type']


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