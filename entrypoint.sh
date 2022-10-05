while !</dev/tcp/db/5432
do sleep 1
done
uvicorn app.server:app --host 0.0.0.0 --port 2137