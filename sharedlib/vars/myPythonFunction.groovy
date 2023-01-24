def call(body) {
    def config = [:]
    body.resolveStrategy = Closure.DELEGATE_FIRST
    body.delegate = config
    body()

    def myPythonFunction(functionName) {
        sh "python myPythonFile.py ${functionName}"
    }
}