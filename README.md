# Azure MySQL Autoscale IOPS - Overview 

IOPS stands for **Input/Output Operations Per Second**.

<details markdown="1">
<summary><b>List of References</b> (Click to expand)</summary>

- [Storage IOPS in Azure Database for MySQL - Flexible Server](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concepts-storage-iops#how-do-i-know-that-iops-have-scaled-up-and-scaled-down-when-the-server-is-using-the-autoscale-iops-feature-can-i-monitor-iops-usage-for-my-server)
- [Azure Database for MySQL - Flexible Server service tiers](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concepts-service-tiers-storage#service-tiers-size-and-server-types)
- [Autoscale IOPS for Azure Database for MySQL - Flexible Server - General Availability](https://techcommunity.microsoft.com/blog/adformysql/autoscale-iops-for-azure-database-for-mysql---flexible-server---general-availabi/3884602)
- [Azure Database for MySQL pricing](https://azure.microsoft.com/en-us/pricing/details/mysql/)

</details>

<details markdown="1">
<summary><b>Table of Content</b> (Click to expand)</summary>

- [How to provision](#how-to-provision)
- [How to enable IOPS (manual approach)](#how-to-enable-iops-manual-approach)
- [How to enable IOPS (script)](#how-to-enable-iops-script)
- [How to Monitor IOPS Scaling](#how-to-monitor-iops-scaling)

</details>

When Autoscale IOPS is enabled for Azure Database for MySQL Flexible Server, IOPS automatically scale up and down based on workload demand:

- During `high demand`, the system `increases IOPS` to maintain performance.
- During `low demand`, it `scales down` to reduce resource usage and cost.

## How to provision 

1. Go to the [Azure Portal](https://portal.azure.com/)
2. Search for `Azure Database for MySQL Flexible Server` in the search bar.
3. Click `Create`.
4. Choose your subscription, resource group, and server name.
5. Select the region, MySQL version, and workload type (e.g., Development, Production).

<video controls width="700" aria-label="Provision an Azure Database for MySQL Flexible Server">
  <source src="https://github.com/user-attachments/assets/5b500aea-538d-4ddb-88b6-e0717a2d0fbe" type="video/mp4">
  Your browser does not support the video tag.
</video>

## How to enable IOPS (manual approach)

1. Go to the [Azure Portal](https://portal.azure.com/)
2. Select the server you want to configure.
3. In the left-hand menu, go to `Settings > Compute + Storage.`
4. In the IOPS section, select the option `Autoscale IOPS`
5. Click `Save` to apply the changes.

<video controls width="700" aria-label="Configure Autoscale IOPS manually">
  <source src="https://github.com/user-attachments/assets/9e2983b3-3839-4ad3-8ab8-ccbb698f3228" type="video/mp4">
  Your browser does not support the video tag.
</video>

## How to enable IOPS (script)

[Automate Autoscale IOPS using Python and the Azure REST API](automation.md) across resource groups or an entire subscription. Autoscale IOPS is supported only on the General Purpose and Business Critical tiers and cannot currently be enabled through Azure CLI or PowerShell.

## How to Monitor IOPS Scaling

Use the metrics available in Azure Monitor to determine when IOPS scale up or down.

### 1. Use Azure Monitor Metrics

- Go to your server in the [Azure portal](https://portal.azure.com/).
- Open `Monitoring`, then select `Metrics`.

<img width="550" alt="Azure Monitor Metrics navigation" src="https://github.com/user-attachments/assets/f08afb04-e271-4ac3-8594-e3e98a9bfd2e">

- Choose the `Storage IO` metric in both percentage and count formats.

  <img width="550" alt="Storage IO metric selection" src="https://github.com/user-attachments/assets/ca585f55-e943-413d-9477-f26c099a1e66">

- Set a `custom time range` to observe trends over time.

  | Storage IO Count | Storage IO Percent |
  | --- | --- |
  | <img width="550" alt="Storage IO count metric" src="https://github.com/user-attachments/assets/9be08df9-3fe6-4010-9e75-487a325d0acb"> | <img width="550" alt="Storage IO percentage metric" src="https://github.com/user-attachments/assets/c5f7f45d-303d-48ce-82a4-00685da29849"> |

### 2. Look for Scaling Patterns

- Sudden increases or decreases that correlate with workload changes indicate that Autoscale IOPS adjusted the performance level.
- Monitor `IO utilization percentage` to see how close the server is to its current IOPS limit.

### 3. Enable Alerts (Optional)

Configure Azure Monitor alerts to notify you when IOPS usage crosses selected thresholds.

<video controls width="700" aria-label="Configure Autoscale IOPS monitoring and alerts">
  <source src="https://github.com/user-attachments/assets/19b96128-e37f-40b4-8e23-8a5384bc6686" type="video/mp4">
  Your browser does not support the video tag.
</video>
