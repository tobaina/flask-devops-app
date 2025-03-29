pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git url: 'https://github.com/tobaina/flask-devops-app.git', branch: 'main'
            }
        }

        stage('Set up Python') {
            steps {
                sh 'python3 -m venv venv'
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

        stage('Prepare for Deployment') {
            steps {
                sh 'tar -czf app.tar.gz app.py requirements.txt templates/index.html init_db.sql data.db'
            }
        }
    }
}