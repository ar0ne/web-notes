# AWS Cloudformation

In `aws` folder you could find several examples of templates for AWS Cloudformation. 

`ec2.yaml` - creates new VPC, public and private subnets, security groups, nacl's, etc.

*Note*: These templates are not for production use, to simplify MongoDB installation I just installed docker on EC2 and run container. As well as there is no any autoscaling groups for instances.

`ecs-db-service.yaml` - creates ECS cluster and run mongodb service.

`ecs-webapp-service.yaml` - runs app's backend service. 

*Note*: To be able to find database host, webapp service has to get public IP of db-service. 
To make it happen, you should upload `.env` file to your S3 bucket and provide ARN of file in properties.

## AWS ECR

- Create docker image for web app:

    `docker build -t webnotes .`

- Create repository in AWS ECR:

    `aws ecr create-repository --repository-name webnotes --region us-east-1`

- Add tag and push your local docker image to ECR:

  - `aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com`
  
  - `docker tag webnotes:latest <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/webnotes:latest`
  
  - `docker push <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/webnotes:latest`

## AWS ECS (Fargate)

- Update required parameters in `vars/db.json`.

- Create stack for cluster and database:

    `aws cloudformation create-stack --stack-name mongodb --template-body file://ecs-db-service.yaml --parameters file://vars/db.json --capabilities CAPABILITY_NAMED_IAM --region us-east-1`

- Update public IP of MongoDB host, username and password and deploy `.env` file to your s3 bucket:

    `aws s3 cp .env s3://<bucket-name>/.env`

- Update parameters in `webapp.json` accordingly.

- Create stack for backend:

`aws cloudformation create-stack --stack-name webnotes --template-body file://ecs-webapp-service.yaml --parameters file://vars/webapp.json --capabilities CAPABILITY_NAMED_IAM --region us-east-1`

#### Clean up:

`aws ecr delete-repository --repository-name webnotes --region us-east-1 --force`

`aws cloudformation delete-stack --stack-name mongodb --region us-east-1`

`aws cloudformation delete-stack --stack-name webnotes --region us-east-1`

## How to run it locally

- activate virtualenv 

- install dependencies \

`pip install -r requirements/dev.txt`

- create `.env` file (see `.env.example`)

- run MongoDB locally or use docker, i.e. `docker-compose up -d`

- run uvicorn (FastAPI) `uvicorn src.main:app --reload` or `./entrypoint.sh`.


# Kubernetes

- install `kubectl`

- decide where you want to run your cluster (e.g. `minikube`)

- push `webnotes:latest` to own Docker hub or AWS ECR

```
docker tag webnotes:latest ar0ne/webnotes:latest
docker push ar0ne/webnotes:latest
```

- `cd deployments` and run `kubectl apply -k ./`

- wait until pods get running (`kubectl get pods`)

- if all right, now you can reach the app with curl. 
For that you need to find port of your service and minikube IP.

```
PORT=$(kubectl get services/webnotes -o go-template='{{(index .spec.ports 0).nodePort}}')
curl http://"$(minikube ip)":$PORT/api/v1/notes/
```

You should get shomething like `{"notes":[]}` if your local database is empty.

Run and try again:

```
curl --request POST \
  --url http://$(minikube ip):$PORT/api/v1/notes/ \
  --header 'Content-Type: application/json' \
  --data '{
	"title": "idea123",
	"body": "myidea"
}'
```

