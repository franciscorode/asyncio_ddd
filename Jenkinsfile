library('slack-notifier@master')

pipeline {
  agent any
  options {
    ansiColor('xterm')
  }
  stages {
    stage('🏗️ Prepare environment') {
      steps {
        sh "python3.10 -m venv venv"
      }
    }
    stage('📥 Install dependencies') {
      steps {
        script {
          sh "$PYTHON_ENV_CMD && python3.10 -m pip install --upgrade pip"
          sh "$PYTHON_ENV_CMD && make install"
        }
      }
    }
    stage('🐋 Up docker containers') {
      steps {
        script {
          sh "make up"
        }
      }
    }
    stage('✅ Run tests') {
      steps {
        script {
          sh "$PYTHON_ENV_CMD && make test"
        }
      }
    }
    stage('🎣 Record reports') {
      steps {
        junit(testResults: 'output/tests/tests.xml')
        cobertura(coberturaReportFile: 'output/coverage/coverage.xml')
      }
    }
  }
  post {
    fixed {
      notifyFixedBuild()
    }
    failure {
      notifyFailedBuild()
    }
    cleanup {
      cleanWs()
    }
    always {
      sh "make down || true"
    }
  }
}
