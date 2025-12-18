pipeline {
    agent any
    
    options {
        // Keep only 10 builds
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    
    stages {
        stage('Run Tests in Docker') {
            steps {
                script {
                    sh '''
                        # Pull Python image
                        docker pull python:3.8
                        
                        # Run tests in Docker container
                        docker run --rm \
                            -v ${WORKSPACE}:/workspace \
                            -w /workspace \
                            python:3.8 bash -c "
                                pip install --upgrade pip && \
                                pip install -r requirements.txt && \
                                pip install pytest pytest-cov pytest-html && \
                                pytest tests/ \
                                    -v \
                                    --junitxml=test-results/junit.xml \
                                    --html=test-results/pytest-report.html \
                                    --self-contained-html \
                                    --cov=pre-production/etl \
                                    --cov-report=xml:test-results/coverage.xml \
                                    --cov-report=html:test-results/htmlcov
                            "
                    '''
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    sh '''
                        # Build Docker image
                        docker build -f deployment/Dockerfile -t thaibigdata/dataops-pipeline:${BUILD_NUMBER} .
                        docker tag thaibigdata/dataops-pipeline:${BUILD_NUMBER} thaibigdata/dataops-pipeline:latest
                    '''
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh '''
                            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                            docker push thaibigdata/dataops-pipeline:${BUILD_NUMBER}
                            docker push thaibigdata/dataops-pipeline:latest
                            docker logout
                        '''
                    }
                }
            }
        }
        
        stage('Deploy to Production') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'db-password', variable: 'DB_PASSWORD')]) {
                        sh '''
                            export DB_PASSWORD="${DB_PASSWORD}"
                            chmod +x deployment/deploy.sh
                            ./deployment/deploy.sh
                        '''
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Archive test results
            archiveArtifacts artifacts: 'test-results/**/*', allowEmptyArchive: true
            
            // Publish test results
            junit allowEmptyResults: true, testResults: 'test-results/junit.xml'
            
            // Publish HTML reports
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'test-results',
                reportFiles: 'pytest-report.html',
                reportName: 'Pytest Report'
            ])
            
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'test-results/htmlcov',
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ])
        }
        
        success {
            echo 'Pipeline completed successfully!'
        }
        
        failure {
            echo 'Pipeline failed!'
        }
    }
}
