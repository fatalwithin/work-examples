//SERVICE_NAME=cloud-ba-frontend-proj
//SCOPE_NAME=cloudba
//CONFIG_SCOPE_NAME=configs
//TARGET_CONFIG_BRANCH=dev
//REGISTRY_HOST=git.sbear.ru:4567
//REGISTRY_CREDENTIALS_ID= userNamePasswordJenkinsCredentialsForGitLab
//GIT_HOST=git.sbear.ru
//GIT_REPO_CREDENTIALS_ID= gitLabKeyForDeployKeysForEachProject
//LANDSCAPE=dev
//TARGET_BRANCH=develop

node {
    def scm
    def gitRepoUrl = "git@${GIT_HOST}:${SCOPE_NAME}/${SERVICE_NAME}.git"
    stage('Clone repository') {
        dir("${env.WORKSPACE}/app") {
            scm = checkout([
                $class: 'GitSCM',
                branches: [[name: "*/${TARGET_BRANCH}"]],
                doGenerateSubmoduleConfigurations: false,
                extensions: [],
                submoduleCfg: [],
                userRemoteConfigs: [
                    [credentialsId: env.GIT_REPO_CREDENTIALS_ID, url: gitRepoUrl]
                ]
            ])
//        }
//        dir("${env.WORKSPACE}/app") {
          env.GIT_COMMIT = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
          sh"git rev-parse --short HEAD"
//        }
        env.GIT_COMMIT_SHORT = env.GIT_COMMIT.substring(0,8)
    }
}
    

    def imageName = "${SCOPE_NAME}/${SERVICE_NAME}/${LANDSCAPE}:${TARGET_BRANCH}-${GIT_COMMIT_SHORT}"
    env.TARGET_IMAGE_NAME = imageName

    stage('Get configs') {
        dir("${env.WORKSPACE}/configs") {
            def configScm
            def configGitRepoUrl = "git@${GIT_HOST}:${CONFIG_SCOPE_NAME}/${SERVICE_NAME}.git"
            configScm = checkout([
                $class: 'GitSCM',
                branches: [[name: "*/${TARGET_CONFIG_BRANCH}"]],
                doGenerateSubmoduleConfigurations: false,
                extensions: [],
                submoduleCfg: [],
                userRemoteConfigs: [
                    [credentialsId: env.GIT_REPO_CREDENTIALS_ID, url: configGitRepoUrl]
                ]
            ])
            stash includes: '.env', name: 'envFile'
        }
    }

    stage('Copy configs') {
        dir("${env.WORKSPACE}/app/cloud-ba-frontend") {
            unstash 'envFile'
        }
    }


    stage('Build') {
        dir("${env.WORKSPACE}/app") {
            script {
                docker.build(imageName)
            }
        }
    }

    stage('Push') {
       script {
            docker.withRegistry("https://${REGISTRY_HOST}", env.REGISTRY_CREDENTIALS_ID) {
                docker.image(imageName).push()
                docker.image(imageName).push('latest')
            }
        }
    }

    stage('Clean builds') {
        sh 'docker rmi -f ${TARGET_IMAGE_NAME}'
        sh 'docker rmi -f ${REGISTRY_HOST}/${TARGET_IMAGE_NAME}'
    }

//    stage('Clean workspace') {
//        cleanWs()
//        deleteDir()
//        dir("${env.WORKSPACE}@2") {
//          deleteDir()
//        }
//        dir("${env.WORKSPACE}@tmp") {
//          deleteDir()
//        }
//        dir("${env.WORKSPACE}@script@tmp") {
//          deleteDir()
//        }
//        dir("${env.WORKSPACE}@script") {
//          deleteDir()
//        }
//        dir("${env.WORKSPACE}@2@tmp") {
//          deleteDir()
//        }
//    }
}

