sudo az login --use-device-code
sudo az acr login --name campusmarket
sudo docker-compose build
sudo docker push campusmarket.azurecr.io/campusmarket-frontend:latest
sudo docker push campusmarket.azurecr.io/campusmarket-backend:latest
