pipeline {
    agent any
    
    environment{
        TOKEN = credentials('mfanobot-token')
        CHAT_ID = credentials('ainur-tele')
        
        CRED = credentials('db-test')
    }

    stages {
        stage('Tes') {
            steps {
                git url: "https://github.com/eipiriru/ci-cd-mfano.git", branch:'main' 
                echo "Hello Test"
                sh "pwd"
                sh "ls -l"
            }
        }
        stage("Coba Insert Database dari File yang dipush"){
            steps {
                sh(script:'''
                    changes=$(git diff --name-only main~ main sql/)
                    for i in $changes
                        do
                          mysql -N -u ${CRED_USR} -p${CRED_PSW} ainur_tesdb -e "source $i"
                        done
                ''')
            }
        }
    }
    post {
        always{
            script{
                sh "curl --location --request POST 'https://api.telegram.org/bot${TOKEN}/sendMessage' --form text='ALWAYS SEND FOR YOU HAHAH' --form chat_id='${CHAT_ID}'"
            }
        }
        success {
            echo "Job Success"
        }
    }
}
