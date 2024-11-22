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
        stage("try Insert Database"){
            steps {
                sh(script:'''
                    mysql -N -u ${CRED_USR} -p${CRED_PSW} ainur_tesdb -e "INSERT into random(nama,alamat) VALUES ('Bayu','Bandung')"
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
