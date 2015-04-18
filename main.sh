#!/bin/bash

# If a symlink to the blpapi library exists in this directory, things are broken and we need to add . to the library load path.
if [ -e libblpapi3_64.so ]
then
	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:.
fi

./main.py
