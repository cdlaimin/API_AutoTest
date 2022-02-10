pipeline {
    // 创建 JOB 时，任务名称 小写，且避免使用短横线、下划线等其他符号
    agent any
    options {
        disableConcurrentBuilds()
    }
    parameters {
        booleanParam(name: "send_wechat", defaultValue: true, description: "选择是否发送报告到企微群，默认 true")
        string(name: "wechat_token", defaultValue: "73d36c76-5e62-43fd-b18d-eb710fcb4c0e", description: "企微群token")
        choice(name: "env", choices:["tp", ], description: "测试对象选择，默认 tp")
    }
    stages {
        stage("构建docker镜像") {
            steps {
                echo "==================构建镜像=================="
                sh label: "构建镜像", script: "docker build -t ${JOB_NAME}:latest ."
            }
        }
        stage("停止异常容器") {
            steps {
                echo "==================停止异常容器=================="
                // 当前stage报错时，设置构建结果为成功，保证后续stage继续执行
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE'){
                    sh label: '停止测试并删除容器', script: 'docker-compose down'
                }
            }
        }
        stage("清理镜像") {
            steps {
                // 当前stage报错时，设置构建结果为成功，保证后续stage继续执行
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE'){
                    echo "==================清理环境=================="
                    sh script: "docker rmi \$(docker images | grep 'none' | awk '{print \$3}')"
                }
            }
        }
//         stage("关闭退出容器") {
//             steps {
//                 // 当前stage报错时，设置构建结果为成功，保证后续stage继续执行
//                 catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE'){
//                     sh script: "docker stop \$(docker ps -a | grep 'Exited' | awk '{print \$1}')"
//                 }
//             }
//         }
//         stage("删除退出容器") {
//             steps {
//                 // 当前stage报错时，设置构建结果为成功，保证后续stage继续执行
//                 catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE'){
//                     sh script: "docker rm \$(docker ps -a | grep 'Exited' | awk '{print \$1}')"
//                 }
//             }
//         }
        stage("初始化环境") {
            steps {
                echo "==================初始化环境=================="
                // 当前测试在mac上进行，unix和linux sed 命令有些区别，使用 -i 时，要在后面加上一个空字符。linux不能加
                sh label: "指定启动镜像", script: "sed -i 's/demo/${JOB_NAME}/g' docker-compose.yaml"
                sh label: "指定挂载目录", script: "sed -i 's/job_name/${JOB_NAME}/g' docker-compose.yaml"
                sh label: "启动容器", script: "docker-compose up -d"
                sh label: "修改shell操作权限", script: "chmod 777 run.sh"
            }
        }
        stage("执行测试") {
            steps {
                echo "==================执行测试=================="
                // ./ 执行shell文件，需要文件本身具有可执行权限；sh 执行shell文件则不需要
                sh label: "执行测试", script: "./run.sh $JOB_NAME ${params.git_branch} $BUILD_NUMBER ${params.server} ${params.env} ${params.send_wechat} ${params.wechat_token}"
            }
        }
    }
    post {
        always {
            echo "==================停止测试并删除容器==================="
            sh label: '测试执行结束, 删除测试容器', script: 'docker-compose down'
            echo "==================正在收集并生成报告=================="
            script {
                allure([
                    includeProperties: false,
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: "allure-results"]]
                ])
            }
        }
    }
}