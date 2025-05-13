"""
Azure MySQL Flexible Server Auto IOPS Enabler

This script connects to Azure using the Azure CLI and Azure REST API to:
1. Retrieve the current subscription ID.
2. List all Resource Groups in the current subscription.
3. List all MySQL Flexible Servers in each resource group.
4. Skip resource groups with no MySQL Flexible Servers.
5. Check if each server is eligible for Auto IOPS scaling (only GeneralPurpose or BusinessCritical tiers).
6. Optionally enable Auto IOPS scaling if not already enabled.
7. Print a summary of which servers were updated or skipped.
"""

import subprocess
import requests
import shutil
from azure.identity import AzureCliCredential

SUPPORTED_TIERS = {"GeneralPurpose", "BusinessCritical"}

def mask_value(value, start=4, end=4):
    return value[:start] + '*' * (len(value) - start - end) + value[-end:]

def get_subscription_id():
    az_path = shutil.which("az")
    if az_path is None:
        raise FileNotFoundError("Azure CLI (az) not found in system PATH.")
    result = subprocess.check_output([az_path, "account", "show", "--query", "id", "-o", "tsv"], text=True)
    return result.strip()

def get_access_token():
    credential = AzureCliCredential()
    token = credential.get_token("https://management.azure.com/.default")
    return token.token

def list_resource_groups(subscription_id, access_token):
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourcegroups?api-version=2024-06-01-preview"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def list_mysql_servers(subscription_id, resource_group, access_token):
    url = (
        f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/"
        f"{resource_group}/providers/Microsoft.DBforMySQL/flexibleServers?api-version=2024-06-01-preview"
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        return {"value": []}
    response.raise_for_status()
    return response.json()

def get_server_config(subscription_id, resource_group, server_name, access_token):
    url = (
        f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/"
        f"providers/Microsoft.DBforMySQL/flexibleServers/{server_name}?api-version=2024-06-01-preview"
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def enable_auto_io_scaling_put(subscription_id, resource_group, server_name, access_token):
    url = (
        f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/"
        f"providers/Microsoft.DBforMySQL/flexibleServers/{server_name}?api-version=2024-06-01-preview"
    )
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "properties": {
            "storage": {
                "autoIoScaling": "Enabled"
            }
        }
    }
    response = requests.patch(url, headers=headers, json=payload)
    print(f"PATCH Response: {response.status_code} - {response.text}")
    response.raise_for_status()
    return response.json()

def main():
    try:
        print("Script started")
        subscription_id = get_subscription_id()
        print(f"Using subscription: {mask_value(subscription_id)}")

        access_token = get_access_token()
        print(f"Access Token: {mask_value(access_token[:10])}...")

        resource_groups = list_resource_groups(subscription_id, access_token)
        eligible_servers = []
        ineligible_servers = []

        for rg in resource_groups.get("value", []):
            rg_name = rg["name"]
            servers = list_mysql_servers(subscription_id, rg_name, access_token).get("value", [])

            if not servers:
                print(f"[SKIP] No MySQL Flexible Servers found in resource group: {rg_name}")
                continue

            print(f"\nMySQL Flexible Servers in {rg_name}:")
            for server in servers:
                print(f"  - {server['name']}")

            target_server = input(f"Enter a specific server name in {rg_name} (or press Enter to apply to all): ").strip()

            for server in servers:
                server_name = server["name"]
                if target_server and server_name.lower() != target_server.lower():
                    continue

                config = get_server_config(subscription_id, rg_name, server_name, access_token)
                tier = config["sku"]["tier"]
                auto_io = config["properties"]["storage"].get("autoIoScaling", "Disabled")

                if tier not in SUPPORTED_TIERS:
                    ineligible_servers.append((server_name, tier))
                    continue

                if auto_io == "Enabled":
                    print(f"[SKIP] Auto IOPS already enabled for {server_name}")
                    continue

                print(f"[UPDATE] Enabling Auto IOPS for {server_name} (Tier: {tier})...")
                enable_auto_io_scaling_put(subscription_id, rg_name, server_name, access_token)
                eligible_servers.append(server_name)

        print("\nSummary:")
        if eligible_servers:
            print("Auto IOPS enabled for:")
            for name in eligible_servers:
                print(f"  - {name}")
        else:
            print("No servers were updated.")

        if ineligible_servers:
            print("\nIneligible servers (unsupported tier):")
            for name, tier in ineligible_servers:
                print(f"  - {name} (Tier: {tier})")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
