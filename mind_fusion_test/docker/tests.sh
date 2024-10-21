#!/bin/bash

alembic upgrade head

pytest tests -s -v