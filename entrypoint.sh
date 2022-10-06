while !</dev/tcp/db/3306
do sleep 1
done
uvicorn app.server:app --host 0.0.0.0 --port 2137