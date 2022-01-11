#!/bin/bash
## Creating ansible inventory from terraform state file

filter="$(cat "terraform/terraform.tfstate" | grep \"public_ip\" | awk -F "\"" '{print$4}')"

echo "[test]" > "ansible/hosts"
if [ -n "$filter" ]; then 
  for line in $filter; do
    echo "host${i:=1}   ansible_host=$line" >> "ansible/hosts"
    ((i++))
  done
else
  echo "host1   ansible_host="  >> "ansible/hosts"
fi
