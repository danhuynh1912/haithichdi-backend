# Production Media Stack

This stack is the production root for shared media infrastructure.

## What it creates

- private S3 bucket for uploaded images and PDFs
- CloudFront distribution with Origin Access Control
- IAM managed policy for upload-capable backend roles
- optional attachment of that policy to existing IAM roles

## Why this stack is separate from Amplify

Media storage is shared infrastructure:

- backend writes objects
- frontend reads media through CloudFront
- the bucket has a different lifecycle from frontend deployments

Putting it inside the Amplify stack would create the wrong coupling boundary.

## How to use

1. Copy `terraform.tfvars.example` to `terraform.tfvars`.
2. Fill in the real bucket name and IAM role names.
3. Leave `cloudfront_aliases = []` for phase 1 if you want to start with the default CloudFront domain.
4. Run:

```bash
terraform init
terraform plan
terraform apply
```

## Outputs you will use next

After apply, capture:

- `media_bucket_name`
- `media_base_url`
- `writer_policy_arn`

These are the values you will need for:

- backend storage configuration
- frontend `NEXT_PUBLIC_MEDIA_BASE_URL`
- IAM validation for Lambda and ECS

## Choosing `writer_role_names`

Use IAM role names for the compute runtimes that actually upload files:

- Lambda execution role for the Django API
- ECS task role for the Django API, if ECS also serves upload traffic

Avoid using ECS task execution roles unless they also need S3 object access.

If you do not know the names yet, leave `writer_role_names = []`, apply the stack, and attach `writer_policy_arn` manually first. You can add the role names into Terraform once you confirm the exact runtime roles.

## Output to application mapping

Use the Terraform outputs as the source of truth:

- `media_bucket_name`
  Feed this into backend storage config as the bucket identifier.

- `media_base_url`
  Feed this into frontend as `NEXT_PUBLIC_MEDIA_BASE_URL`.
  Feed this into backend storage config as the public media domain once the backend stops using MinIO-style URL assembly.

- `writer_policy_arn`
  Confirm this policy is attached to the Lambda role and/or ECS task role that uploads images and PDFs.

Note:

- the backend storage settings now support native AWS S3 + CloudFront for production and MinIO for local development.
- if uploads still fail after Terraform apply and IAM attachment, the next things to verify are backend env vars, runtime redeploy, and S3 network reachability from a VPC-attached Lambda.

## Phase 2

When phase 1 is stable, add:

- ACM certificate in `us-east-1`
- `media.haithichdi.com` as a CloudFront alias
- Route 53 alias record
- remote Terraform state

## Runbook

For the exact rollout sequence across Terraform, IAM, backend env vars, frontend env vars, and verification, use:

- `localDocs/infra/terraform/environments/prod/media/DEPLOYMENT_RUNBOOK.md`
