Команда для сборки образа:
docker build <директория, где лежит Dockerfile> -t <имя образа>

Команда для запуска образа:
docker run --name <имя контейнера> -p <порт хоста>:<порт контейнера> <имя образа>

