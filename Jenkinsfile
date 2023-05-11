#!/usr/bin/env groovy



pipeline {
    agent any

    parameters {
        string(name: 'MODEL_NAME', description: 'The name for the model')
        string(name: 'VERSION', description: 'The version for the model')
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
        BE_IMAGE_NAME="mlops-backend"
        IMAGE_TO_PUSH="${BE_IMAGE_NAME}:${MODEL_NAME}"
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
                mv train/exp/weights/best.pt ../models_train/"${MODEL_NAME}".pt
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
                        sh "docker build -t artifactorymlopsk18.jfrog.io/${DOCKER_REPO}/${IMAGE_TO_PUSH} ."
                        sh "docker login -u ${USERNAME} -p ${PASSWORD} artifactorymlopsk18.jfrog.io"

                        // sh "docker tag ${IMAGE_TO_PUSH} artifactorymlopsk18.jfrog.io/${DOCKER_REPO}/${IMAGE_TO_PUSH}"
                        sh "docker push artifactorymlopsk18.jfrog.io/${DOCKER_REPO}/${IMAGE_TO_PUSH}"
                    }
                }
            }
            post {
                success {
                    script { 
                        sh "docker image rm -f artifactorymlopsk18.jfrog.io/${DOCKER_REPO}/${IMAGE_TO_PUSH}" 
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