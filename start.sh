git pull
docker build -t dhruvpatel33343/microservice_user_service:latest ./user_service
docker build -t dhruvpatel33343/microservice_product_service:latest ./product_service
docker build -t dhruvpatel33343/microservice_order_service:latest ./order_service
docker push dhruvpatel33343/microservice_user_service:latest
docker push dhruvpatel33343/microservice_product_service:latest
docker push dhruvpatel33343/microservice_order_service:latest
docker stack rm ecomm
docker stack deploy -c docker-compose.yml ecomm