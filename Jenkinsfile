pipeline {
    agent none 
    stages {
	    stage('Unit tests') {
            agent {
                dockerfile {
		            filename 'DF_python36_selenium_pytest'
                    }
            }
            steps {
                sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_calc.py'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
        stage('Deliver (Linux)') {
            agent {
                dockerfile {
		            filename 'DF_pyinstaller_ubuntu'
                    }
            }
            steps {
                dir("sources") {
                    sh 'rm -rf ./dist'
                    sh 'rm -rf ./build'
		    sh 'pyinstaller backend.py --hidden-import bottle_websocket --add-data "eel.js:eel" --add-data "web/**:web" --add-data "web/additions_diary.html:web" --add-data "web/__target__/frontendscrypt.js:web/__target__" --add-data "web/__target__/org.transcrypt.__runtime__.js:web/__target__" --add-data "web/__target__/frontendscrypt.options:web/__target__" --onefile'
                    sh 'chmod +x dist/backend'
                }
            }
            post {
                success {
			stash includes: 'sources/dist/backend', name: 'linuxbuilt'
                    archiveArtifacts 'sources/dist/backend'
                }
            }
        }
        stage('Deliver (Windows)') {
            agent {
                dockerfile {
		            filename 'DF_pyinstaller_windows'
                    }
            }
		steps {
			dir("sources") {
				sh 'pip install $(grep -iE "eel" requirements.txt) 2>&1 | cat' // to complete windows that can't install eel with git
				sh 'rm -rf ./dist 2>&1 | cat'
				sh 'rm -rf ./build 2>&1 | cat'
				sh 'pyinstaller backend.py -n backend.exe --hidden-import bottle_websocket --add-data "eel.js;eel" --add-data "web/**;web" --add-data "web/additions_diary.html;web" --add-data "web/__target__/frontendscrypt.js;web/__target__" --add-data "web/__target__/org.transcrypt.__runtime__.js;web/__target__" --add-data "web/__target__/frontendscrypt.options;web/__target__" --onefile 2>&1 | cat'
				sh 'chmod +x dist/backend.exe'
		}
            }
            post {
                success {
                    archiveArtifacts 'sources/dist/backend.exe'
                }
            }
        }
	stage('Integration Test (Linux)'){
            agent {
                dockerfile {
		            filename 'DF_python36_selenium_pytest'
                    }
            }
            steps {
	    			unstash 'linuxbuilt'
				sh './sources/dist/backend &'
				sh 'py.test sources/test_web.py --driver Chrome --verbose --junit-xml test-reports/results.xml'
		}
	    post {
		always {
		    junit 'test-reports/results.xml'
		}
	    }
	
	}
    }
}
