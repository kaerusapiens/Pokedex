# Define the variables used in the Terraform configuration
variable "default_name" {
  type        = string
}

variable "project_id" {
  type        = string
}

variable "region" {
  type        = string
  default     = "asia-northeast1"
}
