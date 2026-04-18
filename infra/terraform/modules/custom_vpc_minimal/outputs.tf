output "vpc_id" {
  description = "ID of the custom VPC."
  value       = aws_vpc.this.id
}

output "private_app_subnet_ids" {
  description = "Private application subnet IDs."
  value       = values(aws_subnet.private_app)[*].id
}

output "private_db_subnet_ids" {
  description = "Private database subnet IDs."
  value       = values(aws_subnet.private_db)[*].id
}

output "private_app_route_table_id" {
  description = "Route table ID shared by the private app subnets."
  value       = aws_route_table.private_app.id
}

output "private_db_route_table_id" {
  description = "Route table ID shared by the private DB subnets."
  value       = aws_route_table.private_db.id
}

output "lambda_runtime_security_group_id" {
  description = "Dedicated Lambda runtime security group ID."
  value       = aws_security_group.lambda_runtime.id
}

output "rds_security_group_id" {
  description = "Dedicated RDS security group ID."
  value       = aws_security_group.rds.id
}

output "ssm_interface_endpoint_security_group_id" {
  description = "Security group ID attached to the SSM interface endpoint when enabled."
  value       = var.enable_ssm_interface_endpoint ? aws_security_group.ssm_interface_endpoint[0].id : null
}

output "db_subnet_group_name" {
  description = "DB subnet group name for the future RDS migration."
  value       = aws_db_subnet_group.this.name
}

output "s3_gateway_endpoint_id" {
  description = "S3 gateway endpoint ID."
  value       = module.s3_gateway_endpoint.vpc_endpoint_id
}

output "ssm_interface_endpoint_id" {
  description = "SSM interface endpoint ID when enabled."
  value       = var.enable_ssm_interface_endpoint ? aws_vpc_endpoint.ssm_interface[0].id : null
}
