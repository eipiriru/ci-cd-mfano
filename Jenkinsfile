pipeline {
    agent any
    
    environment{
        // CREDENTIAL TELEGRAM
        TOKEN = credentials('mfanobot-token')
        CHAT_ID = credentials('ainur-tele')
        
        // CREDENTIAL DATABASE
        CRED = credentials('db-test')
        
        
        // Telegram Message Pre Build
        TEXT_PRE_BUILD = "${JOB_NAME} is Building"

        // Telegram Message Success and Failure
        TEXT_SUCCESS_BUILD = "${JOB_NAME} is Success"
        TEXT_FAILURE_BUILD = "${JOB_NAME} is Failure"
    }

    stages {
        stage('Github Check') {
            steps {
                git url: "https://github.com/eipiriru/ci-cd-mfano.git", branch:'main' 
                sh "curl --location --request POST 'https://api.telegram.org/bot${TOKEN}/sendMessage' --form text='${TEXT_PRE_BUILD}' --form chat_id='${CHAT_ID}'"
            }
        }
        stage("Coba Insert Database dari File yang dipush"){
            steps {
                sh(script:'''
                    changes=$(git diff --name-only main~ main sql/)
                    for i in $changes
                        do
                          mysql -N -u ${CRED_USR} -p${CRED_PSW} ainur_tesdb -e "source $i"
                          curl --location --request POST 'https://api.telegram.org/bot${TOKEN}/sendMessage' --form text='Execute $i' --form chat_id='${CHAT_ID}'
                        done
                ''')
            }
        }
    }
    post {
        always{
            script{
                sh "curl --location --request POST 'https://api.telegram.org/bot${TOKEN}/sendMessage' --form text='Jobs End' --form chat_id='${CHAT_ID}'"
            }
        }
        success {
            script{
                sh "curl --location --request POST 'https://api.telegram.org/bot${TOKEN}/sendMessage' --form text='${TEXT_SUCCESS_BUILD}' --form chat_id='${CHAT_ID}'"
            }
        }
        failure {
            script{
                sh "curl --location --request POST 'https://api.telegram.org/bot${TOKEN}/sendMessage' --form text='${TEXT_FAILURE_BUILD}' --form chat_id='${CHAT_ID}'"
            }
        }
    }
}
