# How to use locally

1. activate virtualenv
2. install dependencies \
`pip install -r requirements/dev.txt`
3. run mongodb \
e.g. use `docker-compose up -d`)
4. create `.env` file (see `.env.example`)
5. run FastApi \
`uvicorn src.main:app --reload`

# Docker

docker build -t webnotes .

# AWS ECR

1. `aws ecr create-repository --repository-name webnotes --region us-east-1`

2. `aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com`

3. `docker tag webnotes:latest <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/webnotes:latest`

4. `docker push <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/webnotes:latest`