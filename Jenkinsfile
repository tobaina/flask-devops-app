pipeline {
    agent any

    environment {
        // AWS and Nexus environment variables
        AWS_DEFAULT_REGION = 'ca-central-1'
        S3_BUCKET          = 'flask-devops-artifacts-tobaina'
        NEXUS_URL          = 'http://35.183.72.244:8081'
        NEXUS_REPO         = 'flask-artifacts'  // Use the real Nexus raw repo name you created

        // SonarQube variables (assuming you have these as Jenkins credentials or env variables)
        SONARQUBE_URL      = 'http://35.183.48.7:9000'  // Your SonarQube URL
        SONARQUBE_TOKEN    = credentials('sonar-token') // SonarQube token securely pulled
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/tobaina/flask-devops-app.git', branch: 'main'
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
                    source venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    source venv/bin/activate
                    pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Package Application') {
            steps {
                sh '''
                    deactivate || true
                    rm -rf venv
                    tar -czvf app-artifact.tar.gz app.py requirements.txt templates/ init_db.sql Jenkinsfile tests/
                '''
                archiveArtifacts artifacts: 'app-artifact.tar.gz', fingerprint: true
            }
        }

        stage('Upload Artifact to S3') {
            steps {
                sh 'aws s3 cp app-artifact.tar.gz s3://$S3_BUCKET/app-artifact.tar.gz'
            }
        }

        stage('Upload Artifact to Nexus') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'nexus-creds-id', usernameVariable: 'NEXUS_USERNAME', passwordVariable: 'NEXUS_PASSWORD')]) {
                    sh '''
                        curl -v -u ${NEXUS_USERNAME}:${NEXUS_PASSWORD} \
                             --upload-file app-artifact.tar.gz \
                             $NEXUS_URL/repository/$NEXUS_REPO/app-artifact.tar.gz
                    '''
                }
            }
        }

        stage('Ansible Deployment') {
            steps {
                dir('ansible') {
                    sh 'ansible-playbook -i dynamic_inventory.aws_ec2.yml playbooks/deploy_flask.yml'
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
