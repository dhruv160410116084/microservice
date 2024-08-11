git pull
docker build -t dhruvpatel33343/microservice_user_service:latest ./user_service
docker build -t dhruvpatel33343/microservice_product_service:latest ./product_service
docker build -t dhruvpatel33343/microservice_order_service:latest ./order_service
docker push dhruvpatel33343/microservice_user_service:latest
docker push dhruvpatel33343/microservice_product_service:latest
docker push dhruvpatel33343/microservice_order_service:latest
docker stack rm ecomm
docker stack deploy -c docker-compose.yml ecomm



kuberntes
gcloud container clusters create  app --zone us-central1-a --num-nodes 2 --machine-type e2-medium --disk-size 10GB
kubectl create secret docker-registry my-registry-secret --docker-server=https://index.docker.io/v1/ --docker-username=dhruvpatel33343 --docker-password=Dhruv@33343 --docker-email=dhruvnpatel289@gmail.com


kubectl delete deployments --all 
kubectl delete services --all 
kubectl delete pvc --all 
kubectl delete pv --all

kubectl apply -f user_service/configmap.yaml
kubectl apply -f user_service/postgre-pvc-claim.yaml
kubectl apply -f user_service/deployment-postgresql.yaml
kubectl apply -f user_service/deployment.yaml
kubectl apply -f product_service/deployment.yaml
kubectl apply -f order_service/deployment.yaml
