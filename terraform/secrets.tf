

variable "secret_names" {
  description = "A list of secrets to be created and made accessible to the server"
  type        = list(string)
  default     = ["db-uri", "db-proxy-uri", "django-secret-key", "google-application-credentials"]
}

resource "google_secret_manager_secret" "secrets" {
  count = length(var.secret_names)
  secret_id = "${var.resource_affix}-${var.environment}-${var.secret_names[count.index]}"
  replication {
    automatic = true
  }
}

# TODO Figure out how to manage the contents of these. In the meantime, manually set them!
# resource "google_secret_manager_secret_version" "secret_versions" {
#   count = length(google_secret_manager_secret.secrets)
#   secret = google_secret_manager_secret.secrets[count.index].name
#   secret_data = "change this in production"
# }

# Fine grained resource access
# resource "google_secret_manager_secret_iam_binding" "secret_accessor" {
#   project = var.project
#   count = length(google_secret_manager_secret.secrets)
#   secret_id = google_secret_manager_secret.secrets[count.index].secret_id
#   role = "roles/secretmanager.secretAccessor"
#   members = [
#     "serviceAccount:${google_service_account.operating_service_account.email}"
#   ]
# }
