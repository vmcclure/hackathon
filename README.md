# hackathon
для запуска проекта используем `docker-compose up --build -d`
далее необходимо востановить бд 
`cat dump.sql | docker exec -i hackathon_postgres_1 psql -U postgres` 
(название контейнера может отличаться)
на всякий случай можно перезапустить контейнер `hackaton_rss_1`

#Работа с API
получение списко новостей - `curl --location --request GET 'http://localhost:8001/news'`
доступные query_params - `limit`, `offset`
######
топ 3 новости для роли `curl --location --request GET '127.0.0.1:8001/news/?role=buhgalter&limit=3`
доступные query_params `start_date`, `end_date`, `role`
доступные роли `buhgalter`, `it_director`
добавление новых ролей и тегов возможно через инсерт в бд
###
кластеризация новостей за период `curl --location --request GET '127.0.0.1:8001/best_news?start_date=09102022&end_date=10102022'`
подробное раскрытие кластера `curl --location --request GET '127.0.0.1:8001/best_news?custer_num=1&start_date=09102022&end_date=10102022'`
###
выделенные именованные сущности для выбранной новости `curl --location --request GET '127.0.0.1:8001/news/3/tags_area'`

