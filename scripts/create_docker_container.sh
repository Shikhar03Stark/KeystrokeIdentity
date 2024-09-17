#!/bin/bash

# Create a new docker container
docker run -d -p 5432:5432 --name keystroke_identity -e POSTGRES_PASSWORD=password -e POSTGRES_USER=keystroke -e POSTGRES_DB=keystroke pgvector/pgvector:pg16
