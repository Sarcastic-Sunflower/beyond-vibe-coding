#!/bin/bash

for ((j=1; j<6;j++))
        do
for ((k=1; k<6;k++))
	do
		./test_accuracy.sh 2 ${j} ${k}
done
done
