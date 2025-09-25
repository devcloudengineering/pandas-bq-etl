terraform {
  backend "gcs" {
    bucket = "mi-primer-proyecto-469023-tfstate"
    prefix = "prd/bq/state"
  }
}
