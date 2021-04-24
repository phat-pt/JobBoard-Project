from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from pages.models import JobPost


@registry.register_document
class JobPostDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'jobs'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = JobPost # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = ['job_location', 'job_apply_url', 'is_active','ID','job_description',
        'job_salary','job_summary','job_time','job_title','company_name','company_url','job_type']