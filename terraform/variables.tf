variable "project" {
  type    = string
  default = "octue-django-twined-example"
}

variable "project_number" {
  type = string
  default = "413423446251"
}

variable "credentials_file" {
  type    = string
  default = "gcp-credentials.json"
}

variable "region" {
  type    = string
  default = "europe-west1"
}

variable "zone" {
  type    = string
  default = "europe-west1-d"
}

variable "environment" {
  type    = string
  default = "main"
}

variable "environments" {
  description = "A list of environments (eg main, staging + each developer's local environment)"
  type        = list(string)
  default     = ["main", "thclark"]
}
