import subprocess
import json

def get_pipeline_credentials(pipeline_name):
    with open('..\..\resources\azblob_config.json', 'r') as config_file:
        config = json.load(config_file)['blob_auth']

    spn = credentials(config[pipeline_name]["spn_id"])
    secret = credentials(config[pipeline_name]["spn_secret"])
    tenant = credentials(config[pipeline_name]["tenant_id"])
    return spn, secret, tenant

def check_resource(storage_account_name, container_name, file_name)
    # check that resource exists via function. (vnext).
    return True

def azure_storage_operation(storage_account_name, container_name, file_name, operation, pipeline_name):
    spn, secret, tenant = get_pipeline_credentials(pipeline_name)

    command = f"az login --service-principal -u {spn} -p {secret} --tenant {tenant}"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        print('Error: Autentication has failed. Please check the credentials.')

    # check that resource exists via function. (vnext).
    if check_resource(storage_account_name, container_name, file_name) == True:
        if operation == "upload":
            command = f"az storage blob upload --account-name {storage_account_name} --container-name {container_name} --file {file_name}"
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError:
                print('Error: Uploading file to blob failed. Please check supplied parameters.')
        elif operation == "download":
            command = f"az storage blob download --account-name {storage_account_name} --container-name {container_name} --file {file_name}"
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError:
                print('Error: Downloading a file from blob failed. Please check supplied parameters')
        else:
            print("Error: Invalid operation. Please specify either 'upload' or 'download' as the operation.")
    else:
        print("Error: Resource does not exist. Please check supplied parameters.")
