set Compose_File=docker-compose.yaml
set Compose_Project_Name=campusmarket

docker-compose -f %Compose_File% -p %Compose_Project_Name% build
docker-compose -f %Compose_File% -p %Compose_Project_Name% up
