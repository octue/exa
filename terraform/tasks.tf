
# Primary task queue for django-twined-example server
resource "google_cloud_tasks_queue" "task_queue" {
  name     = "${var.environment}-primary"
  location = var.region
}

# Allow django-gcp.tasks to create on-demand tasks in the queue
#  See: https://cloud.google.com/iam/docs/understanding-roles
resource "google_project_iam_binding" "tasks_admin" {
  project = var.project
  role    = "roles/cloudtasks.admin"
  members = [
   "serviceAccount:${google_service_account.operating_service_account.email}",
  ]
}

# Allow django-gcp.tasks to create periodic tasks in google cloud scheduler
resource "google_project_iam_binding" "cloudscheduler_admin" {
  project = var.project
  role    = "roles/cloudscheduler.admin"
  members = [
    "serviceAccount:${google_service_account.operating_service_account.email}",
  ]
}
