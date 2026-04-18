variable "aws_region" {
  description = "AWS region for the custom VPC."
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

variable "vpc_cidr" {
  description = "Primary IPv4 CIDR block for the custom VPC."
  type        = string
}

variable "secondary_vpc_cidr_blocks" {
  description = "Optional secondary IPv4 CIDR blocks associated with the custom VPC."
  type        = list(string)
  default     = []
}

variable "private_app_subnets" {
  description = "Private application subnets for Lambda runtimes."
  type = list(object({
    availability_zone = string
    cidr_block        = string
  }))
}

variable "private_db_subnets" {
  description = "Private database subnets for RDS."
  type = list(object({
    availability_zone = string
    cidr_block        = string
  }))
}

variable "db_subnet_group_name" {
  description = "Name for the DB subnet group used by the future RDS migration."
  type        = string
}

variable "s3_gateway_endpoint_name" {
  description = "Name tag for the S3 gateway endpoint."
  type        = string
}

variable "ssm_interface_endpoint_name" {
  description = "Name tag for the SSM interface endpoint."
  type        = string
  default     = null
  nullable    = true
}

variable "enable_ssm_interface_endpoint" {
  description = "Whether to create the SSM interface endpoint in the app subnets."
  type        = bool
  default     = true
}

variable "confirm_backend_runtime_direct_secrets_cutover" {
  description = "Safety flag required when disabling the SSM interface endpoint."
  type        = bool
  default     = false
}

variable "s3_gateway_endpoint_policy" {
  description = "Optional endpoint policy JSON for the S3 gateway endpoint."
  type        = string
  default     = null
  nullable    = true
}

variable "tags" {
  description = "Additional tags applied to managed resources."
  type        = map(string)
  default     = {}
}
