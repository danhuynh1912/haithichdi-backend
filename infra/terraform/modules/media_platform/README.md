# Module: media_platform

This module provisions the core media delivery plane for the application:

- private S3 bucket
- CloudFront distribution in front of the bucket
- CloudFront Origin Access Control
- IAM managed policy for services that upload media

The module deliberately avoids owning Route 53 and ACM creation in phase 1.
That keeps the first rollout focused on fixing media uploads and serving media securely.
