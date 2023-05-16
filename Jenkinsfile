#!/usr/bin/env groovy

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

        def VERSION_ = "latest"
        //Artifactory connect info
        def SERSER_URL="artifactorymlopsk18.jfrog.io"
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
                script 
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'artifactory_user',
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
                    model_list = params.MODEL_NAME.split(',')
                    version_list = params.MODEL_VERSION.split(',')
                    echo "Checking model version on Artifactory"
                    if (model_list.size() == version_list.size()){
                        for (int i = 0; i < model_list.size(); i++) {
                            sh " curl -u${USERNAME}:${PASSWORD} -f -I https://${SERVER_URL}/artifactory/${MODEL_REPO}/${model_list[i]}/${version_list[i]}.tar.gz"
                        }
                    } else {
                        echo "Models and versions is not equal"
                        error "Exit process"
                        return
                    }
                }
            }
        }
        // stage('Pull model results from Artifactory') {
        //     steps {
        //         script {
        //             def server = Artifactory.server(SERVER_ID)
        //             for (def value in model_list) {
        //                 echo "Download model: ${value}"                       
        //                 // Perform the desired steps for each value
        //                 def downloadSpec = """{
        //                     "files": [
        //                         {
        //                             "pattern": "${MODEL_REPO}/${value}/${VERSION_}.tar.gz",
        //                             "target": "./"
        //                         }
        //                     ]
        //                 }"""
        //                 def buildInfo = server.download(downloadSpec)
        //             }
        //         }
        //     }
        // }
        stage("test"){
            steps {
                script {
                    echo "Model_array: ${model_list}"
                }
            }
        }

        // stage('Add model and results to Dockerfile') {
        //     steps {
        //         script {
        //             for (def value in model_list) {
        //                 echo "Move model: ${value} to model_folder"                       
        //                 // Perform the desired steps for each value
        //                 sh '''
        //                     cd ${MODEL_NAME}
        //                     chmod 777 "${VERSION_}.tar.gz"
        //                     tar -xvf "${VERSION_}.tar.gz"
        //                     mv train/exp/weights/best.pt ../models_train/"${MODEL_NAME}".pt
        //                 '''
        //             }
        //         }
        //     }
        // }

        // stage('Build and Push Docker Image') {
        //     steps {
        //         script {
                    
        //             withCredentials([
        //                 usernamePassword(
        //                     credentialsId: 'artifactory_user',
        //                     usernameVariable: 'USERNAME',
        //                     passwordVariable: 'PASSWORD'
        //                 )
        //             ]) {
        //                 // Build the Docker image
        //                 sh "docker build -t artifactorymlopsk18.jfrog.io/${DOCKER_REPO}/${IMAGE_TO_PUSH} ."
        //                 sh "docker login -u ${USERNAME} -p ${PASSWORD} artifactorymlopsk18.jfrog.io"

        //                 // sh "docker tag ${IMAGE_TO_PUSH} artifactorymlopsk18.jfrog.io/${DOCKER_REPO}/${IMAGE_TO_PUSH}"
        //                 sh "docker push artifactorymlopsk18.jfrog.io/${DOCKER_REPO}/${IMAGE_TO_PUSH}"
        //             }
        //         }
        //     }
        //     post {
        //         success {
        //             script { 
        //                 sh "docker image rm -f artifactorymlopsk18.jfrog.io/${DOCKER_REPO}/${IMAGE_TO_PUSH}" 
        //             }
        //         }
        //     }
        // }

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