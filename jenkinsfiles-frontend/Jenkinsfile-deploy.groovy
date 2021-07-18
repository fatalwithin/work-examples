//GIT_REPO_CREDENTIALS_ID= gitLabKeyForDeployKeysForEachProject
//GIT_HOST=git.sbear.ru
//CONFIG_SCOPE_NAME=configs
//SERVICE_NAME=cloud-ba-frontend-proj
//TARGET_CONFIG_BRANCH=dev
//REGISTRY_CREDENTIALS_ID=userNamePasswordJenkinsCredentialsForGitLab
//REGISTRY_HOST=git.sbear.ru:4567
//LANDSCAPE=dev
//SCOPE_NAME=cloudba
//TARGET_BRANCH=dev
//GIT_COMMIT_SHORT=aeb8c933
//NETWORK_NAME=cloudba-apps

node('backend') {
    stage('Get configs') {
        def scm
        def gitRepoUrl = "git@${GIT_HOST}:${CONFIG_SCOPE_NAME}/${SERVICE_NAME}.git"
        scm = checkout([
            $class: 'GitSCM',
            branches: [[name: "*/${TARGET_CONFIG_BRANCH}"]],
            doGenerateSubmoduleConfigurations: false,
            extensions: [],
            submoduleCfg: [],
            userRemoteConfigs: [
                [credentialsId: env.GIT_REPO_CREDENTIALS_ID, url: gitRepoUrl]
            ]
        ])
        stash includes: 'default.conf', name: 'nginxDefConf'
    }

    stage('Copy configs') {
        dir('/opt/cloudba/frontend') {
            unstash 'nginxDefConf'
        }
    }

//    stage('Get Deploy Scenario') {
//        def scm
//        def gitRepoUrl = "git@${GIT_HOST}:devops/cloudba-frontend.git"
//        scm = checkout([
//            $class: 'GitSCM',
//            branches: [[name: "*/dev"]],
//           doGenerateSubmoduleConfigurations: false,
//            extensions: [],
//            submoduleCfg: [],
//            userRemoteConfigs: [
//                [credentialsId: env.GIT_REPO_CREDENTIALS_ID, url: gitRepoUrl]
//            ]
//        ])
//        unstash "serviceConfigs"
//    }

    stage('Prepare env') {
        try {
            sh 'docker network create  ${NETWORK_NAME}'
        } catch(e1) {
            echo "Network ${NETWORK_NAME} already exist. Deploy processing..."
        }
    }
    def imageName = "${SCOPE_NAME}/${SERVICE_NAME}/${LANDSCAPE}"

    stage('Pull image') {
        docker.withRegistry("https://${REGISTRY_HOST}", env.REGISTRY_CREDENTIALS_ID) {
            docker.image(imageName).pull()
        }
    }
    env.IMAGE_NAME = "${REGISTRY_HOST}/${imageName}"

    stage('Run service') {
        try {
            sh "docker run \
                --name frontend \
                -p 8081:80 \
                --net ${NETWORK_NAME} \
                -d \
                --restart=always \
                -v /opt/cloudba/frontend/default.conf:/etc/nginx/conf.d/default.conf \
                ${REGISTRY_HOST}/${imageName}"
        } catch(e1) {
            echo "Can`t update service. Try recreate..."
            sh "docker rm -f frontend"
            sh "docker run \
                --name frontend \
                -p 8081:80 \
                --net ${NETWORK_NAME} \
                -d \
                --restart=always \
                -v /opt/cloudba/frontend/default.conf:/etc/nginx/conf.d/default.conf \
                ${REGISTRY_HOST}/${imageName}"
        }

    }

//    stage('Clean workspace') {
//        cleanWs()
    //     deleteDir()
    //     dir("${env.WORKSPACE}") {
    //       deleteDir()
    //     }
    //     dir("${env.WORKSPACE}@tmp") {
    //       deleteDir()
    //     }
    // }
}
