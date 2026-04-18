# SSM Endpoint Cost Optimization Runbook

This runbook migrates the backend from runtime SSM reads to direct Lambda
environment secrets, then removes the SSM interface endpoint to reduce VPC
hourly charges.

## Preconditions

- Backend Terraform root and Network Terraform root are initialized.
- AWS credentials used by Terraform can read:
  - `/haithichdi/prod/backend/postgres_password`
  - `/haithichdi/prod/backend/django_secret_key`
- Do not apply the network stack first.

## Step 1: Apply backend runtime cutover

```bash
cd infra/terraform/environments/prod/backend
terraform plan
terraform apply
```

Expected backend changes:

- Lambda environment updated with direct secrets (`POSTGRES_PASSWORD`, `DJANGO_SECRET_KEY`)
- Runtime SSM-read IAM policy detached and removed

## Step 2: Verify Lambda configuration

```bash
aws lambda get-function-configuration \
  --function-name haithichdi-backend-api \
  --query "keys(Environment.Variables)" \
  --output json
```

Expected result:

- Key names `POSTGRES_PASSWORD` and `DJANGO_SECRET_KEY` are present
- SSM pointer variables can be absent when runtime SSM is disabled

## Step 3: Remove SSM interface endpoint

```bash
cd ../network
terraform plan
terraform apply
```

Expected network changes:

- Destroy SSM interface endpoint
- Destroy SSM endpoint security group

## Step 4: Smoke test

1. Call backend health or a lightweight API endpoint.
2. Trigger at least one cold start path (for example after publish or after idle period).
3. Check Lambda logs for no `Unable to read SSM parameter` errors.

## Rollback

If any issue appears:

1. In backend tfvars:
   - `runtime_use_ssm_parameter_store = true`
   - `inject_runtime_secrets_from_ssm = false`
2. In network tfvars:
   - `enable_ssm_interface_endpoint = true`
3. Apply backend first, then network.
