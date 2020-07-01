import os
import boto3
import curator
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection

ES_HOST = os.environ.get('ES_HOST', 'localhost')
ES_REGION = os.environ.get('ES_REGION', 'us-west-1')
ES_INDICES_PREFIX = os.environ.get('ES_INDICES_PREFIX', 'logs')
ES_INDICES_DATA_RETENTION_THRESHOLD_IN_DAYS = os.environ.get('ES_INDICES_DATA_RETENTION_THRESHOLD_IN_DAYS', '90')
ES_INDICES_DATE_FORMAT = os.environ.get('ES_INDICES_DATE_FORMAT', '%Y.%m.%d')
AWS_SERVICE = "es"


def lambda_handler(event, context):
    """
    Lambda Handler
    """

    # getting credentials
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, ES_REGION, AWS_SERVICE, session_token=credentials.token)

    elasticsearch_client_obj = Elasticsearch(hosts=[{'host': ES_HOST, 'port': 443}],
                                             http_auth=awsauth,
                                             use_ssl=True,
                                             verify_certs=True,
                                             connection_class=RequestsHttpConnection
                                            )

    index_list = curator.IndexList(elasticsearch_client_obj)

    # filter the indices based on the prefix (ES_INDICES_PREFIX).
    index_list.filter_by_regex(kind='prefix',
                               value=ES_INDICES_PREFIX)

    if index_list.indices:
        # filter the logs indices that are ES_INDICES_DATA_RETENTION_THRESHOLD_IN_DAYS days old
        index_list.filter_by_age(source='name',
                                 direction='older',
                                 timestring=ES_INDICES_DATE_FORMAT,
                                 unit='days',
                                 unit_count=int(ES_INDICES_DATA_RETENTION_THRESHOLD_IN_DAYS))

    # check if indices exist
    if index_list.indices:
        curator.DeleteIndices(index_list).do_action()
