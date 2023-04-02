#!/usr/bin/env groovy



pipeline {
    agent any
        // docker {
        //     // image 'ultralytics/yolov5:latest'
        //     image 'hoangchieng/mlops_image:v3'
        //     args '--ipc=host'
        // }
    

    parameters {
        string(name: 'MODEL_NAME', description: 'The name for the model')
        // string(name: 'IMG', description: 'The image size for training. Example 480', defaultValue: "480")
        // string(name: 'BATCH', description: 'The number to build at a time. Example 1', defaultValue: "1")
        // string(name: 'EPOCH', description: 'The number of training for model. Example 1', defaultValue: "1")
        // string(name: 'DATA_PATH', description: 'The path to data folder. Example mlops-demo-project-1', defaultValue: "mlops-demo-project-1")
        // string(name: 'WEIGHT', description: 'The weight to start traing from. Example yolov5l.pt', defaultValue: "yolov5n.pt")
    }
    options {
        timeout(time: 1, unit: 'HOURS')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        // Copy the Jenkins build number of Suite-Build job into a global iPension environment variable
        // MLOPS_TRAIN_NUMBER = "${env.BUILD_NUMBER}"
        VERSION_ = 'latest'
        ARCHIV = "${params.MODEL_NAME}"+'.tar.gz'
        // Define default job parameters
        propagate = true

    }

    stages {
        
        stage('Pull model result from Artifactory') {
            steps {
                rtDownload (
                    serverId: 'Jfrog-mlops-model-store',
                    spec: """{
                        "files": [
                            {
                                "pattern": "mlops-trained-model/${MODEL_NAME}/${VERSION_}.tar.gz",
                                "target": "."
                            }
                        ]
                    }"""
                )
            }
            // post {
            //     success {
            //         script { 
            //             untar file: ARCHIV, dir: 'runs' 
            //         }
            //     }
            // }
        }


        stage('Add model and results to Dockerfile') {
            steps {
                sh '''
                ls -l
                '''
            }
        }

        stage('Build docker images') {
            steps {
                sh '''
                docker build -t ${MODEL_NAME} .
                '''
            }
        }

        stage('Deploy model'){
            steps {
                // sh  "docker ps | grep 9443 | awk '{print $1}' | xargs docker container stop"
                sh '''
                    docker run --rm -d -p 5000:5000 ${MODEL_NAME}
                '''
            }
        }

    }
    post {
        always {
            cleanWs()
        }
    }
}