output "vpc_endpoint_id" {
  description = "ID of the managed S3 gateway endpoint."
  value       = aws_vpc_endpoint.this.id
}
