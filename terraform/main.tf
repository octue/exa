terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.33.0"
    }
  }
  # To use terraform cloud, which is a good idea for integrating into CI because it'll avoid deadlocks, uncomment the following:
  # cloud {
  #   organization = "your-organisation"
  #   workspaces {
  #     name = "your-workspace-which-is-almost-certainly-your-project-name"
  #   }
  # }
}

provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project
  region      = var.region
  zone        = var.zone
}
