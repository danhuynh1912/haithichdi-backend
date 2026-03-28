# Terraform Layout

This repository uses a layered Terraform layout instead of putting every resource into one flat folder.

## Structure

```text
infra/terraform/
  bootstrap/
    state/                       # creates the remote-state bucket for Terraform itself
  modules/
    backend_runtime/             # reusable building block for Lambda runtime config
    custom_vpc_minimal/          # reusable building block for the low-cost custom VPC shape
    media_platform/              # reusable building block for media delivery
    s3_gateway_endpoint/         # reusable building block for S3 gateway endpoint networking
    rds_instance/                # reusable building block for the production RDS instance
  environments/
    prod/
      backend/                   # current production owner for the Lambda runtime
      database/                  # current production owner for the RDS instance
      media/                     # production root module for shared media infra
      network/                   # current production custom VPC hosting the backend runtime and RDS
```

## Why this structure

- `modules/` contains reusable building blocks with no environment-specific values.
- `environments/` contains deployable roots with concrete values for `prod`, and later `staging` or `dev`.
- `bootstrap/` contains one-time foundation stacks that exist to support Terraform workflows themselves.
- shared infrastructure such as media storage lives at the repository root because it serves both backend and frontend.

## Current scope

Implemented in this phase:

- bootstrap stack for a remote Terraform state bucket
- backend stack for the active Lambda runtime config and env vars
- database stack for the active production RDS instance
- network stack for the active low-cost custom VPC
- private S3 bucket for media objects
- CloudFront distribution with Origin Access Control
- IAM managed policy for backend writers
- SSM Parameter Store SecureString secrets for backend runtime values

Legacy cleanup completed in this phase:

- old Lambda runtime security group in the default VPC
- old S3 gateway endpoint in the default VPC
- old SSM interface endpoint and its security group in the default VPC
- old PostgreSQL ingress rule from the legacy Lambda security group
- old manual RDS snapshot created only for the migration

Deferred to later phases:

- Route 53 records
- ACM certificate provisioning for custom media domain
- CloudFront logging and WAF
- API Gateway custom domain and mapping ownership
- CloudWatch log retention, alarms, and budgets
- multi-environment expansion such as `staging`
