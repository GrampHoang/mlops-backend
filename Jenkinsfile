#!/usr/bin/env groovy
library 'mlops-shared-lib'

pipeline {
    agent any

    parameters {
        string(name: 'MODEL_NAME', description: 'The name for the model')
        string(name: 'MODEL_VERSION', description: 'The version for the model')
        string(name: 'IMAGE_NAME', description: 'The version for the model',defaultValue: "currentDeploy")
    }
    options {
        timeout(time: 3, unit: 'HOURS')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        //Artifactory connect info
        def BE_IMAGE_NAME="mlops-backend"
        def SERVER_ID="Jfrog-mlops-model-store"
        def DOCKER_REPO="mlops-docker-images"
        def MODEL_REPO = "mlops-trained-models"

        //Name and version of the backend image to be built
        def IMAGE_TO_PUSH="${BE_IMAGE_NAME}:${params.IMAGE_NAME}"
        def model_list=""
        def version_list=""

        // Define default job parameters
        propagate = true

    }

    stages {
        stage('Process Input') {
            steps {
                script {
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'artifactory-chih',
                            usernameVariable: 'USERNAME',
                            passwordVariable: 'PASSWORD'
                        )
                    ]){
                        if (!params.MODEL_NAME?.trim()) {
                            echo "MODEL_NAME is a mandatory parameter"
                            error "MODEL_NAME is a mandatory parameter"
                            return
                        }
                        if (!params.MODEL_VERSION?.trim()) {
                            echo "MODEL_VERSION is a mandatory parameter"
                            error "MODEL_VERSION is a mandatory parameter"
                            return
                        }

                        //Checking semantic for params
                        semanticVersionCheck(this,params.MODEL_NAME)
                        semanticVersionCheck(this,params.MODEL_VERSION)
                        
                        //Parse model version to build image
                        model_list = params.MODEL_NAME.split(',')
                        version_list = params.MODEL_VERSION.split(',')
                        echo "Checking model version on Artifactory"
                        if (model_list.size() == version_list.size()){
                            for (int i = 0; i < model_list.size(); i++) {
                                sh "echo Checking on model: ${model_list[i]} version: ${version_list[i]}"
                                sh "curl -u ${USERNAME}:${PASSWORD} -f -I https://${env.SERVER_URL}/artifactory/${MODEL_REPO}/${model_list[i]}/${version_list[i]}.tar.gz"
                            }
                        } else {
                            echo "Models and versions is not equal"
                            error "Exit process"
                            return
                        }
                    }
                }
            }
        }

        stage('Pull model results from Artifactory') {
            steps {
                script {
                    def server = Artifactory.server(SERVER_ID)
                    for (int i = 0; i < model_list.size(); i++) {
                        sh "echo Download model: ${model_list[i]} version: ${version_list[i]}"                       
                        // Perform the desired steps for each value
                        def downloadSpec = """{
                            "files": [
                                {
                                    "pattern": "${MODEL_REPO}/${model_list[i]}/${version_list[i]}.tar.gz",
                                    "target": "./"
                                }
                            ]
                        }"""
                        def buildInfo = server.download(downloadSpec)
                    }
                }
            }
        }

        stage('Add model and results to Dockerfile') {
            steps {
                script {
                    for (int i = 0; i < model_list.size(); i++) {
                        sh "echo Move model: ${model_list[i]} to model_folder"
                        sh """
                            cd ${model_list[i]}
                            chmod 777 ${version_list[i]}.tar.gz
                            tar -xvf ${version_list[i]}.tar.gz
                            mv train/exp/weights/best.pt ../models_train/${model_list[i]}.pt
                        """
                    }
                }
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
                        sh "docker build -t ${env.SERVER_URL}/${DOCKER_REPO}/${IMAGE_TO_PUSH} ."
                        sh "docker login -u ${USERNAME} -p ${PASSWORD} ${env.SERVER_URL}"

                        // sh "docker tag ${IMAGE_TO_PUSH} ${env.SERVER_URL}/${DOCKER_REPO}/${IMAGE_TO_PUSH}"
                        sh "docker push ${env.SERVER_URL}/${DOCKER_REPO}/${IMAGE_TO_PUSH}"
                    }
                }
            }
            post {
                success {
                    script { 
                        sh "docker image rm -f ${env.SERVER_URL}/${DOCKER_REPO}/${IMAGE_TO_PUSH}" 
                    }
                }
            }
        }

    }
    post {
        success {
            slackSend(color:"good", message:"To: <!here|here>, Build deployed successfully - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)")
        }

        failure {
            slackSend(color:"#ff0000",message: "To: <!channel|channel>, Build failed  - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)")
        }

        always {
            cleanWs()
        }
    }
}