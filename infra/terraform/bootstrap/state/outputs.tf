output "state_bucket_name" {
  description = "Name of the Terraform remote state bucket."
  value       = aws_s3_bucket.this.bucket
}

output "state_bucket_arn" {
  description = "ARN of the Terraform remote state bucket."
  value       = aws_s3_bucket.this.arn
}

output "backend_config_example" {
  description = "Example backend.hcl content for other Terraform root modules."
  value       = <<-EOT
bucket       = "${aws_s3_bucket.this.bucket}"
region       = "${var.aws_region}"
encrypt      = true
use_lockfile = true
key          = "replace-me/terraform.tfstate"
EOT
}
