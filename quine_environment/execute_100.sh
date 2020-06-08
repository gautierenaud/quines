#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: ./execute_100.sh quine.py"
    exit 1
fi

rm -r out
mkdir -p out

script_name=$1

for i in {1..100}
do
  new_file_name=out/tmp_$i.py
  python3 $script_name > $new_file_name
  exit_code=$?

  if [ $exit_code -ne 0 ]; then
    echo "Breaking (not executable) at ${i}th iteration"
    exit 1
  fi

  script_name=$new_file_name
done

echo "Finished!"