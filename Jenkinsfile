pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'docker build -t paranuara-challenge-solution -f DOCKER .'
      }
    }
    stage('Run') {
      steps {
        sh 'docker run -p 0.0.0.0:8383:8080 -dt --name paranuara-challenge-solution --rm paranuara-challenge-solution'
      }
    }
    stage('Unit Tests and API Test') {
      steps {
        sh 'docker run -t --name paranuara-challenge-solution-tests --entrypoint /paranuara/api/test.sh --rm paranuara-challenge-solution'
      }
    }
  }
}