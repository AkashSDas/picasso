#! /usr/bin/env sh

# Exit if following commands fail
set -ex

python app/app_prestart.py
alembic upgrade head
