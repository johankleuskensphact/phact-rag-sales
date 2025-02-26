25-02-2025:
During running azd up, the nodejs version (via npm?) was not okay. Fixed it this way (link:https://askubuntu.com/questions/426750/how-can-i-update-my-nodejs-to-the-latest-version):
    sudo npm cache clean -f
    sudo npm install -g n
    sudo n stable

26-02-2025:
After a clean install, set the following environment vars:
# For gpt-4o
azd env set AZURE_OPENAI_CHATGPT_DEPLOYMENT <your-deployment-name>
azd env set AZURE_OPENAI_CHATGPT_MODEL gpt-4o
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