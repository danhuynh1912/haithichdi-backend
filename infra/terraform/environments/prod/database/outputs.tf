output "db_instance_identifier" {
  description = "Managed DB instance identifier."
  value       = module.rds_instance.db_instance_identifier
}

output "address" {
  description = "DB endpoint address."
  value       = module.rds_instance.address
}

output "port" {
  description = "DB endpoint port."
  value       = module.rds_instance.port
}

output "db_subnet_group_name" {
  description = "DB subnet group attached after apply."
  value       = module.rds_instance.db_subnet_group_name
}

output "vpc_security_group_ids" {
  description = "Attached VPC security groups."
  value       = module.rds_instance.vpc_security_group_ids
}

output "publicly_accessible" {
  description = "Whether the DB is publicly accessible."
  value       = module.rds_instance.publicly_accessible
}
