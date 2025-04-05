pipeline {
    agent any

    environment {
        S3_BUCKET = 'flask-devops-artifacts-tobaina'
        AWS_CREDENTIALS_ID = 'aws-s3-creds'
        SONAR_AUTH_TOKEN = credentials('sonar-token')  // pulled securely
        SONAR_HOST_URL = 'http://35.183.48.7:9000'     // your SonarQube URL
    }

    stages {
        stage('Install dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonar') {
                    sh '''
                        ./venv/bin/pip install coverage
                        ./venv/bin/coverage run -m pytest tests/
                        ./venv/bin/coverage xml
                        sonar-scanner \
                          -Dsonar.projectKey=flask-devops-app \
                          -Dsonar.python.coverage.reportPaths=coverage.xml \
                          -Dsonar.sources=. \
                          -Dsonar.host.url=$SONAR_HOST_URL \
                          -Dsonar.login=$SONAR_AUTH_TOKEN
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    echo "Running unit tests..."
                    ./venv/bin/pytest tests/
                '''
            }
        }

        stage('Upload to S3') {
            steps {
                sh '''
                    tar -czf app-artifact.tar.gz app.py requirements.txt templates/ init_db.sql Jenkinsfile tests/
                '''
                withAWS(credentials: "${AWS_CREDENTIALS_ID}", region: 'ca-central-1') {
                    s3Upload(bucket: "${S3_BUCKET}", path: "builds/app-artifact.tar.gz", file: "app-artifact.tar.gz")
                }
            }
        }

        stage('Deploy with Ansible') {
            steps {
                dir('ansible') {
                    sh 'ansible-playbook -i dynamic_inventory.aws_ec2.yml playbooks/deploy_flask.yml'
                }
            }
        }
    }
}
