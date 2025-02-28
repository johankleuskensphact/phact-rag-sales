import argparse
import asyncio
import logging

from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient

import manageacl

logger = logging.getLogger("scripts")

# Azure Blob Storage configuration
#account_url = "https://stl7xzhvezfc52c.blob.core.windows.net"
#container_name = "content"

account_url = "https://stc2ohx2fbixllg.blob.core.windows.net"
container_name = "gptkbcontainer"

# Authenticate using Entra ID (Azure AD)
credential = DefaultAzureCredential()

# Initialize the ContainerClient
container_client = ContainerClient(account_url, container_name, credential=credential)

# List all blobs (files) in the container
blob_references = [blob.name for blob in container_client.list_blobs()]

# Generate a list of full HTTPS references to the blobs
blob_urls = [f"{account_url}/{container_name}/{blob.name}" for blob in container_client.list_blobs()]

# Create arguments to simulate calling:  python ./scripts/manageacl.py -v --acl-type groups --acl-action view --url https://.....
parser = argparse.ArgumentParser(
    description="Manage ACLs in a search index",
    epilog="Example: manageacl.py --acl-action enable_acls",
)
parser.add_argument(
    "--search-key",
    required=False,
    help="Optional. Use this Azure AI Search account key instead of the current user identity to login",
)
parser.add_argument("--acl-type", required=False, choices=["oids", "groups"], help="Optional. Type of ACL")
parser.add_argument(
    "--acl-action",
    required=False,
    choices=["remove", "add", "view", "remove_all", "enable_acls", "update_storage_urls", "check_chunks"],
    help="Optional. Whether to remove or add the ACL to the document, or enable acls on the index",
)
parser.add_argument("--acl", required=False, default=None, help="Optional. Value of ACL to add or remove.")
parser.add_argument("--url", required=False, help="Optional. Storage URL of document to update ACLs for")
parser.add_argument(
    "--tenant-id", required=False, help="Optional. Use this to define the Azure directory where to authenticate)"
)
parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

logging.basicConfig(level=logging.WARNING, format="%(message)s")
# We only set the level to INFO for our logger,
# to avoid seeing the noisy INFO level logs from the Azure SDKs
logger.setLevel(logging.INFO)

# Print the acl-groups of all documents in blob storage
for blob_url in blob_urls:
    # urls from data lake have "dfs" in their url, not "blob"
    blob_url = "%2F".join(blob_url.rsplit("/", 1)).replace("blob","dfs").replace(" ","%20")
    #Fill arguments programatically
    args = parser.parse_args(['--acl-type', 'groups', '--acl-action', 'check_chunks', '--url',f'{blob_url}'])
    asyncio.run(manageacl.main(args))
