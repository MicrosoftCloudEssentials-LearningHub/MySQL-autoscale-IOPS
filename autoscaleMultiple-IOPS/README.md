# Autoscale IOPS for multiple Azure MySQL Flexible Server

This automation uses [Python 3.7 or later](https://www.python.org/downloads/source/).

<details markdown="1">
<summary><b>Table of Content</b> (Click to expand)</summary>

- [Pre-requisites](#pre-requisites)
- [By Resource Group](#by-resource-group)
- [Across a Subscription](#across-a-subscription)
- [Run the automation scripts](#run-the-automation-scripts)

</details>

!!! note
    Use the Azure REST API to automate Autoscale IOPS. Azure CLI and PowerShell do not currently support this setting.

!!! warning
    Autoscale IOPS is available only for the `General Purpose` and `Business Critical` tiers. Burstable B-series servers such as B1ms do not support it.

## Pre-requisites

- Install azure-identity with: `py -m pip install azure-identity requests`

    <img width="550" alt="image" src="https://github.com/user-attachments/assets/fa74f47c-bef2-4ad3-8b0f-2ee50813c486" />

- [Install Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).

    <img width="550" alt="image" src="https://github.com/user-attachments/assets/3f552ecc-8e07-453a-9655-8bb5a89e1791" />

## By Resource Group

> Overall process: <br/> 
>
> - Automatically retrieves your **Azure subscription ID** using the Azure CLI. <br/>
> - List all Resource Groups in current subscription ID. <br/>
> - Prompts you only for the **resource group name**. <br/>
> - Lists all MySQL Flexible Servers in that resource group. Few conditions were added to review which servers are available for update. 
> - Sends a `PATCH request` to enable `autoIoScaling` for each server using the `Azure REST API`

Review the [resource-group automation script](https://github.com/Cloud2BR-MSFTLearningHub/MySQL-autoscale-IOPS/blob/main/autoscaleMultiple-IOPS/scripts/enable_autoscale_iops_byRG.py), then download it to your local machine.

> Example: enabling Autoscale IOPS on two different servers, each hosted in same resource group and same subscription.

<video controls width="700" aria-label="Enable Autoscale IOPS across servers in a resource group">
  <source src="https://github.com/user-attachments/assets/4c087afe-6fa1-40cb-bb2f-ef912edb974d" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Across a Subscription

> You can also enable autoscale IOPS across an entire subscription, overall process: <br/>
>
> - Listing all MySQL Flexible Servers in the subscription. <br/>
> - For each server, retrieving its resource group.  <br/>
> - Applying the update if the server is in a supported tier (General Purpose or Business Critical).  <br/>

Review the [subscription automation script](https://github.com/Cloud2BR-MSFTLearningHub/MySQL-autoscale-IOPS/blob/main/autoscaleMultiple-IOPS/scripts/enable_autoscale_iops_across_subscription.py), then download it to your local machine.

> Example: enabling Autoscale IOPS on different servers, each hosted in different resource group and same subscription.

<video controls width="700" aria-label="Enable Autoscale IOPS across a subscription">
  <source src="https://github.com/user-attachments/assets/7c06f457-d1c5-4277-ab1f-cee6621b6871" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Run the automation scripts

1. Download the [automation scripts](https://github.com/Cloud2BR-MSFTLearningHub/MySQL-autoscale-IOPS/tree/main/autoscaleMultiple-IOPS/scripts) to your local machine or Cloud Shell environment.
2. Make sure you're logged in: `az login`
3. Run the script: `python {script-name}.py`
