provider "google" {
  project     = var.project_id
  region      = var.region
  credentials = file(var.path_credentials)
}


resource "google_storage_bucket" "my_bucket" {
  name          = var.bucket_datain
  location      = var.region
  force_destroy = true

  lifecycle_rule {
    action {
      type = "Delete"
    }

    condition {
      age = 30
    }
  }
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id                 = var.dataset_id
  location                   = var.location
  delete_contents_on_destroy = false
}

resource "google_bigquery_table" "ventas" {
  dataset_id          = google_bigquery_dataset.dataset.dataset_id
  table_id            = "ventas"
  schema              = file("${path.module}/schema/ventas.schema.json")
  deletion_protection = false
}

resource "google_bigquery_table" "clientes" {
  dataset_id          = google_bigquery_dataset.dataset.dataset_id
  table_id            = "clientes"
  schema              = file("${path.module}/schema/clientes.schema.json")
  deletion_protection = false
}

resource "google_bigquery_table" "productos" {
  dataset_id          = google_bigquery_dataset.dataset.dataset_id
  table_id            = "productos"
  schema              = file("${path.module}/schema/productos.schema.json")
  deletion_protection = false
}
