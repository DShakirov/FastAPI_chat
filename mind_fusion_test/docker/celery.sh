#!/bin/bash

cd src

celery --app=tasks:celery worker -l INFO