#  Time Attendance Monitoring (TAM) Application
#  To Run the project 
## Prerequisites

- install Docker and docker compose
- run `docker-compose up --build --remove-orphans`
- in separate terminal run `sudo docker exec -it core bash`
- in the docker shell run `python manage.py makemigrations`
- then ` python manage.py migrate`
- then ` python manage.py createsuperuser`
- for give permission `sudo chown -R $USER:$USER .`


### Postman Test setup COde

```
const loginResponse = JSON.parse(responseBody);
pm.environment.set("ACCESS_TOKEN", loginResponse.data.access);
```