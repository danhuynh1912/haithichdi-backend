# Environment Variables

This file is the single reference for configuration variables used by the frontend and backend.

The goal is simple:

- keep secrets out of Git
- keep public frontend values separate from backend secrets
- make it obvious where each value should live

## The Rule

Use these four buckets:

| Bucket | What goes here | Example |
| --- | --- | --- |
| Local template | Example values for local development | `.env.example`, `env.aws.example` |
| Frontend public build config | Values safe to expose in the browser | `NEXT_PUBLIC_API_BASE_URL` |
| Backend runtime config | Non-secret values injected into Lambda | `POSTGRES_HOST`, `AWS_S3_CUSTOM_DOMAIN` |
| Secret store | Real secrets only | `DJANGO_SECRET_KEY`, `POSTGRES_PASSWORD` |

## Source Of Truth

### Frontend production

Frontend production variables are managed by Amplify Terraform.

Primary source:

- `../frontend/infra/terraform/amplify/locals.tf`
- `../frontend/infra/terraform/amplify/terraform.tfvars`

Local template:

- `../frontend/.env.example`

### Backend production

Backend non-secret runtime config is managed by backend Terraform.

Primary source:

- `../infra/terraform/environments/prod/backend/locals.tf`

Backend secrets are stored in AWS SSM Parameter Store SecureString and loaded at runtime by Django.

Primary source:

- `../backend/backend/settings.py`

Local template:

- `../backend/env.aws.example`

## Frontend Variables

These values are public by design. If a variable starts with `NEXT_PUBLIC_`, assume it can be seen in the browser.

| Variable | Purpose | Secret? | Production source |
| --- | --- | --- | --- |
| `NEXT_PUBLIC_API_BASE_URL` | Browser-side API base URL | No | Amplify Terraform |
| `SERVER_API_BASE_URL` | Server-side fetch base URL for SSR/metadata | No | Amplify Terraform |
| `NEXT_PUBLIC_SITE_URL` | Canonical URL and social metadata base | No | Amplify Terraform |
| `NEXT_PUBLIC_MEDIA_BASE_URL` | Media/image origin allow-list and public media base | No | Amplify Terraform |

### Frontend notes

- `NEXT_PUBLIC_API_BASE_URL` is used by client-side calls in `../frontend/lib/api.ts`.
- `SERVER_API_BASE_URL` is used by server-side data fetch in `../frontend/app/tour-booking/[tourId]/page.tsx`.
- `NEXT_PUBLIC_SITE_URL` is used for SEO metadata in `../frontend/lib/seo.ts`.
- `NEXT_PUBLIC_MEDIA_BASE_URL` is used by `../frontend/next.config.ts` for remote image patterns.

## Backend Variables

Backend variables split into two groups: runtime config and secrets.

### Backend runtime config

| Variable | Purpose | Secret? | Production source |
| --- | --- | --- | --- |
| `DJANGO_DEBUG` | Turns Django debug on or off | No | Lambda env via Terraform |
| `DJANGO_SETTINGS_MODULE` | Django settings module | No | Lambda env via Terraform |
| `POSTGRES_DB` | Database name | No | Lambda env via Terraform |
| `POSTGRES_USER` | Database user name | No | Lambda env via Terraform |
| `POSTGRES_HOST` | Database host | No | Lambda env via Terraform |
| `POSTGRES_PORT` | Database port | No | Lambda env via Terraform |
| `USE_S3` | Enable S3 storage mode | No | Lambda env via Terraform |
| `AWS_STORAGE_BUCKET_NAME` | S3 bucket used for media | No | Lambda env via Terraform |
| `AWS_S3_REGION_NAME` | AWS region for media bucket | No | Lambda env via Terraform |
| `AWS_S3_CUSTOM_DOMAIN` | Public media domain, now CloudFront | No | Lambda env via Terraform |
| `API_GATEWAY_BASE_PATH` | API stage/base path compatibility | No | Lambda env via Terraform |
| `FORCE_SCRIPT_NAME` | Django path prefix compatibility | No | Lambda env via Terraform |

### Backend secrets

| Variable | Purpose | Secret? | Production source |
| --- | --- | --- | --- |
| `DJANGO_SECRET_KEY` | Django signing secret | Yes | SSM SecureString |
| `POSTGRES_PASSWORD` | Database password | Yes | SSM SecureString |

Production does not inject these two values directly. Instead, Lambda receives parameter names:

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY_SSM_PARAMETER` | SSM parameter name for Django secret |
| `POSTGRES_PASSWORD_SSM_PARAMETER` | SSM parameter name for DB password |

Django reads those parameter names in `../backend/backend/settings.py` and fetches the real secret from SSM.

## Local-Only Variables

These are allowed for local development, but they should not be part of AWS production config.

| Variable | Why local only |
| --- | --- |
| `DJANGO_SECRET_KEY` | Plaintext fallback for local only |
| `POSTGRES_PASSWORD` | Plaintext fallback for local only |
| `AWS_ACCESS_KEY_ID` | Not needed in Lambda when IAM role is used |
| `AWS_SECRET_ACCESS_KEY` | Not needed in Lambda when IAM role is used |
| `AWS_S3_ENDPOINT_URL` | Used for MinIO or custom S3-compatible local setup |
| `AWS_S3_PUBLIC_ENDPOINT_URL` | Local compatibility only |
| `AWS_S3_PUBLIC_BASE_URL` | Local compatibility only |
| `AWS_S3_ADDRESSING_STYLE` | Local MinIO compatibility only |

## What Good Looks Like

The clean operating model for this project is:

1. Local examples live in `.env.example` files.
2. Frontend production public config lives in Amplify Terraform.
3. Backend production non-secret config lives in backend Terraform.
4. Backend production secrets live in SSM Parameter Store.
5. No real secret is committed to Git.
6. Console edits are avoided when Terraform already owns that setting.

## What To Avoid

Do not do these things:

- do not put `DJANGO_SECRET_KEY` or `POSTGRES_PASSWORD` into Git
- do not move frontend `NEXT_PUBLIC_*` values into secret storage
- do not put backend secrets into Amplify environment variables
- do not keep changing production values by hand in AWS Console if Terraform already owns them
- do not treat local `.env` files as the source of truth for production

## Quick Decision Guide

If you add a new variable, decide like this:

| Question | Put it here |
| --- | --- |
| Will the browser see it? | Frontend env / Amplify |
| Is it sensitive? | SSM Parameter Store |
| Is it backend-only and not sensitive? | Backend Terraform |
| Is it only for local development? | `.env.example` template |

## Current Production Shape

At the moment, the production contract is:

- frontend public config comes from Amplify branch environment variables
- backend runtime config comes from Terraform-managed Lambda environment variables
- backend secrets come from SSM SecureString parameters
- media public URL goes through CloudFront

That is the model to keep going forward.
