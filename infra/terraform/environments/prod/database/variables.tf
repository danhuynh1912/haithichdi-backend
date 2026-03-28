variable "aws_region" {
  description = "AWS region for the database stack."
  type        = string
}

variable "state_bucket_name" {
  description = "S3 bucket that stores Terraform remote state."
  type        = string
}

variable "network_state_key" {
  description = "Remote state key for the active network stack."
  type        = string
  default     = "network/prod/terraform.tfstate"
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

variable "db_instance_identifier" {
  description = "Production DB instance identifier."
  type        = string
}

variable "instance_class" {
  description = "RDS instance class."
  type        = string
}

variable "engine" {
  description = "Database engine."
  type        = string
}

variable "engine_version" {
  description = "Database engine version."
  type        = string
}

variable "master_username" {
  description = "Master username."
  type        = string
}

variable "allocated_storage" {
  description = "Allocated storage in GiB."
  type        = number
}

variable "max_allocated_storage" {
  description = "Maximum autoscaled storage in GiB."
  type        = number
}

variable "storage_type" {
  description = "Storage type."
  type        = string
}

variable "iops" {
  description = "Provisioned IOPS."
  type        = number
}

variable "storage_throughput" {
  description = "Storage throughput in MiB/s."
  type        = number
}

variable "port" {
  description = "Database port."
  type        = number
  default     = 5432
}

variable "publicly_accessible" {
  description = "Whether the DB should remain publicly accessible after the move."
  type        = bool
  default     = false
}

variable "auto_minor_version_upgrade" {
  description = "Whether minor version upgrades are automatically applied."
  type        = bool
}

variable "backup_retention_period" {
  description = "Backup retention period in days."
  type        = number
}

variable "backup_window" {
  description = "Preferred backup window."
  type        = string
}

variable "maintenance_window" {
  description = "Preferred maintenance window."
  type        = string
}

variable "storage_encrypted" {
  description = "Whether the DB storage is encrypted."
  type        = bool
}

variable "kms_key_id" {
  description = "KMS key ARN for storage encryption."
  type        = string
}

variable "performance_insights_enabled" {
  description = "Whether Performance Insights is enabled."
  type        = bool
}

variable "performance_insights_kms_key_id" {
  description = "KMS key ARN for Performance Insights."
  type        = string
}

variable "performance_insights_retention_period" {
  description = "Performance Insights retention period in days."
  type        = number
}

variable "parameter_group_name" {
  description = "DB parameter group name."
  type        = string
}

variable "option_group_name" {
  description = "DB option group name."
  type        = string
}

variable "deletion_protection" {
  description = "Whether deletion protection is enabled."
  type        = bool
}

variable "copy_tags_to_snapshot" {
  description = "Whether tags are copied to snapshots."
  type        = bool
}

variable "ca_cert_identifier" {
  description = "CA certificate identifier."
  type        = string
}

variable "monitoring_interval" {
  description = "Enhanced Monitoring interval in seconds."
  type        = number
  default     = 0
}

variable "monitoring_role_arn" {
  description = "Monitoring role ARN when enhanced monitoring is enabled."
  type        = string
  default     = null
  nullable    = true
}

variable "network_type" {
  description = "Network type."
  type        = string
  default     = "IPV4"
}

variable "multi_az" {
  description = "Whether the DB instance is Multi-AZ."
  type        = bool
}

variable "apply_immediately" {
  description = "Whether the migration changes should be applied immediately."
  type        = bool
  default     = false
}

variable "skip_final_snapshot" {
  description = "Whether the instance should skip a final snapshot on destroy. Included to match the current imported state."
  type        = bool
  default     = true
}

variable "tags" {
  description = "Additional tags applied to the DB instance."
  type        = map(string)
  default     = {}
}
