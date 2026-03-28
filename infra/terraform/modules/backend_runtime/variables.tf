variable "project_name" {
  description = "Logical project name used for resource naming."
  type        = string
}

variable "environment_name" {
  description = "Environment name such as prod or staging."
  type        = string
}

variable "function_name" {
  description = "Existing Lambda function name."
  type        = string
}

variable "function_description" {
  description = "Lambda function description."
  type        = string
  default     = ""
}

variable "image_uri" {
  description = "Current ECR image URI for the Lambda function. Code rollout stays external to Terraform for now."
  type        = string
}

variable "role_arn" {
  description = "Execution role ARN used by the Lambda function."
  type        = string
}

variable "role_name" {
  description = "Execution role name used by the Lambda function."
  type        = string
}

variable "architectures" {
  description = "Lambda architectures."
  type        = list(string)
  default     = ["x86_64"]
}

variable "memory_size" {
  description = "Lambda memory size in MB."
  type        = number
}

variable "timeout" {
  description = "Lambda timeout in seconds."
  type        = number
}

variable "ephemeral_storage_size" {
  description = "Lambda ephemeral storage size in MB."
  type        = number
  default     = 512
}

variable "subnet_ids" {
  description = "Subnet IDs for Lambda VPC configuration."
  type        = list(string)
}

variable "security_group_ids" {
  description = "Security group IDs for Lambda VPC configuration."
  type        = list(string)
}

variable "lambda_environment_variables" {
  description = "Environment variables for the Lambda function."
  type        = map(string)
}

variable "media_writer_policy_arn" {
  description = "Managed policy ARN that grants write access to the media bucket."
  type        = string
}

variable "ssm_parameter_arns" {
  description = "SSM parameter ARNs the Lambda runtime may read with decryption."
  type        = list(string)
  default     = []
}

variable "tracing_mode" {
  description = "Lambda tracing mode."
  type        = string
  default     = "PassThrough"
}

variable "tags" {
  description = "Additional tags applied to managed resources."
  type        = map(string)
  default     = {}
}
