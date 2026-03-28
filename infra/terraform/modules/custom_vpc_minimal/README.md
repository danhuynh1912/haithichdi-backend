# custom_vpc_minimal

Reusable Terraform module for a cost-aware custom VPC that fits the current Hai Thich Di backend architecture.

## What it creates

- one custom VPC
- two private app subnets
- two private DB subnets
- one shared private app route table
- one shared private DB route table
- S3 gateway endpoint for the app route table
- one SSM interface endpoint across the private app subnets
- dedicated security groups for Lambda, RDS, and the SSM endpoint
- one DB subnet group for the future RDS migration

## Design goals

- keep Lambda and RDS private
- avoid NAT Gateway at the first phase to save cost
- open only the paths the current application needs:
  - Lambda -> RDS
  - Lambda -> S3
  - Lambda -> SSM

## What it intentionally does not create

- public subnets
- Internet Gateway
- NAT Gateway
- ALB
- extra interface endpoints beyond SSM
