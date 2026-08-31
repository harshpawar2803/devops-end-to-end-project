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
        TEST_CONTAINER = "devops-app-test"
        DEPLOY_CONTAINER = "devops-app-jenkins"
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

                    echo "Docker Compose:"
                    docker compose version 2>/dev/null || true

                    echo "Build Number:"
                    echo "${BUILD_NUMBER}"

                    echo "Deployment Mode:"
                    echo "${DEPLOY_MODE}"

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

                    echo "Building:"
                    echo "${IMAGE_NAME}:${IMAGE_TAG}"

                    docker build \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} .

                    echo "Docker image built successfully."

                    echo "======================================"
                    echo "        BUILT IMAGE DETAILS"
                    echo "======================================"

                    docker images ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Test Docker Image') {
            steps {
                sh '''
                    echo "======================================"
                    echo "        TEST DOCKER IMAGE"
                    echo "======================================"

                    echo "Test Image:"
                    echo "${IMAGE_NAME}:${IMAGE_TAG}"

                    echo "Removing old test container if present..."

                    docker rm -f ${TEST_CONTAINER} 2>/dev/null || true

                    echo "Starting test container..."

                    docker run -d \
                        --name ${TEST_CONTAINER} \
                        -p 8096:8080 \
                        ${IMAGE_NAME}:${IMAGE_TAG}

                    echo "Test container started."

                    echo "Waiting for application to start..."

                    sleep 5

                    echo "======================================"
                    echo "        CONTAINER STATUS"
                    echo "======================================"

                    docker ps --filter name=${TEST_CONTAINER}

                    echo "======================================"
                    echo "        APPLICATION TEST"
                    echo "======================================"

                    echo "Testing:"
                    echo "http://localhost:8096"

                    curl -f http://localhost:8096

                    echo ""

                    echo "Application response received successfully."

                    echo "======================================"
                    echo "        CONTAINER LOGS"
                    echo "======================================"

                    docker logs ${TEST_CONTAINER}

                    echo "======================================"
                    echo "        CLEANING TEST CONTAINER"
                    echo "======================================"

                    docker rm -f ${TEST_CONTAINER}

                    echo "======================================"
                    echo "       TEST PASSED SUCCESSFULLY"
                    echo "======================================"
                '''
            }

            post {
                failure {
                    sh '''
                        echo "======================================"
                        echo "        TEST FAILED"
                        echo "======================================"

                        echo "Test container logs:"

                        docker logs ${TEST_CONTAINER} 2>/dev/null || true

                        echo "Removing failed test container..."

                        docker rm -f ${TEST_CONTAINER} 2>/dev/null || true
                    '''
                }
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

                    echo "Pushing:"
                    echo "${IMAGE_NAME}:${IMAGE_TAG}"

                    docker push ${IMAGE_NAME}:${IMAGE_TAG}

                    echo "Docker image pushed successfully."

                    echo "======================================"
                    echo "        IMAGE PUSH COMPLETE"
                    echo "======================================"
                '''
            }
        }

        stage('Docker Logout') {
            steps {
                sh '''
                    echo "======================================"
                    echo "        DOCKER LOGOUT"
                    echo "======================================"

                    echo "Logging out from Docker Hub..."

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
                    echo "        IMAGE TO DEPLOY"
                    echo "======================================"

                    echo "${IMAGE_NAME}:${DEPLOY_TAG}"

                    echo "======================================"
                    echo "        CHECKING DOCKER IMAGE"
                    echo "======================================"

                    docker image inspect \
                        ${IMAGE_NAME}:${DEPLOY_TAG} > /dev/null

                    echo "Docker image found."

                    echo "======================================"
                    echo "        STOPPING OLD CONTAINER"
                    echo "======================================"

                    docker rm -f ${DEPLOY_CONTAINER} 2>/dev/null || true

                    echo "Old container removed."

                    echo "======================================"
                    echo "        STARTING NEW CONTAINER"
                    echo "======================================"

                    docker run -d \
                        --name ${DEPLOY_CONTAINER} \
                        -p 8095:8080 \
                        ${IMAGE_NAME}:${DEPLOY_TAG}

                    echo "Container started."

                    echo "======================================"
                    echo "        RUNNING CONTAINER"
                    echo "======================================"

                    docker ps --filter name=${DEPLOY_CONTAINER}

                    echo "======================================"
                    echo "        DEPLOYMENT COMPLETE"
                    echo "======================================"
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

                    echo "======================================"
                    echo "        CONTAINER STATUS"
                    echo "======================================"

                    docker ps --filter name=${DEPLOY_CONTAINER}

                    echo "======================================"
                    echo "        APPLICATION TEST"
                    echo "======================================"

                    echo "Testing:"
                    echo "http://localhost:8095"

                    curl -f http://localhost:8095

                    echo ""

                    echo "Application responded successfully."

                    echo "======================================"
                    echo "        DEPLOYED IMAGE"
                    echo "======================================"

                    docker inspect ${DEPLOY_CONTAINER} \
                        --format '{{.Config.Image}}'

                    echo "======================================"
                    echo "  APPLICATION DEPLOYMENT SUCCESSFUL"
                    echo "======================================"
                '''
            }
        }

        stage('Docker Image Cleanup') {
            steps {
                sh '''
                    echo "======================================"
                    echo "        DOCKER IMAGE CLEANUP"
                    echo "======================================"

                    echo "Currently deployed image:"

                    CURRENT_IMAGE=$(docker inspect ${DEPLOY_CONTAINER} \
                        --format '{{.Config.Image}}')

                    echo "$CURRENT_IMAGE"

                    echo "======================================"
                    echo "Keeping latest 5 numbered images"
                    echo "and the currently deployed image."
                    echo "======================================"

                    docker images ${IMAGE_NAME} \
                        --format '{{.Tag}}' \
                        | grep -E '^[0-9]+$' \
                        | sort -nr \
                        | tail -n +6 \
                        | while read TAG
                    do

                        if [ -n "$TAG" ]; then

                            IMAGE="${IMAGE_NAME}:${TAG}"

                            if [ "$IMAGE" = "$CURRENT_IMAGE" ]; then

                                echo "Keeping currently deployed image:"
                                echo "$IMAGE"

                            else

                                echo "Removing old image:"
                                echo "$IMAGE"

                                docker rmi "$IMAGE" || true

                            fi

                        fi

                    done

                    echo "======================================"
                    echo "      REMAINING APPLICATION IMAGES"
                    echo "======================================"

                    docker images ${IMAGE_NAME}

                    echo "======================================"
                    echo "        DOCKER DISK USAGE"
                    echo "======================================"

                    docker system df

                    echo "======================================"
                    echo "        CLEANUP COMPLETE"
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

            echo "Build Number:"
            echo "${BUILD_NUMBER}"

            echo "Deployment Mode:"
            echo "${DEPLOY_MODE}"

            echo "Build Image:"
            echo "${IMAGE_NAME}:${IMAGE_TAG}"

            echo "Application:"
            echo "http://192.168.71.128:8095"

            echo "======================================"
            echo "       ALL STAGES PASSED"
            echo "======================================"
        }

        failure {
            echo "======================================"
            echo "      CI/CD PIPELINE FAILED"
            echo "======================================"

            echo "Build Number:"
            echo "${BUILD_NUMBER}"

            echo "Deployment Mode:"
            echo "${DEPLOY_MODE}"

            echo "Check Console Output for details."

            echo "======================================"
        }

        always {
            echo "======================================"
            echo "       PIPELINE COMPLETED"
            echo "======================================"

            echo "Build Number:"
            echo "${BUILD_NUMBER}"

            echo "Deployment Mode:"
            echo "${DEPLOY_MODE}"

            echo "======================================"
        }
    }
}
