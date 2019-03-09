pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'docker build -t paranuara-challenge-solution -f DOCKER .'
      }
    }
    stage('Test') {
      parallel {
        stage('Unit Tests') {
          steps {
            sh 'docker run -t --entrypoint /paranuara/api/test.sh --rm paranuara-challenge-solution'
          }
        }
        stage('Run') {
          steps {
            sh 'docker run -p 0.0.0.0:8383:8080 -dt --rm paranuara-challenge-solution'
          }
        }
      }
    }
  }
}