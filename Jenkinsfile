pipeline{
    agent any
    environment{
           DB_HOST = "${Math.abs(new Random().nextInt(1000+1))}_db_user"
    }

    stages{
        stage('Static code analysing') {
            stages {
                stage('Install dependencies')
                {
                    steps {
                        sh 'pip3 install --upgrade pipenv'
                        sh 'pipenv install --pre --dev'
                    }
                }
                stage ('PyDocStyle') {
                    steps {
                        sh 'pipenv run pydocstyle --config=.pydocstyle.ini ${MODULE_DIR_NAME}'
                    }
                }

                stage ('Mypy') {
                    steps {
                        sh 'pipenv run mypy -p installation_requests --config-file mypy.ini --no-incremental'
                    }
                }

                stage ('Pylint') {
                    steps {
                        sh 'pipenv run pylint installation_requests --output-format=parseable  --rcfile=.pylintrc'
                    }
                }
            }
        }

        stage('Start DB'){
            steps("launch psql container"){
                script{
                    def inspectExitCode = sh script: "docker container inspect ${DB_HOST}", returnStatus: true
                    if (inspectExitCode == 0) {
                        echo "container already up"
                    }
                    else {
                        dir('dev_scripts/docker'){
                            sh "docker run -d --rm --network=traefik_default --name ${DB_HOST} --env-file .env  -v \"\$(pwd)\"/initDB:/docker-entrypoint-initdb.d postgres:13 "
                        }
                    }
                }
            }
        }

        stage('Unit-test'){
            steps('Unit test'){
                sh "wait-for-it -p 5432 -h ${DB_HOST} -t 30 && pipenv run coverage run --source=installation_requests -m pytest -v --junit-xml=reports/report.xml  tests && pipenv run coverage xml"
            }

        }
        stage('build && SonarQube analysis') {
            environment {
                scannerHome = tool 'SonarQubeScanner'
            }
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh "echo $PATH & echo $JAVA_HOME"
                    sh "${scannerHome}/bin/sonar-scanner"
                }
            }
        }
        stage("Quality Gate") {
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    // Parameter indicates whether to set pipeline to UNSTABLE if Quality Gate fails
                    // true = set pipeline to UNSTABLE, false = don't
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage("Publish") {
            when {
                expression { BRANCH_NAME ==~ /(master|develop)/ }
            }
            environment {
                registryCredential = 'dockerhub'
                app_regisgtry = 'myem/installation-requests'
                IMG_TAG = "${env.BRANCH_NAME == "master" ? "preprod" : "staging"}"
            }
            steps{
               script {
                    docker.withRegistry( '', registryCredential ) {
                        // we copy files inside the app image and tag it
                        def appimage = docker.build(app_regisgtry + ":${IMG_TAG}", "--no-cache . -f ci/Dockerfile " )
                        appimage.push("${IMG_TAG}")
                    }
               }
            }

        }
//         stage("Deploy") {
//             when {
//                  expression { BRANCH_NAME ==~ /(master|develop)/ }
//             }
//             environment {
//                 AWS_SSH_KEY = credentials('aws-server-ssh-private-key')
//                 AWS_IP = ' ec2-35-181-118-48.eu-west-3.compute.amazonaws.com'
//                 AWS_USER = 'ubuntu'
//                 ENV_NAME = "${env.BRANCH_NAME == "master" ? "preprod" : "staging"}"
//             }
//             steps {
//                 sh "./ci/deploy.sh ${AWS_USER} ${AWS_IP} ${AWS_SSH_KEY} /home/${AWS_USER}/installation-requests-devops/${ENV_NAME}"
//            }
//         }
    }
    post{
        always{
            echo "build finished"
            sh "docker stop ${DB_HOST}"
            junit 'reports/*.xml'

        }
    }

}
