pipeline {
    agent any

    environment {
        S3_BUCKET = 'flask-devops-artifacts-tobaina'
        AWS_CREDENTIALS_ID = 'aws-s3-creds'
    }

    stages {
        stage('Clone') {
            steps {
                echo 'Cloning code from GitHub...'
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install -r requirements.txt'
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

        stage('Run Flask App (basic test)') {
            steps {
                sh '''
                    . venv/bin/activate
                    nohup python app.py > app.log 2>&1 &
                    sleep 5
                    curl http://localhost:5000 || echo "App not responding!"
                '''
            }
        }

        stage('Upload to S3') {
            steps {
                sh '''
                    tar -czf app-artifact.tar.gz app.py requirements.txt templates/ static/ init_db.sql Jenkinsfile tests/
                '''
                withAWS(credentials: "${AWS_CREDENTIALS_ID}", region: 'us-east-1') {
                    s3Upload(bucket: "${S3_BUCKET}", path: "builds/app-artifact.tar.gz", file: "app-artifact.tar.gz")
                }
            }
        }
    }
}
