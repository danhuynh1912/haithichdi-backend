variable "project_name" {
  description = "Logical project name used for resource naming."
  type        = string
}

variable "environment_name" {
  description = "Environment name such as prod or staging."
  type        = string
}

variable "aws_region" {
  description = "AWS region for the endpoint service name."
  type        = string
}

variable "vpc_id" {
  description = "VPC ID where the endpoint lives."
  type        = string
}

variable "route_table_ids" {
  description = "Route tables associated with the gateway endpoint."
  type        = list(string)
}

variable "policy" {
  description = "Optional endpoint policy JSON."
  type        = string
  default     = null
  nullable    = true
}

variable "name" {
  description = "Name tag for the endpoint."
  type        = string
}

variable "tags" {
  description = "Additional tags applied to the endpoint."
  type        = map(string)
  default     = {}
}
