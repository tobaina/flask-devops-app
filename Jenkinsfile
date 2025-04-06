pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'ca-central-1'
        S3_BUCKET          = 'flask-devops-artifacts-tobaina'
        NEXUS_URL          = 'http://35.183.72.244:8081'
        NEXUS_REPO         = 'flask-artifacts'
        SONARQUBE_URL      = 'http://99.79.70.72:9000'
        SONARQUBE_TOKEN    = credentials('sonar-token')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/tobaina/flask-devops-app.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonar') {
                    sh '''
                        sonar-scanner \
                        -Dsonar.projectKey=FlaskApp \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=$SONARQUBE_URL \
                        -Dsonar.login=$SONARQUBE_TOKEN
                    '''
                }
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Package Application') {
            steps {
                sh '''
                    . venv/bin/activate
                    python3 setup.py sdist
                '''
            }
        }

        stage('Upload Artifact to S3') {
            steps {
                sh '''
                    aws s3 cp dist/ s3://$S3_BUCKET/ --recursive
                '''
            }
        }

        stage('Upload Artifact to Nexus') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'nexus-creds-id', usernameVariable: 'NEXUS_USERNAME', passwordVariable: 'NEXUS_PASSWORD')]) {
                    sh '''
                        curl -v -u ${NEXUS_USERNAME}:${NEXUS_PASSWORD} \
                             --upload-file dist/*.tar.gz \
                             $NEXUS_URL/repository/$NEXUS_REPO/app-artifact.tar.gz
                    '''
                }
            }
        }

        stage('Ansible Deployment') {
            steps {
                dir('ansible') {
                    sh '''
                        ansible-playbook -i dynamic_inventory.aws_ec2.yml playbooks/deploy_flask.yml
                    '''
                }
            }
        }
    }
}
