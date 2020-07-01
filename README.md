# Elasticsearch Curator Lambda

## Overview
This repository contains the manifest for the elasticsearch curator lamdba.

## Details

1. Build and package this project by following these commands, so that it deployed on lambda:

```bash

sudo pip3 install virtualenv 

# i have used python3.7, other versions can also be used that are supported by lambda
virtualenv -p python3.7 v-env

# activate the virtual environment
source v-env/bin/activate


# install packages
pip3 install -r requirements.txt

# deactivate the virtual environment
deactivate

# move inside virtual environment's packages section
cd v-env/lib/<python-version>/site-packages

# archive the library contents
zip -r9 ${OLDPWD}/elasticsearch-curator-lambda.zip .

# move back to the directory
cd $OLDPWD

# add the lambda function code to the archive
zip -g elasticsearch-curator-lambda.zip lambda_function.py

```

2. Upload the archive save it, there are two ways to do it

    1. direct upload(not recommended)
    2. upload to s3 and specify the path in the lambda.
    3. [zappa](https://github.com/Miserlou/Zappa)

3. Following environment variables can be configured on AWS Lambda:

| Environment Variable | Description | Default Value |
|---|---|---|
| ES_HOST | Elasticsearch URL without `https//` | localhost |
| ES_RESION | Elasticsearch cluster reason | us-west-1 |
| ES_INDICES_DATA_RETENTION_DAYS_THRESHOLD | Data retention period in days. | 90 |
| ES_INDICES_PREFIX_TO_BE_DELETED | Indices prefix, it will be used as **`first`** filter, it will filter all the indices that have this prefix in their name. The remaining indices name will be filtered based on the age filter ES_INDICES_DATE_FORMAT. The reason to do these two filters is that we don't want to delete | logs |
| ES_INDICES_DATE_FORMAT | Date format in the indices name. Indices will be filtered if their date is older than ES_INDICES_DATA_RETENTION_DAYS_THRESHOLD | %Y.%m.%d |
