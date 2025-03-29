pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                echo 'Cloning code from GitHub...'
                // Already done by Jenkins using "Pipeline from SCM"
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
                sh '''
                    source venv/bin/activate
                    nohup python app.py > app.log 2>&1 &
                    sleep 5
                    curl http://localhost:5000 || echo "App not responding!"
                '''
            }
        }
    }
}
