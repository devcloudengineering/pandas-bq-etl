terraform {
  backend "gcs" {
    bucket = "eng-archery-473819-h2-tfstate"
    prefix = "prd/bq/state"
  }
}
