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
        stage('Install dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        stage('SonarQube Analysis') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install coverage pytest
                    coverage run -m pytest tests/
                    coverage xml
                '''
                withSonarQubeEnv("${env.SONARQUBE_ENV}") {
                    sh 'sonar-scanner -Dsonar.projectKey=flask-devops-app -Dsonar.python.coverage.reportPaths=coverage.xml'
                }
            }
        }
        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests/
                '''
            }
        }
        stage('Package Application') {
            steps {
                sh 'tar -czf app-artifact.tar.gz app.py requirements.txt templates init_db.sql Jenkinsfile tests'
            }
        }
        stage('Upload to S3') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: "${env.AWS_CREDENTIALS_ID}",
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    sh 'aws s3 cp app-artifact.tar.gz s3://$S3_BUCKET/builds/app-artifact.tar.gz'
                }
            }
        }
        stage('Upload to Nexus') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${env.NEXUS_CREDENTIALS_ID}", usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASS')]) {
                    sh 'curl -u $NEXUS_USER:$NEXUS_PASS --fail --upload-file app-artifact.tar.gz $NEXUS_URL/app-artifact.tar.gz'
                }
            }
        }
        stage('Deploy with Ansible') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: "${env.AWS_CREDENTIALS_ID}",
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    sh '''
                    ansible-playbook -i ansible/dynamic_inventory.aws_ec2.yml ansible/playbooks/deploy_flask.yml -u admin --private-key /home/ubuntu/wood.pem
                    '''
                }
            }
        }
    }
}
