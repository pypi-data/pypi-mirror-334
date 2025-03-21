# ServiceNow Integration with IP Fabric

## IP Fabric

IP Fabric is a vendor-neutral network assurance platform that automates the 
holistic discovery, verification, visualization, and documentation of 
large-scale enterprise networks, reducing the associated costs and required 
resources whilst improving security and efficiency.

It supports your engineering and operations teams, underpinning migration and 
transformation projects. IP Fabric will revolutionize how you approach network 
visibility and assurance, security assurance, automation, multi-cloud 
networking, and trouble resolution.

**Integrations or scripts should not be installed directly on the IP Fabric VM unless directly communicated from the
IP Fabric Support or Solution Architect teams.  Any action on the Command-Line Interface (CLI) using the root, osadmin,
or autoboss account may cause irreversible, detrimental changes to the product and can render the system unusable.**

## Overview

This project syncs devices from IP Fabric's Inventory to ServiceNow's CMDB Network Gear Table.

## CLI Utility Installation
```shell
pip install ipfabric-snow
```
## ServiceNow Configuration
Please see the [ServiceNow Configuration](docs/IP_Fabric_Service_Now_Application/index.md) section for details on how to configure ServiceNow for use with this integration.


## Environment Setup
Copy sample.env to .env and fill in the necessary details.
During the setup, you'll be prompted to enter the necessary environment variables including URLs and authentication details for both ServiceNow and IP Fabric.

## Quick Start 
To sync devices from IP Fabric to ServiceNow, run:

```shell
ipfabric-snow sync devices 
```
If the environment is not properly set up, you'll be prompted to set it up. Follow the prompts to provide the necessary details.

```shell
ipfabric-snow --help
```
```shell
 Usage: ipfabric-snow [OPTIONS] COMMAND [ARGS]...                                                                                                                                                 
                                                                                                                                                                                                  
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --log-level                                 TEXT  Log level [default: INFO]                                                                                                                    │
│ --log-to-file           --no-log-to-file          Log to file [default: log-to-file]                                                                                                           │
│ --log-file-name                             TEXT  Log file name [default: ipf_serviceNow.log]                                                                                                  │
│ --log-json              --no-log-json             Log in JSON format [default: no-log-json]                                                                                                    │
│ --install-completion                              Install completion for the current shell.                                                                                                    │
│ --show-completion                                 Show completion for the current shell, to copy it or customize the installation.                                                             │
│ --help                                            Show this message and exit.                                                                                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ env                     Setup environment variables                                                                                                                                            │
│ sync                    Sync Inventory data with ServiceNow                                                                                                                                    │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
```shell
❯ ipfabric-snow sync --help
                                                                                                                                                                                                                                                             
 Usage: ipfabric-snow sync [OPTIONS] COMMAND [ARGS]...                                                                                                                                                                                                       
                                                                                                                                                                                                                                                             
 Sync Inventory data with ServiceNow                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                             
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                                                                                               │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ devices                                  Sync devices from IP Fabric to ServiceNow                                                                                                                                                                        │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
```shell
 ipfabric-snow sync devices --help
```
```shell                                                                                                                                                                  
Usage: ipfabric-snow sync devices [OPTIONS] [STAGING_TABLE_NAME]                                                                                                                                 
                                                                                                                                                                                                  
 Sync devices from IP Fabric to ServiceNow                                                                                                                                                       
                                                                                                                                                                                                  
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   staging_table_name      [STAGING_TABLE_NAME]  The name of the ServiceNow staging table to use. [default: x_1249630_ipf_devices]                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --show-diff         --no-show-diff                  Display the data difference [default: no-show-diff]                            │
│ --diff-source                              TEXT     Specify the main source for diff, either IPF or SNOW [default: IPF]            │
│ --write-diff        --no-write-diff                 Enable or disable writing the diff to a file [default: no-write-diff]          │
│ --diff-file                                TEXT     Path to save the diff file, if desired                                         │
│                                                     [default: data/{date_time}_diff_{diff_source}.json]                            │
│ --dry-run           --no-dry-run                    Perform a dry run without making any changes [default: no-dry-run]             │
│ --ipf-snapshot                             TEXT     IP Fabric snapshot ID to use for the sync [default: $last]                     │
│ --timeout                                  INTEGER  timeout for httpx requests [default: 10]                                       │
│ --record-limit                             INTEGER  Limit the number of records to pull from ServiceNow. Defaults to 1000          │
│                                                     [default: 1000]                                                                │
│ --output-verbose    --no-output-verbose             adds more detail to the output. Identifies which keys changed per device       │
│                                                     [default: no-output-verbose]                                                   │
│ --help                                              Show this message and exit.                                                    │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

example of sync devices command:
```shell
ipfabric-snow --log-level DEBUG sync devices --show-diff --diff-source SNOW  --ipf-snapshot "12dd8c61-129c-431a-b98b-4c9211571f89" --output-verbose --timeout 30 --record-limit 1000
```

### Development

#### Poetry
Clone the repository and run
```shell
poetry install
```
#### Invoke
This project uses [Invoke](https://www.pyinvoke.org/) for task automation. To see a list of available tasks, run:
```shell
invoke --list
```
#### Clearing the Netgear Table
During Development, you may want to clear the netgear table in ServiceNow.
To clear the netgear table, run:
```shell
❯ invoke clear-netgear-table
```
Any Changes to ServiceNow Application should be merged into the main_snow_app branch
