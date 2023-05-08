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
        string(name: 'VERSION', description: 'The version for the model')
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
        VERSION_ = "${params.VERSION}"
        IMAGE_TO_PUSH="${MODEL_NAME}:${VERSION_}"
        SERVER_ID="Jfrog-mlops-model-store"
        DOCKER_REPO="mlops-docker-images"
        MODEL_RESULT = "mlops-trained-models"
        // Define default job parameters
        propagate = true

    }

    stages {
        
        stage('Pull model result from Artifactory') {
            steps {
                script {
                    def server = Artifactory.server(SERVER_ID)
                    def downloadSpec = """{
                        "files": [
                            {
                                "pattern": "${MODEL_RESULT}/${MODEL_NAME}/${VERSION_}.tar.gz",
                                "target": "./"
                            }
                        ]
                    }"""
                    def buildInfo = server.download(downloadSpec)
                    
                }
            }
        }


        stage('Add model and results to Dockerfile') {
            steps {
                sh '''
                cd ${MODEL_NAME}
                chmod 777 "${VERSION_}.tar.gz"
                tar -xvf "${VERSION_}.tar.gz"
                mv train/exp/weights/last.pt ../models_train/"${MODEL_NAME}".pt
                '''
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    
                    
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'artifactory_user',
                            usernameVariable: 'USERNAME',
                            passwordVariable: 'PASSWORD'
                        )
                    ]) {
                        // Build the Docker image
                        sh 'docker build -t ${IMAGE_TO_PUSH} .'
                        sh "docker login -u ${USERNAME} -p ${PASSWORD} artifactorymlopsk18.jfrog.io"
                    }
                }
            }
        }

    }
    post {
        always {
            cleanWs()
        }
    }
}