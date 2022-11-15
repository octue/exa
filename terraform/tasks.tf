
# Primary task queue for django-twined-example server
resource "google_cloud_tasks_queue" "task_queue" {
  name     = "${var.environment}-primary"
  location = var.region
}


# Allow django-gcp.tasks to create periodic tasks in google cloud scheduler
# resource "google_project_iam_binding" "cloudscheduler_jobs_update" {
#   project = var.project
#   role    = "roles/CloudSchedulerAdmin"
#   members = [
#     "serviceAccount:${google_service_account.operating_service_account.email}",
#   ]
# }
