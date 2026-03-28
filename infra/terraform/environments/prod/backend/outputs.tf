output "lambda_function_name" {
  description = "Managed Lambda function name."
  value       = module.backend_runtime.lambda_function_name
}

output "lambda_function_arn" {
  description = "Managed Lambda function ARN."
  value       = module.backend_runtime.lambda_function_arn
}

output "lambda_role_name" {
  description = "Execution role name managed by the backend runtime stack."
  value       = module.backend_runtime.lambda_role_name
}

output "target_network_state_key" {
  description = "Remote state key currently feeding subnet and security group values into this cutover stack."
  value       = var.network_state_key
}

output "target_vpc_id" {
  description = "VPC ID currently targeted for the Lambda VPC config."
  value       = data.terraform_remote_state.target_network.outputs.vpc_id
}

output "target_private_app_subnet_ids" {
  description = "Subnet IDs currently targeted for the Lambda VPC config."
  value       = local.lambda_subnet_ids
}

output "target_lambda_runtime_security_group_ids" {
  description = "Security group IDs currently targeted for the Lambda VPC config."
  value       = local.lambda_security_group_ids
}
