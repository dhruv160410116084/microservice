docker-compose up --build
docker-compose down -v 

docker swarm init #manager node
docker swarm join --token SWMTKN-1-xxxxxxxxx <manager-ip>:2377 # worker node

docker node update --label-add role=manager aflu8t9b8i445qfz4usull7sd
docker node update --label-add role=worker x7i6lbnu5hztckury7uyg3cf6
docker node ls

git clone https://github.com/dhruv160410116084/microservice
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
kubectl delete configmaps postgres-init-script

kubectl apply -f user_service/configmap.yaml
kubectl apply -f user_service/postgre-pvc-claim.yaml
kubectl apply -f user_service/deployment-postgresql.yaml
kubectl apply -f user_service/deployment.yaml
kubectl apply -f product_service/deployment.yaml
kubectl apply -f order_service/deployment.yaml


helm upgrade --install postgres ./user_service/postgres/ --namespace default
helm upgrade --install user-service ./user_service/user-service/ --namespace default
helm upgrade --install product-service ./product_service/product-service/ --namespace default
helm upgrade --install order-service ./order_service/order-service/ --namespace default


argocd login 34.136.107.14 --username admin --password vig3SIKZbfznM1Xi


argocd app create postgresql 
  --repo https://github.com/dhruv160410116084/microservice 
  --path  user_service/postgres 
  --dest-server https://kubernetes.default.svc 
  --dest-namespace default 
  --helm-set image.tag=latest 
  --sync-policy automated


argocd app create user-service 
  --repo https://github.com/dhruv160410116084/microservice 
  --path user_service/user-service 
  --dest-server https://kubernetes.default.svc 
  --dest-namespace default 
  --helm-set image.tag=latest 
  --sync-policy automated

argocd app create product-service 
  --repo https://github.com/dhruv160410116084/microservice 
  --path product_service/product-service 
  --dest-server https://kubernetes.default.svc 
  --dest-namespace default 
  --helm-set image.tag=latest 
  --sync-policy automated

argocd app create order-service 
  --repo https://github.com/dhruv160410116084/microservice 
  --path order_service/order-service 
  --dest-server https://kubernetes.default.svc 
  --dest-namespace default 
  --helm-set image.tag=latest
  --sync-policy automated





