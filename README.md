#   ChatUI using Answer API of Vertex AI Search a.k.a. Vertex AI Agent Builder

## Prerequisite
- Python 3.10+
- Google Cloud project, billing enabled
- Google Cloud SDK(gcloud command)
- Some PDFs for search sources
- [Option]: Original FQDN for this service if using https

## Preparation
on your local environment
Run as below, to get authorization.
```
gcloud auth application-default login
gcloud auth login
```

## Setup

### 1. Setup your Datastore for Agent Builder

You can build a Datastore very simply.
follow the link.  
[https://cloud.google.com/generative-ai-app-builder/docs/try-enterprise-search](https://cloud.google.com/generative-ai-app-builder/docs/try-enterprise-search)

> [!NOTE]
> Recommend to use Cloud Storage as data source because I have not confirmed other data sources.


### 2. Get the datastore ID

Write down the Datastore ID.
![](./images/id_of_datastore.png)
The ID is "kaijuu-storage_1723815035090" in this case.

### 3. Create service accounts for Cloud Run service.

Make sure where you are in top directory, and then just type this.
```bash
make iam
```

### 4. Deploy Cloud Run Service

Prepare environment values.
Database ID is one you wrote down before.
```bash
export PROJECT_ID=<your Project ID>
export DATASTORE_ID=<your Datastore ID>
```

Deploy the Cloud Run service.
```bash
make deploy
```
Wait for few minutes until finishing the deployment.

>[!NOTE]
>You cannot access Cloud Run services yet, because the service requires Load Balancer + IAP for security reason.  
>Proceed the next step.

### 5. Configure Identity Aware Proxy(IAP) 
To prevent unauthorized access from the Internet, you can take advantage of IAP.

Follow the link.  
[https://cloud.google.com/iap/docs/enabling-cloud-run?hl=ja](https://cloud.google.com/iap/docs/enabling-cloud-run?hl=ja)

>[!NOTE]
> If you want https access, you need domain name that you have authorization of.  
> Take advantage of Managed certification or Certificate manager.
