variable "project_name" {
  description = "Logical project name used for resource naming."
  type        = string
}

variable "environment_name" {
  description = "Environment name such as prod or staging."
  type        = string
}

variable "bucket_name" {
  description = "Globally unique S3 bucket name for media assets."
  type        = string
}

variable "force_destroy" {
  description = "Whether Terraform can destroy the bucket even when it still contains objects."
  type        = bool
  default     = false
}

variable "writer_role_names" {
  description = "Existing IAM role names that should receive the media writer policy."
  type        = list(string)
  default     = []
}

variable "cloudfront_aliases" {
  description = "Optional custom domain aliases for the CloudFront distribution."
  type        = list(string)
  default     = []
}

variable "acm_certificate_arn" {
  description = "Optional ACM certificate ARN for custom CloudFront aliases. Must be issued in us-east-1."
  type        = string
  default     = null
  nullable    = true

  validation {
    condition     = length(var.cloudfront_aliases) == 0 || var.acm_certificate_arn != null
    error_message = "acm_certificate_arn is required when cloudfront_aliases is not empty."
  }
}

variable "minimum_protocol_version" {
  description = "Minimum TLS protocol version when using a custom ACM certificate."
  type        = string
  default     = "TLSv1.2_2021"
}

variable "cloudfront_price_class" {
  description = "CloudFront price class for media delivery."
  type        = string
  default     = "PriceClass_100"

  validation {
    condition = contains(
      ["PriceClass_All", "PriceClass_200", "PriceClass_100"],
      var.cloudfront_price_class,
    )
    error_message = "cloudfront_price_class must be one of PriceClass_100, PriceClass_200, or PriceClass_All."
  }
}

variable "abort_incomplete_multipart_upload_days" {
  description = "Number of days before incomplete multipart uploads are aborted."
  type        = number
  default     = 7
}

variable "noncurrent_version_expiration_days" {
  description = "Number of days before noncurrent object versions expire."
  type        = number
  default     = 30
}

variable "tags" {
  description = "Additional tags applied to all resources."
  type        = map(string)
  default     = {}
}
