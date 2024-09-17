#!/bin/bash

# configure the alembic.ini file to point to the correct database in backend/alembic.ini

# Run migrations
cd ../backend
alembic upgrade head