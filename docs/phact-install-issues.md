25-02-2025:
During running azd up, the nodejs version (via npm?) was not okay. Fixed it this way (link:https://askubuntu.com/questions/426750/how-can-i-update-my-nodejs-to-the-latest-version):
    sudo npm cache clean -f
    sudo npm install -g n
    sudo n stable

26-02-2025:
Using the dev container gives lots of problems with deploying for example:
    pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available...
So do not use the dev container!

26-02-2025:
After a clean install, set the following environment vars:
# For gpt-4o
azd env set AZURE_OPENAI_CHATGPT_DEPLOYMENT <your-deployment-name>
azd env set AZURE_OPENAI_CHATGPT_MODEL gpt-4o
azd env set AZURE_OPENAI_CHATGPT_DEPLOYMENT_SKU GlobalStandard
azd env set AZURE_OPENAI_CHATGPT_DEPLOYMENT_CAPACITY 10
azd env set AZURE_OPENAI_CHATGPT_DEPLOYMENT_VERSION 2024-05-13

# For embedding-3 models
azd env set AZURE_OPENAI_EMB_MODEL_NAME text-embedding-3-large
azd env set AZURE_OPENAI_EMB_DIMENSIONS 256
azd env set AZURE_OPENAI_EMB_DEPLOYMENT_VERSION 1

# Enabling authentication
azd env set AZURE_USE_AUTHENTICATION true
azd env set AZURE_ENFORCE_ACCESS_CONTROL true
azd env set AZURE_ENABLE_GLOBAL_DOCUMENT_ACCESS true
azd env set AZURE_AUTH_TENANT_ID <YOUR-TENANT-ID>

# Enabling Data Lake Gen2 storage
Do the following after azd up has been successfully executed with an empty data folder
-azd env set AZURE_ADLS_GEN2_STORAGE_ACCOUNT ste3blc4xnteeuu
-azd env AZURE_ADLS_GEN2_FILESYSTEM="gptkbcontainer"
-azd env AZURE_ADLS_GEN2_FILESYSTEM_PATH="sales" or other folder you want to upload
-On the storage account on the azure portal, turn off the "soft-delete" option under "Data Protection"
-On the storage account, create the specified container named after the file system and create the specified directory, named after the file system path. Put some data in the directory or else it wont be created
-On the storage account on the azure portal, upgrade the storage account to an account with Azure Data Lake Gen2 capabilities.
-Add the role "Storage Blob Data Owner" in the storage account to the user that requests this access ("Johan Kleuskens and the mananged identity in this case ...)
-Run the command :python ./scripts/manageacl.py -v --acl-action enable_acls to create group and oid attributes in Search AI ???

## --- maybe
run pip install -r app/backend/requirement.txt to install necessary packages
run python ./scripts/adlsgen2setup.py './data' --data-access-control './scripts/sampleacls.json' -v
## --- end maybe

27-0202-25:
Stategy for uploading documents:
    - Keep data folder in app empty.
    - Upload documents (PFD only?) into data lake and setup ACL
    - run prepdocs script
    - Upload documents to root of blob container for making reference in chat work
    - Delete docs in data lake?
    - The Azure Storage Explorer tool (https://azure.microsoft.com/en-us/products/storage/storage-explorer) is a great tool to manage ACL on files and directories
