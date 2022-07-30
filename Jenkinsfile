library('slack-notifier@master')

pipeline {
  agent any
  options {
    ansiColor('xterm')
  }
  stages {
    stage('🏗️ Prepare environment') {
      steps {
        sh "python3.8 -m virtualenv venv"
      }
    }
    stage('📥 Install dependencies') {
      steps {
        script {
          sh "$PYTHON_ENV_CMD && python3.8 -m pip install --upgrade pip"
          sh "$PYTHON_ENV_CMD && make install"
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
  }
}
