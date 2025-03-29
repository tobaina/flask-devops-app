pipeline {
    agent any

    environment {
        AWS_REGION = 'ca-central-1'
        ANSIBLE_HOST_KEY_CHECKING = 'False'
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/tobaina/flask-devops-app.git'
            }
        }

        stage('Set up Python') {
            steps {
                sh 'python3 -m venv ./venv'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Run Unit Test') {
            steps {
                sh './venv/bin/pytest --junitxml=report.xml'
            }
        }

        stage('Publish Test Report') {
            steps {
                junit 'report.xml'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh './venv/bin/pip install pylint'
                    sh './venv/bin/pylint app.py || true'
                }
            }
        }

        stage('Prepare for Deployment') {
            steps {
                sh 'tar -czf app.tar.gz app.py requirements.txt templates/index.html init_db.sql data.db'
            }
        }

        stage('Upload to S3') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'aws-creds', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    withAWS(region: "${AWS_REGION}", credentials: 'aws-creds') {
                        s3Upload(
                            bucket: 'flask-devops-artifacts-tobaina',
                            file: 'app.tar.gz',
                            path: 'builds/app.tar.gz'
                        )
                    }
                }
            }
        }

        stage('Run Ansible Deployment') {
            steps {
                sh 'ansible-playbook -i inventory.ini deploy.yml'
            }
        }
    }
}

