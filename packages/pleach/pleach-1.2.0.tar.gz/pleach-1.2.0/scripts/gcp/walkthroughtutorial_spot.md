# Deploy Pleach on Google Cloud Platform

**Duration**: 45 minutes  
**Author**: [Robert Wilkins III](https://www.linkedin.com/in/robertwilkinsiii)

## Introduction

In this tutorial, you will learn how to deploy Pleach on [Google Cloud Platform](https://cloud.google.com/) (GCP) using Google Cloud Shell.

This tutorial assumes you have a GCP account and basic knowledge of Google Cloud Shell. If you're not familiar with Cloud Shell, you can review the [Cloud Shell documentation](https://cloud.google.com/shell/docs).

## Set up your environment

Before you start, make sure you have the following prerequisites:

- A GCP account with the necessary permissions to create resources
- A project on GCP where you want to deploy Pleach

[**Select your GCP project**]<walkthrough-project-setup
  billing="true"
  apis="compute.googleapis.com,container.googleapis.com">
</walkthrough-project-setup>


In the next step, you'll configure the GCP environment and deploy Pleach.

## Configure the GCP environment and deploy Pleach
Run the deploy_pleach_gcp_spot.sh script to configure the GCP environment and deploy Pleach:

```sh  
gcloud config set project <walkthrough-project-id/>  
bash ./deploy_pleach_gcp_spot.sh
```

The script will:

1. Check if the required resources (VPC, subnet, firewall rules, and Cloud Router) exist and create them if needed
2. Create a startup script to install Python, Pleach, and Nginx
3. Create a Compute Engine VM instance with the specified configuration and startup script
4. Run Pleach to serve content on TCP port 7860

> <walkthrough-pin-section-icon></walkthrough-pin-section-icon> The process may take approximately 30 minutes to complete. Rest assured that progress is being made, and you'll be able to proceed once the process is finished.

In the next step, you'll learn how to connect to the Pleach VM.

## Connect to the Pleach VM
To connect to your new Pleach VM, follow these steps:

1. Navigate to the [VM instances](https://console.cloud.google.com/compute/instances) page and click on the external IP for your VM.  Make sure to use HTTP and set the port to 7860
<br>**or**
3. Run the following command to display the URL for your Pleach environment:
```bash
export PLEACH_IP=$(gcloud compute instances list --filter="NAME=pleach-dev" --format="value(EXTERNAL_IP)")

echo http://$PLEACH_IP:7860
```

4. Click on the Pleach URL in cloudshell to be greeted by the Pleach Dev environment

Congratulations! You have successfully deployed Pleach on Google Cloud Platform.

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

## Cleanup
If you want to remove the resources created during this tutorial, you can use the following commands:

```sql
gcloud compute instances delete pleach-dev --zone us-central1-a --quiet
```
The following network settings and services are used during this walkthrough. If you plan to continue using the project after the walkthrough, you may keep these configurations in place.

However, if you decide to remove them after completing the walkthrough, you can use the following gcloud commands:
> <walkthrough-pin-section-icon></walkthrough-pin-section-icon> These commands will delete the firewall rules and network configurations created during the walkthrough. Make sure to run them only if you no longer need these settings.

```
gcloud compute firewall-rules delete allow-tcp-7860 --quiet

gcloud compute firewall-rules delete allow-iap --quiet

gcloud compute networks subnets delete default --region us-central1 --quiet

gcloud compute networks delete default --quiet
```
