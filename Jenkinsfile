pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                echo 'Cloning code from GitHub...'
                // Jenkins already clones your repo using the SCM setup
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Run Flask App (basic test)') {
            steps {
                sh 'python3 app.py &'
                sh 'sleep 5' // wait for it to start
                sh 'curl http://localhost:5000 || echo "App not responding!"'
            }
        }
    }
}
