#!/usr/bin/groovy

boolean continuePipeline = false
def nodeLabel = 'ci-python-35'

jenkinsTemplate(nodeLabel, ['docker', 'python35']) {
    node(nodeLabel) {
        checkout scm

        stage('Install jenkins dependencies') {
            container('python') {
                sh 'pip install setuptools pylint pep8 coverage pytest'
            }
        }

        stage('Running tests') {
            container('python') {
                parallel(
                    'Unit tests': {
                        sh 'python setup.py test'
                        sh 'coverage xml -o coverage.xml'
                    },
                    'PEP8': {
                        sh 'pep8 --max-line-length=99 rest_framework_digestauth > pep8.report || true'
                    },
                    'Pylint': {
                        sh 'pylint rest_framework_digestauth > pylint.report || true'
                    }
                )
            }
        }
        helpers.publishResults()
    }


    if (env.BRANCH_NAME == 'master') {
        continuePipeline = true
    }

    if(continuePipeline) {
        stage('Approval') {
            timeout(time:1, unit:'HOURS') {
                input message:'Approve upload on pypi?'
                continuePipeline = true
            }
        }

        node(nodeLabel) {
            checkout scm

            stage ('Building package') {
                container('python') {
                    sh 'python setup.py sdist'
                }
            }

            stage ('Publish on PyPi') {
                withCredentials([file(credentialsId: 'pypirc', variable: 'pypirc')]) {
                    container('python') {
                        sh 'pip install twine'
                        sh "twine upload --config-file $pypirc --repository internal dist/*"
                    }
                }
            }
        }
    }
}
