/** PROJECT PROPERTIES
* project: Project Name
* gitUrl: Link repository
* branch: Branch Name exist in repository
* credentialID: Login to repository
* appName: Name of the app
* dockerHubRepo: Name of the repo/account that we push images
*/
def project = "Hackathon_devsecops"
def gitUrl = "https://github.com/tronglamitmo142/hackathon_devsecops"
def branch = "main"
def credentialID = "github-credentials"
def appName = "my-flask-app"
def dockerHubRepo = "lamnt67"

pipeline {

    /** agent
        * label: Agent name will execute pipeline
        * Because we use jenkins machine as agent, so when specify agent any
        Jenkins is automaticaly choosed as agent 
        */
    agent any

    environment {
        // Take value from global credentials
        def dockerPass=credentials("docker_password")
        // For easier manage, we specify the Build Version 
        def BUILDVERSION = sh(script: "echo `date +%s`", returnStdout: true).trim()
    }

    /** Checkout
    * Get source code from SVN, Git,...
    */
    stages {
        stage('Checkout') {
            steps {
                cleanWs() // Clean workspace before checkout
                checkout([$class: 'GitSCM',
                    branches: [[name: "${branch}"]],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [], gitTool: 'jgitapache', 
                    submoduleCfg: [],
                    userRemoteConfigs: [[credentialsId: "${credentialID}",
                        url: "${gitUrl}"]]
                ])
            }
        }
        stage('SAST Scan') {
            steps {
                sh """pip3 install semgrep"""
                sh """/var/lib/jenkins/.local/bin/semgrep scan --config=auto -o SAST_report.txt"""
            }
        }
        /** SCA
        * We use dependency-check plugin, the result is showed in dashboard of pipeline
        */
        stage('SCA') {
            steps {
                dependencyCheck additionalArguments: ''' 
                    -o "./" 
                    -s "./"
                    -f "ALL" 
                    --prettyPrint''', odcInstallation: 'dependency-check-8.2.1'

                dependencyCheckPublisher pattern: 'dependency-check-report.xml'
            }           
        }
        stage('Build') {
            steps {
                sh """docker build -q -t ${dockerHubRepo}/${appName}:${BUILDVERSION} ."""
            }
        }
        stage('Container Scanning') {
            steps {
                sh """trivy image --format cyclonedx --output result.cdx ${dockerHubRepo}/${appName}:${BUILDVERSION}"""
            }
        }
        stage('Push to Public Registry') {
            steps {
                sh """docker login -u ${dockerHubRepo} -p ${dockerPass}"""
                sh """ docker push ${dockerHubRepo}/${appName}:${BUILDVERSION} """
            }
        }
        stage('Deployment') {
            steps {
                script {
                    /// Get container port specify in Dockerfile
                    def port = sh(returnStdout: true, script: "grep -E '^EXPOSE' Dockerfile | awk '{print \$2}'").trim()
                    /// get containerId to check whether is port used or not
                    def containerId = sh(returnStdout: true, script: """docker ps --filter 'expose=${port}' --format '{{.ID}}'""").trim()
                    if (containerId) {
                        sh """docker rm -f ${containerId}"""
                        sh """docker network create network-${BUILDVERSION}"""
                        sh """docker run -d -p ${port}:${port} --net network-${BUILDVERSION} ${dockerHubRepo}/${appName}:${BUILDVERSION}"""
                    }
                    else {
                        sh """docker run -d -p ${port}:${port} --net network-${BUILDVERSION} ${dockerHubRepo}/${appName}:${BUILDVERSION}"""
                    }
                }
            }
        }
        stage('DAST') {
            steps {
                script {
                    /// We use ZAP as application deployed in container
                    /// We need to create docker network for communication between ZAP container and application container
                    def port = sh(returnStdout: true, script: "grep -E '^EXPOSE' Dockerfile | awk '{print \$2}'").trim()
                    def containerIp = sh(returnStdout: true, script: """ip -f inet -o addr show docker0 | awk '{print \$4}' | cut -d '/' -f 1""").trim()
                    sh """docker pull owasp/zap2docker-stable """
                    sh """docker run --name zap-${BUILDVERSION} --net network-${BUILDVERSION} -t -v ${env.WORKSPACE}:/zap/wrk/:rw owasp/zap2docker-stable zap-full-scan.py -I -j -m 1 -T 60 -t http://${containerIp}:${port} > DAST_report.txt || true"""
                    sh """docker rm -f zap-${BUILDVERSION} """
                }            
            }
        }
    }
}
