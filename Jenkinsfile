pipeline {
  agent any

  environment {
    VENV_DIR = 'venv'
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install dependencies') {
      steps {
        sh '''
          python3 -m venv $VENV_DIR
          . $VENV_DIR/bin/activate
          pip install -r requirements.txt
        '''
      }
    }

    stage('SonarQube Analysis') {
      environment {
        SONAR_SCANNER_OPTS = "-Xmx512m"
      }
      steps {
        withSonarQubeEnv('sonar') {
          sh '''
            . $VENV_DIR/bin/activate
            pip install coverage pytest
            coverage run -m pytest tests/
            coverage xml
            sonar-scanner \
              -Dsonar.projectKey=flask-devops-app \
              -Dsonar.python.coverage.reportPaths=coverage.xml
          '''
        }
      }
    }

    stage('Run Tests') {
      steps {
        sh '''
          . $VENV_DIR/bin/activate
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
            curl -u $NEXUS_USER:$NEXUS_PASS --fail \
              --upload-file app-artifact.tar.gz \
              http://35.183.72.244:8081/repository/flask-devops-artifacts/app-artifact.tar.gz
          '''
        }
      }
    }

    stage('Deploy with Ansible') {
      steps {
        withCredentials([[
          $class: 'AmazonWebServicesCredentialsBinding',
          credentialsId: 'aws-s3-creds'
        ]]) {
          sh '''
            export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
            export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

            ansible-playbook -i ansible/dynamic_inventory.aws_ec2.yml ansible/playbooks/deploy_flask.yml \
              --private-key /var/lib/jenkins/wood.pem || true
          '''
        }
      }
    }
  }
}

