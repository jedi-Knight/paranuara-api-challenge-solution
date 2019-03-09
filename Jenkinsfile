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
        stage('Test') {
          steps {
            sh 'docker run -t --entrypoint /paranuara/api/test.sh paranuara-challenge-solution'
          }
        }
        stage('Run') {
          steps {
            sh 'docker run -p 127.0.0.1:8383:8080 -dit paranuara-challenge-solution'
          }
        }
      }
    }
  }
}