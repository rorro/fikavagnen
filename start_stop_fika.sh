#!/bin/bash
file=/home/robin/Documents/python/fikavagnen/fikatimeteller
if grep -q yes "$file" ; then
    echo no > $file
else
    echo yes > $file
fi
