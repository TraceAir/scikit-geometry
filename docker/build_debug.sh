#!/bin/bash
set -e
docker build .. -f Dockerfile-debug -t scikit-geometry
docker run -it --rm scikit-geometry