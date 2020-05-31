#!/bin/bash
docker build --no-cache -t feagi:0.1 .
docker run -t feagi:0.1
