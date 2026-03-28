output "vpc_id" {
  description = "ID of the custom VPC."
  value       = module.custom_vpc_minimal.vpc_id
}

output "private_app_subnet_ids" {
  description = "Private application subnet IDs."
  value       = module.custom_vpc_minimal.private_app_subnet_ids
}

output "private_db_subnet_ids" {
  description = "Private database subnet IDs."
  value       = module.custom_vpc_minimal.private_db_subnet_ids
}

output "private_app_route_table_id" {
  description = "Route table ID shared by the private app subnets."
  value       = module.custom_vpc_minimal.private_app_route_table_id
}

output "private_db_route_table_id" {
  description = "Route table ID shared by the private DB subnets."
  value       = module.custom_vpc_minimal.private_db_route_table_id
}

output "lambda_runtime_security_group_id" {
  description = "Dedicated Lambda runtime security group ID."
  value       = module.custom_vpc_minimal.lambda_runtime_security_group_id
}

output "rds_security_group_id" {
  description = "Dedicated RDS security group ID."
  value       = module.custom_vpc_minimal.rds_security_group_id
}

output "ssm_interface_endpoint_security_group_id" {
  description = "Security group ID attached to the SSM interface endpoint."
  value       = module.custom_vpc_minimal.ssm_interface_endpoint_security_group_id
}

output "db_subnet_group_name" {
  description = "DB subnet group name prepared for the future RDS migration."
  value       = module.custom_vpc_minimal.db_subnet_group_name
}

output "s3_gateway_endpoint_id" {
  description = "S3 gateway endpoint ID."
  value       = module.custom_vpc_minimal.s3_gateway_endpoint_id
}

output "ssm_interface_endpoint_id" {
  description = "SSM interface endpoint ID."
  value       = module.custom_vpc_minimal.ssm_interface_endpoint_id
}
