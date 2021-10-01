#!/bin/bash
dir=$(cd `dirname $0`; pwd)
project_name=${dir##*/}
names=$( `docker-compose ps | awk '{print $1}' | grep ${project_name}` )
echo "=================开始进行测试,当前测试HUB分支: $4================="
echo ${names[0]}
docker exec -i ${names[0]} pytest -m "$5" --show-capture=no -d --job_name="$1" --build_number="$2" --target="$3" --send_wechat="$6" --wechat_token="$7" --tx socket=${names[1]}:8888 --tx socket=${names[2]}:8888 --rsyncdir tests/ tests/ --alluredir=allure-results --clean-alluredir --reruns=1 || true
