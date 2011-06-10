#!/bin/sh
sed ':a />/!{s/\n//;N;ba}' | sed '/^>/N; s/\n/\t/; s/ /\t/1 ;s/^>//'
