variable "project" {
  type    = string
  default = "octue-exa"
}

variable "project_number" {
  type = string
  default = "1073024407725"
}

variable "resource_affix" {
  type    = string
  default = "exa"
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
