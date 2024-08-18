#-------------------------------------
# Service Account
#-------------------------------------
resource "google_service_account" "service_account" {
  account_id   = "${var.default_name}-sa"
}



#-------------------------------------
# IAM policy binding
#-------------------------------------
#GCF
resource "google_project_iam_member" "function_invoker" {
  project = var.project_id
  role    = "roles/cloudfunctions.invoker"
  
  member  = "serviceAccount:${google_service_account.service_account.email}"
}

#Bigquery data creation
resource "google_project_iam_member" "bigquery_data_editor" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.service_account.email}"
}

#Bigquery Job user
resource "google_project_iam_member" "bigquery_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.service_account.email}"
}


#-------------------------------------
# GCS
#-------------------------------------
#create bucket
resource "google_storage_bucket" "bucket" {
  name     = "${var.default_name}-bucket"
  location = var.region
}

# Upload
resource "google_storage_bucket_object" "app_source" {
  name   = "${var.default_name}_app.zip"
  bucket = google_storage_bucket.bucket.name
  source = "../app/app.zip"

}


#-------------------------------------
# Cloud Function (Gen2)
#-------------------------------------
resource "google_cloudfunctions2_function" "function" {
  name        = "${var.default_name}-app"
  location    = var.region

  build_config {
    runtime     = "python310"
    entry_point = "main"  # Entry_point
    source {
      storage_source {
        bucket = google_storage_bucket.bucket.name
        object = google_storage_bucket_object.app_source.name
      }
    }
  }

  service_config {
    available_memory   = "256M"
    min_instance_count = 0
    max_instance_count = 1
    service_account_email = google_service_account.service_account.email
    timeout_seconds = 50 #Max time 540
  }

}

#-------------------------------------
# GCLB
#-------------------------------------
# URL Routing
resource "google_compute_url_map" "url_map" {
  name            = "${var.default_name}-url-map"
  default_service = google_compute_backend_service.backend.self_link
}

# Proxy
resource "google_compute_target_http_proxy" "proxy" {
  name   = "${var.default_name}-proxy"
  url_map = google_compute_url_map.url_map.self_link
}

# Forwarding Rule
resource "google_compute_global_forwarding_rule" "forwarding_rule" {
  name       = "${var.default_name}-forwarding-rule"
  target     = google_compute_target_http_proxy.proxy.self_link
  port_range = "80"
}


#-------------------------------------
# Cloud Armor policy
#-------------------------------------
resource "google_compute_security_policy" "armor_policy" {
  name = "${var.default_name}-security-policy"

  rule {
    action   = "allow"
    priority = "2147483647"
    match {
      versioned_expr = "SRC_IPS_V1"
      config {
        src_ip_ranges = ["*"]
      }
    }
    description = "default rule"
  }
}

#-------------------------------------
# GCLB + Serverless_neg + Cloud Armor
#-------------------------------------

resource "google_compute_region_network_endpoint_group" "serverless_neg" {
  name                  = "${var.default_name}-neg"
  region                = var.region
  network_endpoint_type = "SERVERLESS"

  cloud_function {
    function = google_cloudfunctions2_function.function.name
  }
}

resource "google_compute_backend_service" "backend" {
  name                  = "${var.default_name}-backend"
  load_balancing_scheme = "EXTERNAL"

  backend {
    group = google_compute_region_network_endpoint_group.serverless_neg.id
  }

  security_policy = google_compute_security_policy.armor_policy.self_link  # Cloud Armor
}
