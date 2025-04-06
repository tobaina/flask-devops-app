pipeline {
    agent any

    environment {
        S3_BUCKET = 'flask-devops-artifacts-tobaina'
        AWS_CREDENTIALS_ID = 'aws-s3-creds'
        SONARQUBE_ENV = 'sonar'
        NEXUS_CREDENTIALS_ID = 'nexus-creds'
        NEXUS_URL = 'http://35.183.72.244:8081/repository/flask-devops-artifacts/'
    }

    stages {

        stage('Set up Python Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE_ENV}") {
                    sh '''
                        ./venv/bin/pip install coverage
                        ./venv/bin/coverage run -m pytest tests/
                        ./venv/bin/coverage xml
                        sonar-scanner \
                          -Dsonar.projectKey=flask-devops-app \
                          -Dsonar.sources=. \
                          -Dsonar.python.coverage.reportPaths=coverage.xml
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    echo "Running unit tests..."
                    ./venv/bin/pytest tests/
                '''
            }
        }

        stage('Package Application') {
            steps {
                sh '''
                    tar -czf app-artifact.tar.gz app.py requirements.txt templates/ init_db.sql Jenkinsfile tests/
                '''
            }
        }

        stage('Upload to S3') {
            steps {
                withAWS(credentials: "${AWS_CREDENTIALS_ID}", region: 'ca-central-1') {
                    s3Upload(bucket: "${S3_BUCKET}", path: "builds/app-artifact.tar.gz", file: "app-artifact.tar.gz")
                }
            }
        }

        stage('Upload to Nexus') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${NEXUS_CREDENTIALS_ID}", usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASS')]) {
                    sh '''
                        curl -v -u "$NEXUS_USER:$NEXUS_PASS" --upload-file app-artifact.tar.gz "${NEXUS_URL}app-artifact.tar.gz"
                    '''
                }
            }
        }

        stage('Deploy with Ansible') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: "${AWS_CREDENTIALS_ID}"]]) {
                    dir('ansible') {
                        sh '''
                            export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                            export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                            cp ../app-artifact.tar.gz .
                            cp ../init_db.sql .
                            ansible-playbook -i dynamic_inventory.aws_ec2.yml playbooks/deploy_flask.yml
                        '''
                    }
                }
            }
        }
    }
}
