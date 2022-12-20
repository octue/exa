# Deploying Exa

1. Make sure you have the terraform tool installed, and set up the GCloud CLI in your terminal.

1. Create a new GCLOUD project. Call it something sexier than `my-exa-project` which we'll use here for example. Make a note of the project number (it's on the project dashboard), we'll use `1234567890123` for the example.

1. You'll need a resource affix, which **must be globally unique** (it's used for provisioning globally unique named resources like storage buckets). We'll just reuse the project name... if you've chosen a sufficiently awesome name then it'll surely be globally unique ;)

1. [Create a service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts) in your project, call it `terraform` and give it the basic roles:

- Editor
- Owner
  (these are overprivileged but you can trim that back later, our aim is to get working here)

1. [Create a service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) and download it to `terraform/gcp-credentials.json` (don't worry, it won't be committed to the project repo).

1. Create your infrastructure using terraform

- Run the `init` and get a list of services whose APIs need to be enabled:

```
cd terraform
terraform init
terraform apply terraform apply -var "project=my-exa-project" -var "project_number=1234567890123" -var "resource_affix=my-exa-project"
```

- You'll get a lot of errors because APIs are not enabled yet (gcloud disables all its APIs by default). Find the errors that look like the following and click on the links to enable APIs that are needed:

```
Error: Error when reading or editing IAMBetaWorkloadIdentityPoolProvider "projects/1234567890123/locations/global/workloadIdentityPools/github-actions-pool/providers/github-actions-provider": googleapi: Error 403: Identity and Access Management (IAM) API has not been used in project 1234567890123 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/iam.googleapis.com/overview?project=1234567890123 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.
```

- Retry. You'll need to repeat this a few times until all of the APIs that you need are enabled on your project. Each time, a few more resources get created.
- **Some resources, like the managed PostgreSQL database, will take a long time to create (12 minutes and counting whilst writing these docs!)**

## :warning: CLEAN UP WHEN DONE!

The project you've just created will consume resources - although the server and services lie dormant, the database has a fixed running cost so don't forget to remove the project when you're done. You can do this by deleting the entire project in the google console, or by doing:

```
terraform destroy
```
