# Volunteer Manager

## Description
Volunteer management software made for R Systems Hackaton

## Test and Deploy

```
build container:
./docker.sh

build locally:
uvicorn app.server:app --host 0.0.0.0 --port 2137

test:
http://localhost:2137/docs
```