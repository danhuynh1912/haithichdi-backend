variable "project_name" {
  description = "Logical project name used for resource naming."
  type        = string
}

variable "environment_name" {
  description = "Environment name such as prod or staging."
  type        = string
}

variable "aws_region" {
  description = "AWS region for VPC endpoints."
  type        = string
}

variable "vpc_cidr" {
  description = "Primary IPv4 CIDR block for the custom VPC."
  type        = string
}

variable "secondary_vpc_cidr_blocks" {
  description = "Optional secondary IPv4 CIDR blocks associated with the VPC."
  type        = list(string)
  default     = []
}

variable "private_app_subnets" {
  description = "Private application subnets for Lambda runtimes."
  type = list(object({
    availability_zone = string
    cidr_block        = string
  }))

  validation {
    condition     = length(var.private_app_subnets) >= 2
    error_message = "Provide at least two private app subnets across AZs."
  }
}

variable "private_db_subnets" {
  description = "Private database subnets for RDS."
  type = list(object({
    availability_zone = string
    cidr_block        = string
  }))

  validation {
    condition     = length(var.private_db_subnets) >= 2
    error_message = "Provide at least two private DB subnets across AZs."
  }
}

variable "db_subnet_group_name" {
  description = "Name for the DB subnet group created for the future RDS migration."
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

  validation {
    condition = (
      var.enable_ssm_interface_endpoint == false
      || (
        var.ssm_interface_endpoint_name != null
        && trimspace(var.ssm_interface_endpoint_name) != ""
      )
    )
    error_message = "Set ssm_interface_endpoint_name when enable_ssm_interface_endpoint is true."
  }
}

variable "enable_ssm_interface_endpoint" {
  description = "Whether to create the SSM interface endpoint and its security group."
  type        = bool
  default     = true
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
