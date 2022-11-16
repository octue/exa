resource "google_sql_database_instance" "postgres_instance" {
    name                          = "primary"
    project                       = var.project
    region                        = var.region
    database_version              = "POSTGRES_13"
    deletion_protection           = "true"
    settings {
        tier                      = "db-f1-micro"
    }
    # If we need to execute SQL...
    #   provisioner "local-exec" {
    #     command = "PGPASSWORD=<password> psql -f schema.sql -p <port> -U <username> <databasename>"
    #   }
}


resource "google_sql_database" "postgres_database" {
  name     = "${var.resource_affix}-${var.environment}-db"
  instance = google_sql_database_instance.postgres_instance.name
}
