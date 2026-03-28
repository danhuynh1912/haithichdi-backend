output "db_instance_identifier" {
  description = "DB instance identifier."
  value       = aws_db_instance.this.id
}

output "address" {
  description = "DB endpoint address."
  value       = aws_db_instance.this.address
}

output "port" {
  description = "DB endpoint port."
  value       = aws_db_instance.this.port
}

output "db_subnet_group_name" {
  description = "DB subnet group currently attached to the instance."
  value       = aws_db_instance.this.db_subnet_group_name
}

output "vpc_security_group_ids" {
  description = "Attached VPC security groups."
  value       = aws_db_instance.this.vpc_security_group_ids
}

output "publicly_accessible" {
  description = "Whether the instance is publicly accessible."
  value       = aws_db_instance.this.publicly_accessible
}
