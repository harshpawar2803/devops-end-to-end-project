pipeline {

    agent any

    environment {
        IMAGE_NAME = "harshpawar2803/devops-app"
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }

    stages {

        stage('System Information') {
            steps {
                sh '''
                    echo "======================================"
                    echo "       JENKINS CI/CD PIPELINE"
                    echo "======================================"
                    echo "User:"
                    whoami
                    echo "Workspace:"
                    pwd
                    echo "Git Commit:"
                    git log -1 --oneline
                    echo "Docker:"
                    docker --version
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "Building Docker Image..."
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Docker Hub Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "${DOCKER_PASSWORD}" | docker login \
                            -u "${DOCKER_USERNAME}" \
                            --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    echo "Stopping old container..."
                    docker rm -f devops-app-jenkins 2>/dev/null || true

                    echo "Starting new container..."
                    docker run -d \
                        --name devops-app-jenkins \
                        -p 8095:8080 \
                        ${IMAGE_NAME}:${IMAGE_TAG}

                    docker ps
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    sleep 3

                    echo "Checking application..."

                    curl --fail http://localhost:8095

                    echo ""
                    echo "Application is UP"
                '''
            }
        }
    }

    post {
        success {
            echo "======================================"
            echo "       DEPLOYMENT SUCCESS"
            echo "======================================"
            echo "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
        }

        failure {
            echo "======================================"
            echo "       DEPLOYMENT FAILED"
            echo "======================================"
        }
    }
}
