pipeline {

    parameters {

        choice(
            name: 'DEPLOY_MODE',
            choices: ['NORMAL', 'ROLLBACK'],
            description: 'Select NORMAL for CI/CD deployment or ROLLBACK for an older Docker image'
        )

        string(
            name: 'ROLLBACK_VERSION',
            defaultValue: '3',
            description: 'Docker image version to deploy during rollback'
        )
    }

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

                    echo "Docker image built successfully."

                    docker images ${IMAGE_NAME}:${IMAGE_TAG}
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
                    echo "======================================"
                    echo "        DOCKER LOGOUT"
                    echo "======================================"

                    docker logout

                    echo "Docker logout successful."
                '''
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                    echo "======================================"
                    echo "        DEPLOY APPLICATION"
                    echo "======================================"

                    if [ "$DEPLOY_MODE" = "ROLLBACK" ]; then

                        DEPLOY_TAG="$ROLLBACK_VERSION"

                        echo "Deployment Mode: ROLLBACK"
                        echo "Rollback Version: $DEPLOY_TAG"

                    else

                        DEPLOY_TAG="$IMAGE_TAG"

                        echo "Deployment Mode: NORMAL"
                        echo "Build Version: $DEPLOY_TAG"

                    fi

                    echo "======================================"
                    echo "Image to Deploy:"
                    echo "${IMAGE_NAME}:${DEPLOY_TAG}"
                    echo "======================================"

                    echo "Checking Docker image..."

                    docker image inspect \
                        ${IMAGE_NAME}:${DEPLOY_TAG} > /dev/null

                    echo "Docker image found."

                    echo "Stopping old container..."

                    docker rm -f devops-app-jenkins 2>/dev/null || true

                    echo "Starting new container..."

                    docker run -d \
                        --name devops-app-jenkins \
                        -p 8095:8080 \
                        ${IMAGE_NAME}:${DEPLOY_TAG}

                    echo "Container started."

                    echo "======================================"
                    echo "Running Container:"
                    echo "======================================"

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

            echo "Deployment Mode:"
            echo "${DEPLOY_MODE}"

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

        always {
            echo "======================================"
            echo "       PIPELINE COMPLETED"
            echo "======================================"

            echo "Build Number:"
            echo "${BUILD_NUMBER}"

            echo "Deployment Mode:"
            echo "${DEPLOY_MODE}"
        }
    }
}
