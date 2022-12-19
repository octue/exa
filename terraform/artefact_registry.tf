resource "google_artifact_registry_repository" "artefact_registry_repository" {
  location      = var.region
  repository_id = var.resource_affix
  description   = "Docker image repository"
  format        = "DOCKER"
}
