output "media_bucket_name" {
  description = "Name of the production media bucket."
  value       = module.media_platform.bucket_name
}

output "media_bucket_arn" {
  description = "ARN of the production media bucket."
  value       = module.media_platform.bucket_arn
}

output "media_base_url" {
  description = "Public base URL for media assets."
  value       = module.media_platform.media_base_url
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID."
  value       = module.media_platform.cloudfront_distribution_id
}

output "cloudfront_distribution_arn" {
  description = "CloudFront distribution ARN."
  value       = module.media_platform.cloudfront_distribution_arn
}

output "cloudfront_domain_name" {
  description = "Default CloudFront domain."
  value       = module.media_platform.cloudfront_domain_name
}

output "cloudfront_hosted_zone_id" {
  description = "Hosted zone ID for future Route 53 alias records."
  value       = module.media_platform.cloudfront_hosted_zone_id
}

output "writer_policy_arn" {
  description = "IAM managed policy ARN to grant media write access."
  value       = module.media_platform.writer_policy_arn
}
