variable "aws_region" {
  description = "AWS region for the S3 bucket and IAM resources."
  type        = string
}

variable "project_name" {
  description = "Logical project name."
  type        = string
}

variable "environment_name" {
  description = "Environment name."
  type        = string
  default     = "prod"
}

variable "media_bucket_name" {
  description = "Globally unique S3 bucket name for media assets."
  type        = string
}

variable "writer_role_names" {
  description = "IAM role names that should be able to upload and delete media."
  type        = list(string)
  default     = []
}

variable "cloudfront_aliases" {
  description = "Optional custom domains for the media CDN."
  type        = list(string)
  default     = []
}

variable "acm_certificate_arn" {
  description = "Optional ACM certificate ARN in us-east-1 for custom CloudFront aliases."
  type        = string
  default     = null
  nullable    = true
}

variable "cloudfront_price_class" {
  description = "CloudFront price class."
  type        = string
  default     = "PriceClass_100"
}

variable "abort_incomplete_multipart_upload_days" {
  description = "Days before incomplete multipart uploads are aborted."
  type        = number
  default     = 7
}

variable "noncurrent_version_expiration_days" {
  description = "Days before noncurrent versions are expired."
  type        = number
  default     = 30
}

variable "force_destroy" {
  description = "Whether Terraform can destroy a non-empty media bucket."
  type        = bool
  default     = false
}

variable "tags" {
  description = "Additional tags applied to resources."
  type        = map(string)
  default     = {}
}
