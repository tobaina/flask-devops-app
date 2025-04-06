pipeline {
    agent any

    environment {
        S3_BUCKET = 'flask-devops-artifacts-tobaina'
        AWS_CREDENTIALS_ID = 'aws-s3-creds'
        SONAR_AUTH_TOKEN = credentials('sonar-token')
        SONAR_HOST_URL = 'http://99.79.70.72:9000'   // your SonarQube server URL
        NEXUS_URL = '99.79.70.72:8081'               // your Nexus server URL without http
        NEXUS_REPOSITORY = 'flask-devops-repo'       // your Nexus repository name
        NEXUS_CREDENTIALS_ID = 'nexus-creds'         // your Nexus credentials ID in Jenkins
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
                nexusArtifactUploader(
                    nexusVersion: 'nexus3',
                    protocol: 'http',
                    nexusUrl: "${NEXUS_URL}",
                    groupId: 'com.tobaina',
                    version: '1.0.0',
                    repository: "${NEXUS_REPOSITORY}",
                    credentialsId: "${NEXUS_CREDENTIALS_ID}",
                    artifacts: [
                        [artifactId: 'flask-devops-app', classifier: '', file: 'app-artifact.tar.gz', type: 'tar.gz']
                    ]
                )
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
