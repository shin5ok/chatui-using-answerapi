
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.64.0"
    }
  }
}

provider "google" {
  project = var.project 
  region  = "asia-northeast1"
}

# Variables
variable "project" {
  description = "Name of the Cloud Run service"
  type        = string
}

# Variables
variable "cloud_run_service_name" {
  description = "Name of the Cloud Run service"
  type        = string
  default = ""
}

variable "domain_name" {
  description = "FQDN for the managed certificate"
  type        = string
}

locals {
  enable_services = toset([
    "cloudresourcemanager.googleapis.com",
    "compute.googleapis.com",
    "run.googleapis.com",
    "certificatemanager.googleapis.com",
    "iap.googleapis.com",
  ])
}

resource "google_project_service" "compute_service" {
  service = "compute.googleapis.com"
}

resource "google_project_service" "service" {
  for_each = local.enable_services
  project  = var.project
  service  = each.value
  timeouts {
    create = "60m"
    update = "120m"
  }
  depends_on = [
    google_project_service.compute_service
  ]
}

# Cloud Run Serverless NEG
resource "google_compute_region_network_endpoint_group" "serverless_neg" {
  name                  = "serverless-neg"
  network_endpoint_type = "SERVERLESS"
  region                = "asia-northeast1"
  cloud_run {
    service = var.cloud_run_service_name
  }
}

# マネージド証明書
resource "google_compute_managed_ssl_certificate" "default" {
  name = "managed-cert"

  managed {
    domains = [var.domain_name]
  }
}

# グローバル外部ロードバランサ
resource "google_compute_global_forwarding_rule" "default" {
  name       = "global-rule"
  target     = google_compute_target_https_proxy.default.id
  port_range = "443"

  ip_address = google_compute_global_address.reserved_ip.address

  depends_on = [
    google_project_service.compute_service
  ]
}

resource "google_compute_target_https_proxy" "default" {
  name             = "https-proxy"
  url_map          = google_compute_url_map.default.id
  ssl_certificates = [google_compute_managed_ssl_certificate.default.id]
}

resource "google_compute_url_map" "default" {
  name            = "url-map"
  default_service = google_compute_backend_service.default.id
}

resource "google_compute_global_address" "reserved_ip" {
  name = "reserverd-ip"
  depends_on = [
    google_project_service.compute_service
  ]
}

resource "google_compute_backend_service" "default" {
  name        = "backend-service"
  protocol    = "HTTP"
  port_name   = "http"
  timeout_sec = 30

  backend {
    group = google_compute_region_network_endpoint_group.serverless_neg.id
  }

  # CDNを無効化
  enable_cdn = false

}

output "url_for_service" {
  value = "https://${var.domain_name}"
}

output "external_ip_attached_to_gclb" {
  value = google_compute_global_address.reserved_ip.address
}
