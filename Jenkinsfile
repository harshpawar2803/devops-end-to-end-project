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

                    echo "Image:"
                    echo "${IMAGE_NAME}:${IMAGE_TAG}"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "======================================"
                    echo "        BUILD DOCKER IMAGE"
                    echo "======================================"

                    docker build \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} .
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
                        echo "======================================"
                        echo "        DOCKER HUB LOGIN"
                        echo "======================================"

                        echo "$DOCKER_PASSWORD" | docker login \
                            -u "$DOCKER_USERNAME" \
                            --password-stdin

                        echo "Docker Hub login successful."
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                    echo "======================================"
                    echo "        PUSH DOCKER IMAGE"
                    echo "======================================"

                    docker push ${IMAGE_NAME}:${IMAGE_TAG}

                    echo "Docker image pushed successfully."
                '''
            }
        }

        stage('Docker Logout') {
            steps {
                sh '''
                    echo "Logging out from Docker Hub..."

                    docker logout
                '''
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                    echo "======================================"
                    echo "        DEPLOY APPLICATION"
                    echo "======================================"

                    echo "Stopping old container..."

                    docker rm -f devops-app-jenkins 2>/dev/null || true

                    echo "Starting new container..."

                    docker run -d \
                        --name devops-app-jenkins \
                        -p 8095:8080 \
                        ${IMAGE_NAME}:${IMAGE_TAG}

                    echo "Container started."

                    echo ""
                    echo "Running containers:"
                    docker ps --filter name=devops-app-jenkins
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    echo "======================================"
                    echo "        VERIFY DEPLOYMENT"
                    echo "======================================"

                    echo "Waiting for application to start..."

                    sleep 5

                    echo "Testing application..."

                    curl -f http://localhost:8095

                    echo ""
                    echo "======================================"
                    echo "  APPLICATION DEPLOYMENT SUCCESSFUL"
                    echo "======================================"
                '''
            }
        }
    }

    post {

        success {
            echo "======================================"
            echo "   CI/CD PIPELINE SUCCESSFUL"
            echo "======================================"

            echo "Docker Image:"
            echo "${IMAGE_NAME}:${IMAGE_TAG}"

            echo "Application:"
            echo "http://192.168.71.128:8095"
        }

        failure {
            echo "======================================"
            echo "      CI/CD PIPELINE FAILED"
            echo "======================================"

            echo "Check Console Output for details."
        }
    }
}
