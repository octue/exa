
# Primary task queue for django-twined-example server
resource "google_cloud_tasks_queue" "task_queue" {
  name     = "${var.resource_affix}-${var.environment}-primary"
  location = var.region
}
