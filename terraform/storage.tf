

# Add a static bucket (public contents)
resource "google_storage_bucket" "static_assets" {
  name                        = "${var.resource_affix}-${var.environment}-static-assets"
  location                    = "EU"
  force_destroy               = true
  uniform_bucket_level_access = true
}

# Make static bucket contents public
resource "google_storage_bucket_iam_binding" "static_assets_object_viewer" {
  bucket = google_storage_bucket.static_assets.name
  role   = "roles/storage.objectViewer"
  members = [
    "allUsers"
  ]
}

# Add a media bucket (private contents)
#   Note: CORS are set to allow direct uploads, enabling upload of files
#         larger than 32 mb (Cloud Run has a hard limit on file upload size)
resource "google_storage_bucket" "media_assets" {
  name                        = "${var.resource_affix}-${var.environment}-media-assets"
  location                    = "EU"
  force_destroy               = true
  uniform_bucket_level_access = false
  cors {
    origin          = ["*"]
    method          = ["GET", "HEAD", "PUT"]
    response_header = ["*"]
    max_age_seconds = 3600
  }
}


# Allow operating service account to generate signed upload urls
resource "google_storage_bucket_iam_binding" "media_assets_object_admin" {
  bucket = google_storage_bucket.media_assets.name
  role   = "roles/storage.objectAdmin"
  members = [
    "serviceAccount:${google_service_account.operating_service_account.email}"
  ]
}
