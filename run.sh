#!/bin/bash
dir=$(
  cd $(dirname "$0")
  pwd
)
project_name=${dir##*/}
names=($(docker-compose ps | grep "${project_name}" | awk '{print $1}'))
echo "=================开始进行测试,当前测试HUB分支: $2================="
echo "docker exec -i ${names[0]} pytest --show-capture=no --job_name=$1 --build_number=$3 --server=$4 --env=$5 --send_wechat=$6 --wechat_token=$7 -d --tx socket=${names[1]}:8888 --tx socket=${names[2]}:8888 --rsyncdir tests/ tests/ --alluredir=allure-results --clean-alluredir --reruns=1 || true"
docker exec -i "${names[0]}" pytest --show-capture=no --job_name="$1" --build_number="$3" --server="$4" --env="$5" --send_wechat="$6" --wechat_token="$7" -d --tx socket="${names[1]}":8888 --tx socket="${names[2]}":8888 --rsyncdir tests/ tests/ --alluredir=allure-results --clean-alluredir --reruns=1 || true
