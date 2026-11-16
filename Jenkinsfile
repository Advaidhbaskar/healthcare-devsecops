
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'advaidhb/healthcare-devsecops'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Advaidhbaskar/healthcare-devsecops.git'
            }
        }

        
        stage('Gitleaks - Secret Scan') {
            steps {
                bat '''
                docker run --rm -v "%WORKSPACE%:/repo" ghcr.io/gitleaks/gitleaks:latest dir /repo
                '''
            }
        }


        stage('Trivy - Dependency Scan') {
            steps {
                bat '''
                docker run --rm -v "%WORKSPACE%:/project" aquasec/trivy:latest fs --scanners vuln --severity HIGH,CRITICAL --exit-code 1 /project
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% .'
            }
        }

        stage('Trivy - Docker Image Scan') {
            steps {
                bat '''
                docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --severity HIGH,CRITICAL --exit-code 1 %IMAGE_NAME%:%BUILD_NUMBER%
                '''
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-healthcare-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat '''
                    powershell -NoProfile -Command "$env:DOCKER_PASS | docker login --username $env:DOCKER_USER --password-stdin"
                    docker push %IMAGE_NAME%:%BUILD_NUMBER%
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f deployment.yaml'
                bat 'kubectl apply -f service.yaml'
                bat 'kubectl set image deployment/healthcare-app healthcare-container=%IMAGE_NAME%:%BUILD_NUMBER%'
                bat 'kubectl rollout status deployment/healthcare-app --timeout=120s'
            }
        }

        stage('Verify Deployment') {
            steps {
                bat 'kubectl get deployments'
                bat 'kubectl get pods -l app=healthcare-app'
                bat 'kubectl get service healthcare-service'
            }
        }
    }

    post {
        success {
            echo 'DevSecOps pipeline completed successfully. Security gates passed and application deployed.'
        }

        failure {
            echo 'Pipeline failed. Review the failed security or deployment stage before proceeding.'
        }

        always {
            echo 'Healthcare DevSecOps pipeline execution finished.'
        }
    }
}
