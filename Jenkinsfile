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
                                "target": "${ARCHIV}"
                            }
                        ]
                    }"""
                )
            }
        }


        stage('Upload model and results to Artifactory') {
            steps {
                sh 'ls'
            }
        }

    }
    post {
        always {
            cleanWs()
        }
    }
}