# Django-Twined-Example Terraform Configuration

The purpose of this configuration is to maintain a set of resources that can be used for
development and integration testing of django-twined-example with live resources on Google Cloud.

It's already proven invaluable for testing and development of the tasks module.

We're currently learning terraform and expanding our DevOps expertise, so expect our workflows
to change dramatically in this area.

In the meantime, used with a different project ID, performing a `terraform apply`
on a fresh GCP project with this configuration should
give you the resources required to run the example test server. To do that, you'll need to:

- create a `terraform` service account in the new project with `Owner` and `Editor` roles
- supply the project ID as a variable

It's a work in progress so any contributions in this area are very welcome.
