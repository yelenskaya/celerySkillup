#!/bin/bash

set -o errexit
set -o nounset

cd $PROJECT_DIR

worker_ready() {
    $ACTIVE_CELERY -A app.main.celery inspect ping
}

until worker_ready; do
  >&2 echo 'Celery workers are not available'
  sleep 1
done
>&2 echo 'Celery workers are available'

$ACTIVE_CELERY -A app.main.celery flower
