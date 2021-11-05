pipeline{
    agent any

    stages{
        stage('Static code analysing') {
            stages {
                stage('Install dependencies') {
                    steps {
                        sh 'pip3 install --upgrade pipenv'
                        sh 'pipenv install --pre --dev'
                    }
                }
            }
        }
    }

}
