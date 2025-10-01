variable "project_id" {
  type    = string
  default = "eng-archery-473819-h2"
}

variable "region" {
  type    = string
  default = "southamerica-west1"
}

variable "location" {
  type    = string
  default = "southamerica-west1"
}

variable "dataset_id" {
  type    = string
  default = "demo_bq"
}

variable "path_credentials" {
  type    = string
  default = "../keygcp.json"
}

variable "bucket_datain" {
  type    = string
  default = "eng-archery-473819-h2-data-in"
}
