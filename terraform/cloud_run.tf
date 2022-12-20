
# TODO Figure out how this works.
#   - If the initial deployment fails, the creation gets part completed and reapplying gives an 'already exists' error
#   - Circular dependency because you can't route to the container until the container is built
#       - This can be worked around with a placeholder container but then reapplying terraform state kills the service
#   - Revisions aren't manageable because they're created by the CI system on github so get overwritten each time
#       - Which is possibly related to this not being implmented for v2: https://github.com/hashicorp/terraform-provider-google/issues/5898
#
# In the meantime, manually create a service with the following attributes:

# resource "google_cloud_run_v2_service" "server" {
#   name     = "${var.resource_affix}-${var.environment}-server"
#   location = "europe-west1"
#   ingress = "INGRESS_TRAFFIC_ALL"

#   template {

#     service_account = google_service_account.operating_service_account.email

#     scaling {
#       max_instance_count = 2
#     }

#     volumes {
#       name = "secrets"
#       secret {
#         secret = "${var.resource_affix}-${var.environment}-google-application-credentials"
#         items {
#           path = "google-application-credentials"
#           mode = 0400
#           version = "latest"
#         }
#       }
#     }

#     volumes {
#       name = "cloudsql"
#       cloud_sql_instance {
#         instances = [google_sql_database_instance.postgres_instance.connection_name]
#       }
#     }

#     # Container will ultimately be in the following pattern:
#     #    image = "${var.region}.pkg.dev/${var.project}/${var.resource_affix}/server:${var.environment}-latest"
#     # But now, we set up a placeholder container because that won't exist yet
#     #    (it's created by GitHub actions into the artefact repository so won't be initially available)
#     containers {
#       image = "gcr.io/cloudrun/placeholder"

#       env {
#         name = "DATABASE_URL"
#         value_source {
#           secret_key_ref {
#             secret = "${var.resource_affix}-${var.environment}-db-uri"
#             version = "latest"
#           }
#         }
#       }

#       env {
#         name = "DJANGO_SECRET_KEY"
#         value_source {
#           secret_key_ref {
#             secret = "${var.resource_affix}-${var.environment}-django-secret-key"
#             version = "latest"
#           }
#         }
#       }

#       env {
#         name = "GCP_REGION"
#         value = var.region
#       }

#       env {
#         name = "GCP_TASKS_RESOURCE_AFFIX"
#         value = "${var.resource_affix}-${var.environment}"
#       }

#       env {
#         name = "GCP_TASKS_DEFAULT_QUEUE_NAME"
#         value = google_cloud_tasks_queue.task_queue.name
#       }
#       env {
#         name = "GOOGLE_APPLICATION_CREDENTIALS"
#         value = "/secrets/google-application-credentials"
#       }

#       volume_mounts {
#         name = "cloudsql"
#         mount_path = "/cloudsql"
#       }

#       volume_mounts {
#         name = "secrets"
#         mount_path = "/secrets"
#       }

#     }
#   }

#   depends_on = [google_secret_manager_secret_version.secret_versions]
# }


# data "google_iam_policy" "noauth" {
#   binding {
#     role = "roles/run.invoker"
#     members = [
#       "allUsers",
#     ]
#   }
# }


# resource "google_cloud_run_service_iam_policy" "noauth" {
#   location    = google_cloud_run_v2_service.server.location
#   project     = google_cloud_run_v2_service.server.project
#   service     = google_cloud_run_v2_service.server.name
#   policy_data = data.google_iam_policy.noauth.policy_data
# }
