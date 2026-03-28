# Terraform Bootstrap State Stack

This stack creates the S3 bucket that stores Terraform remote state for the rest of the project.

## Why this stack exists

Terraform cannot use an S3 backend before the S3 bucket itself exists.

That creates a chicken-and-egg problem:

- you want remote state
- but the bucket for remote state must be created first

The standard solution is a small bootstrap stack that runs once with local state and creates the state bucket.

After that, the other Terraform root modules can migrate from local state to the remote S3 backend.

## What it creates

- a dedicated S3 bucket for Terraform state
- bucket versioning
- SSE-S3 encryption
- public access block
- bucket ownership controls
- a lifecycle rule for noncurrent object versions
- a bucket policy that denies insecure transport

## What it does not create

- KMS customer-managed key
- DynamoDB lock table

This project uses the modern S3 backend lockfile flow instead:

- `use_lockfile = true`

That keeps phase 1 simpler and cheaper.

## How to use

1. Copy `terraform.tfvars.example` to `terraform.tfvars`.
2. Review the bucket name carefully. It must be globally unique.
3. Run:

```bash
cd infra/terraform/bootstrap/state
terraform init
terraform plan
terraform apply
```

4. Capture the output `state_bucket_name`.
5. Copy the relevant `backend.hcl.example` file in each Terraform root module to `backend.hcl`.
6. Replace the bucket name if needed.
7. Run `terraform init -migrate-state -backend-config=backend.hcl` in each Terraform root you want to migrate.

## Recommended backend keys

- media stack:
  - `shared/media/prod/terraform.tfstate`
- frontend amplify stack:
  - `frontend/amplify/prod/terraform.tfstate`

## Safety notes

- Do not delete this bucket casually. It is not an ordinary application bucket.
- Keep versioning enabled.
- Do not turn on `force_destroy` unless you intentionally want destructive behavior.
