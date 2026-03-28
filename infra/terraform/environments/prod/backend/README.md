# Production Backend Runtime Stack

This stack is the active Terraform owner for the production Django Lambda runtime.

## Purpose

This root exists so the team can:

- keep one Terraform root as the single owner of the live Lambda runtime
- source the Lambda network attachment from the active network remote state

## Scope

- Lambda function configuration for the existing production function
- Lambda environment variables
- Lambda VPC configuration sourced from a target network remote state
- attachment of the media writer policy to the Lambda execution role
- attachment of the SSM Parameter Store read policy to the Lambda execution role

## Important caution

This root is now active production infrastructure.

Do not make ad-hoc AWS Console edits to the Lambda runtime if the same change can be represented here first.
