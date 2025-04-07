pipeline {
  agent any

<<<<<<< HEAD
  environment {
    SONARQUBE = 'sonar'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout([$class: 'GitSCM',
          branches: [[name: '*/main']],
          userRemoteConfigs: [[url: 'https://github.com/tobaina/flask-devops-app.git']]
        ])
      }
    }

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
        withSonarQubeEnv("${env.SONARQUBE}") {
          sh '''
            . venv/bin/activate
            pip install coverage pytest
            coverage run -m pytest tests/
            coverage xml
            sonar-scanner -Dsonar.projectKey=flask-devops-app -Dsonar.python.coverage.reportPaths=coverage.xml
          '''
=======
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
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    ./venv/bin/pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Package Application') {
            steps {
                sh '''
                    ./venv/bin/python setup.py sdist
                '''
                archiveArtifacts artifacts: 'dist/*.tar.gz', fingerprint: true
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

    post {
        always {
            // Temporarily commented out to preserve workspace for troubleshooting
            // cleanWs()
>>>>>>> e833e89 (chore: added project credits and updated Jenkinsfile)
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
        sh '''
          tar -czf app-artifact.tar.gz app.py requirements.txt templates init_db.sql Jenkinsfile tests
        '''
      }
    }

    stage('Upload to S3') {
      steps {
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-s3-creds']]) {
          sh '''
            aws s3 cp app-artifact.tar.gz s3://flask-devops-artifacts-tobaina/builds/app-artifact.tar.gz
          '''
        }
      }
    }

    stage('Upload to Nexus') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'nexus-creds', usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASS')]) {
          sh '''
            curl -u $NEXUS_USER:$NEXUS_PASS --fail --upload-file app-artifact.tar.gz http://35.183.72.244:8081/repository/flask-devops-artifacts/app-artifact.tar.gz
          '''
        }
      }
    }

    stage('Deploy with Ansible') {
      steps {
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-s3-creds']]) {
          sh '''
            export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
            export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
            ansible-playbook \
              -i ansible/dynamic_inventory.aws_ec2.yml \
              ansible/playbooks/deploy_flask.yml \
              -u ec2-user \
              --private-key /var/lib/jenkins/wood.pem
          '''
        }
      }
    }
  }
}
