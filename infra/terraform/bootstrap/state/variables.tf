variable "aws_region" {
  description = "AWS region that hosts the Terraform state bucket."
  type        = string
}

variable "project_name" {
  description = "Logical project name used for resource naming."
  type        = string
}

variable "environment_name" {
  description = "Environment name such as prod or staging."
  type        = string
  default     = "prod"
}

variable "state_bucket_name" {
  description = "Globally unique S3 bucket name used for Terraform remote state."
  type        = string
}

variable "force_destroy" {
  description = "Whether Terraform may destroy the bucket even if it still contains state objects."
  type        = bool
  default     = false
}

variable "noncurrent_version_expiration_days" {
  description = "Days to retain noncurrent object versions in the state bucket."
  type        = number
  default     = 90
}

variable "tags" {
  description = "Additional tags applied to all resources."
  type        = map(string)
  default     = {}
}
