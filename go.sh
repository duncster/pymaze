#!/bin/bash

export SDL_VIDEODRIVER=x11
./test.py
unset SDL_VIDEODRIVER
