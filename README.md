# Jenkins - Shared Libraries, the Python way

## General

We are not going to dive deep into Shared Libraries in here, rather, we are going to see how to use python, as an example, to describe all the pipeline steps in a shared library and then use them within a Jenkinsfile. Our examples will us an Azure Storage Account, but naturally this method can be used for all type of resources, all types of clouds and any activity that needs to be reused in multiple ways with multiple starting conditions.

This allows a few improvements:

- We are using a small groovy wrapper that is VERY easy to understand and is required just to pass parameter values between the main pipeline and the python logic and functions.
- If your devs know python this is a lot easier to maintain and create engagement than forcing them to learn and understand groovy.
- If at any point in the future you ponder changing your CI server, the fact you moved ALL the logic into python and created an abstraction layer, will make the transition easier to an extent. You will just have to think mostly about variables and secrets.

This repository is made of two main sub folders:

- Three project folders, that will show the progress of moving from a simple pipeline to a more complex one that is using our shared library.
    -The first project will show implementation of the azure blob usage directly in the pipeline.
    -The second project will show the same actions using the shared library. Abstracting several elements like authentication and passing just the needed values as parameters.
    -The third project will show another usage of the shared libraries but in a more centralized governance using configuration files managed both in the project and in the shared library repository.

- sharedlib: This is where the code for the shared library exists. This would technically be in a differernt repository and you have already configured your Jenkins controller to use the repository for Shared Libraries.

## Azure Blob actions directly in Jenkinsfile

In project1 folder, we see using the environment block to declare environment variables that pick their values from Jenkins secrets. This can be done at the folder level that holds the Jenkins (more secure) or globally.

later we have the differernt stages that perform an authentication to Azure, downloading a file from a storage account, performing some changes to the content and uploading the file back to the storge account.

This script assumes, all your nodes have the AZ CLI installed on them and your authentication to Azure is done via a Service Principle and its Secret.

## Azure Blob actions via a shared library

The first example works well for one pipeline and for one storage account but in reality, you are bound to have more pipelines that need access to differernt Azure storage accounts and generally the power of shared libraries is the fact we can manage all the pipelines in a similar manner centrally allowing better reusability of tested and approved code to maintain security and governance.

In our Jenkinsfile, we have to declare our shared library. We have to use the shared library name as configured in Jenkins. In our example, we have used:

```groovy
@Library('azure-storage-lib@main') _
```

Then, in the download and upload stages, we called a function and supply some parameters to it.

```groovy
azblob("download", "my_account", "my_container", "name", "config.txt")
...
azblob("upload", "my_account", "my_container", "name", "config.txt")
```

We could have used 2 separate functions for each action, but since there is not a big difference between the expected passed parameters, it made sense to create one function, where the action, is passed as a parameter as well.

Notice the name of the function is 'azblob'. As per Jenkins documentation, this requires the shared library groovy file to be called the same way. Thus, if we look at the shared library code, under the 'vars' folder we will see 'azblob.groovy', this is the mandatory groovy file that will serve as a wrapper to call the python functions, present in the 'src' folder. Here the naming and structure can be as is fit, but for simplicity we will use the same names of the python files as the name of the function and groovy file.

If we look at 'azblob.groovy' we can see how we are calling the 'azblob.py' with the correct path structure and passing the variables we received from the Jenkinsfile. There should be no logic implemented in the groovy file to create that abstraction we mentioned at the start.

## Shared Library

The way this shared library was created is via python with a small groovy wrapper over it.

Note: for the code to work, you will have to make sure of the following:

-We are using Declarative pipelines. You should too!

-We are using the Service Principal Name and SPN Secret methods of authentication to Azure. Make sure you create three secrets in Jenkins called: azure_client_id, azure_client_secret and azure_tenant_id. Preferably create the secrets at the folder scope where the job is located or at the global scope.

-These examples do NOT use the Azure Credentials Jenkins plugin as it is going to stop being supported by Microsoft. You can of course
alter this slightly to adopt it but it is up to you. I will not be able to support in those cases where using the plugin will fail the overall pipeline execution.

-The node you are running the pipeline on, has to have the Azure CLI installed on it. If you have multiple nodes that can be potentially chosen, try to have the same version installed across the nodes.

## Future

This implementation deals with python, but can very much be used with other languages like PowerShell and Golang and more. The main thing to remember is that the node that runs the code, needs to support that programming language and have all the runtimes and library already installed.

As such, you have to remember that all these languages change over the years with new versions and new language changes and it is up to you to maintain and test properly before upgrades.
