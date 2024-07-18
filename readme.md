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

docker build -t web-notes .