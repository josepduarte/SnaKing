#!/bin/bash

echo "" > testes.txt
for i in {1..20..1}
do
	echo -e "\e[33m------------------------------------------\e[0m\n"
	python3 start.py --disable-video
	echo -e "\e[33m__________________________________________\e[0m\n"
done