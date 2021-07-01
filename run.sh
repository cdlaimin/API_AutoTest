#!/bin/bash
dir=$(cd `dirname $0`; pwd)
echo dir
project_name=${dir##*/}
echo project_name
names=( `docker-compose ps | awk '{print $1}' | grep ${project_name}` )
echo "=================开始进行测试,当前测试HUB分支: $1================="
echo names
docker exec -i ${names[0]} pytest --show-capture=no -d --job_name="$2" --build_number="$3" --tx socket=${names[1]}:8888 --tx socket=${names[2]}:8888 --rsyncdir tests/ tests/ --alluredir=allure-results --clean-alluredir --reruns=1 || true
echo "=================测试执行完成，一点点清理工作================="
