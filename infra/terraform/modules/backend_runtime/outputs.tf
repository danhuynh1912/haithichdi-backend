output "lambda_function_name" {
  description = "Managed Lambda function name."
  value       = aws_lambda_function.this.function_name
}

output "lambda_function_arn" {
  description = "Managed Lambda function ARN."
  value       = aws_lambda_function.this.arn
}

output "lambda_role_name" {
  description = "Execution role name attached to the function."
  value       = var.role_name
}
