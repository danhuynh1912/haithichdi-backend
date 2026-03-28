# Backend Runtime Module

This module manages the production Lambda runtime configuration for the Django backend.

## Scope

- existing Lambda function configuration
- environment variables
- VPC config
- memory, timeout, ephemeral storage
- IAM attachment to the media writer policy
- IAM attachment to read named SecureString parameters from SSM Parameter Store

## Deliberate boundary

This module intentionally does **not** own Lambda image rollouts yet.

The function still requires `image_uri` because AWS Lambda needs it, but the
module ignores drift on that attribute so code deploys can remain separate from
infrastructure config while the team matures its release workflow.

## Tagging note

This module only sets workload-specific tags such as `Project`, `Environment`,
and `Component`.

Global organizational tags such as `Owner` or `ManagedBy` should come from the
root provider's `default_tags` configuration. Keeping that split avoids
duplicate tag semantics and makes resource imports cleaner.
