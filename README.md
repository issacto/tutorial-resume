# Tutorial Resume (in traditional chinese)

* Aims: A simple one-page website about my tutorial services
* Tools : Docker, Flask, Aws Dynamo, Bootstrap

### Run the progarm:
Change to CMD ["flask", "run"] on the last line  of the Dockerfile
```
docker-compose up -d --build
```
Open localhost:5000 on browser

### Deploy the program:
```
heroku container:push web
heroku container:release web
heroku open
```

