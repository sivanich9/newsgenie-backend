pipeline {
    agent any
       stages {
            stage('Git Pull stage') {
                steps {
                    git url: 'https://github.com/sivanich9/newsgenie-backend',
                    branch: 'main',
                    credentialsId : 'GithubCred'
                }
            }
            stage('Copy summarizing model') {
                steps {
                    script{
                        sh 'cp -r /var/lib/jenkins/simplet5-epoch-4-train-loss-0.6005-val-loss-1.6554 ./'
                    }
                }
            }
            stage('Install dependencies'){
                steps{
                    script{
                        sh '''
                            pip3 install simplet5
                            pip3 install "fastapi[all]"
                            pip3 install uvicorn
                            pip3 install loguru
                            pip3 install pymongo
                            pip3 install pytest
                            pip3 install mongomock
                        '''    
                    }    
                }
            }
            stage('Backend test'){
                steps{
                    script{
                        sh 'python3 -m pytest test_main.py --disable-warnings'
                    }    
                }
            }
            stage('Docker build image'){
                steps{
                    script{
                        sh 'docker build -t sivani4/newsgeniebackend:latest .'
                    }    
                }
            }
            stage('Push docker image'){
                steps{
                    script{
                        withDockerRegistry([ credentialsId: "dockercred", url: "" ]){
                            sh 'docker push sivani4/newsgeniebackend:latest'
                        }
                    }    
                }
            }
            stage('Ansible deploy'){
                steps{
                    script{
                        sh "/usr/bin/pip3 install docker"
                        sh "ansible-playbook p2.yml -i inventory"
                    }    
                }
            }
       }
}       
