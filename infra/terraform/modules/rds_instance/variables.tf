variable "db_instance_identifier" {
  description = "RDS DB instance identifier."
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
  description = "Master username of the DB instance."
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
  description = "Storage type, for example gp3."
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

variable "db_subnet_group_name" {
  description = "DB subnet group name."
  type        = string
}

variable "vpc_security_group_ids" {
  description = "Security groups attached to the DB instance."
  type        = list(string)
}

variable "publicly_accessible" {
  description = "Whether the DB instance is publicly accessible."
  type        = bool
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
  description = "Whether storage is encrypted."
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
  description = "Option group name."
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
  description = "Network type, for example IPV4."
  type        = string
  default     = "IPV4"
}

variable "multi_az" {
  description = "Whether the DB instance is Multi-AZ."
  type        = bool
}

variable "apply_immediately" {
  description = "Whether modifications should be applied immediately."
  type        = bool
  default     = false
}

variable "skip_final_snapshot" {
  description = "Whether a final snapshot should be skipped on destroy. Kept primarily to mirror the existing instance state."
  type        = bool
  default     = true
}

variable "tags" {
  description = "Additional tags applied to the DB instance."
  type        = map(string)
  default     = {}
}
