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
- optional attachment of the SSM Parameter Store read policy to the Lambda execution role

## Secret delivery modes

This stack supports two runtime secret modes:

- `runtime_use_ssm_parameter_store = true`: Lambda reads secrets from SSM at runtime.
- `runtime_use_ssm_parameter_store = false` + `inject_runtime_secrets_from_ssm = true`:
  Terraform reads SecureString values from SSM during apply and injects
  `POSTGRES_PASSWORD` + `DJANGO_SECRET_KEY` directly into Lambda environment variables.

For cost optimization with private subnets, apply backend first with direct secret
injection, then disable the SSM interface endpoint in the network stack.

This root also enforces runtime secret source validation so an apply fails fast
if no usable secret source is configured.

## Important caution

This root is now active production infrastructure.

Do not make ad-hoc AWS Console edits to the Lambda runtime if the same change can be represented here first.
