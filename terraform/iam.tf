
# You need to start with a service account called "terraform" which has both the 'editor' and 'owner' basic permissions.
# This allows it to assign permissions to resources per https://cloud.google.com/iam/docs/understanding-roles


resource "google_service_account" "operating_service_account" {
  account_id   = "${var.environment}-server"
  display_name = "${var.environment}-server"
  description  = "Operate the example server in the cloud or local environment"
  project      = var.project
}


resource "google_service_account" "github_actions_service_account" {
    account_id   = "github-actions-ci"
    description  = "Allow GitHub Actions to deploy code onto resources"
    display_name = "github-actions-ci"
    project      = var.project
}


resource "google_iam_workload_identity_pool" "github_actions_pool" {
    display_name              = "github-actions-pool"
    project                   = var.project
    workload_identity_pool_id = "github-actions-pool"
}


resource "google_iam_workload_identity_pool_provider" "github_actions_provider" {
    attribute_mapping                  = {
        "attribute.actor"            = "assertion.actor"
        "attribute.repository"       = "assertion.repository"
        "attribute.repository_owner" = "assertion.repository_owner"
        "google.subject"             = "assertion.sub"
    }
    display_name                       = "Github Actions Provider"
    project                            = var.project_number
    workload_identity_pool_id          = "github-actions-pool"
    workload_identity_pool_provider_id = "github-actions-provider"

    oidc {
        allowed_audiences = []
        issuer_uri        = "https://token.actions.githubusercontent.com"
    }
}
