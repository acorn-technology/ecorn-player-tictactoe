#!/bin/bash
docker run -it --rm -p 9080:9080 --mount type=bind,source="$(pwd)",target=/usr/src/app --name tictacgame_running tictacgame