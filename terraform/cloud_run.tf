

# data "google_iam_policy" "noauth" {
#   binding {
#     role = "roles/run.invoker"
#     members = [
#       "allUsers",
#     ]
#   }
# }


# resource "google_cloud_run_service_iam_policy" "noauth" {
#   location    = google_cloud_run_service.server.location
#   project     = google_cloud_run_service.server.project
#   service     = google_cloud_run_service.server.name
#   policy_data = data.google_iam_policy.noauth.policy_data
# }




resource "google_cloud_run_v2_service" "server" {
  name     = "${var.resource_affix}-${var.environment}-server"
  location = "europe-west1"
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.operating_service_account.email

    scaling {
      max_instance_count = 2
    }

    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        instances = [google_sql_database_instance.postgres_instance.connection_name]
      }
    }

    volumes {
      name = "secrets"
      secret {
        secret = "${var.resource_affix}-${var.environment}-google-application-credentials"
        items {
          path = "google-application-credentials"
          mode = 0400
          version = "latest"
        }
      }
    }

    containers {
      image = "${var.region}.pkg.dev/${var.project}/${var.resource_affix}/server:${var.environment}-latest"

      env {
        name = "GCP_REGION"
        value = var.region
      }

      env {
        name = "GCP_RESOURCE_AFFIX"
        value = var.resource_affix
      }

      env {
        name = "GOOGLE_APPLICATION_CREDENTIALS"
        value = "/secrets/google-application-credentials"
      }

      env {
        name = "DATABASE_URL"
        value_source {
          secret_key_ref {
            secret = "${var.resource_affix}-${var.environment}-db-uri"
            version = "1"
          }
        }
      }

      env {
        name = "DJANGO_SECRET_KEY"
        value_source {
          secret_key_ref {
            secret = "${var.resource_affix}-${var.environment}-django-secret-key"
            version = "1"
          }
        }
      }

      volume_mounts {
        name = "secrets"
        mount_path = "/secrets"
      }

      volume_mounts {
        name = "cloudsql"
        mount_path = "/cloudsql"
      }
    }
  }

  traffic {
    type = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
  depends_on = [google_secret_manager_secret_version.secret_versions]
}
