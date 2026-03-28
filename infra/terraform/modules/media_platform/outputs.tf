output "bucket_name" {
  description = "Name of the media bucket."
  value       = aws_s3_bucket.this.bucket
}

output "bucket_arn" {
  description = "ARN of the media bucket."
  value       = aws_s3_bucket.this.arn
}

output "cloudfront_distribution_id" {
  description = "ID of the CloudFront distribution."
  value       = aws_cloudfront_distribution.this.id
}

output "cloudfront_distribution_arn" {
  description = "ARN of the CloudFront distribution."
  value       = aws_cloudfront_distribution.this.arn
}

output "cloudfront_domain_name" {
  description = "Default CloudFront domain name."
  value       = aws_cloudfront_distribution.this.domain_name
}

output "cloudfront_hosted_zone_id" {
  description = "Hosted zone ID for alias records targeting the distribution."
  value       = aws_cloudfront_distribution.this.hosted_zone_id
}

output "media_base_url" {
  description = "Public base URL for media delivery."
  value       = length(var.cloudfront_aliases) > 0 ? "https://${var.cloudfront_aliases[0]}" : "https://${aws_cloudfront_distribution.this.domain_name}"
}

output "writer_policy_arn" {
  description = "IAM managed policy ARN that grants media write access."
  value       = aws_iam_policy.media_writer.arn
}
