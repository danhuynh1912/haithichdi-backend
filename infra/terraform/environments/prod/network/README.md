# Production Custom VPC Stack

This root module manages the active low-cost custom VPC production network.

## Purpose

This stack is now the active production network.

It exists so the team can:

- keep Lambda and RDS in a dedicated custom VPC instead of the AWS default VPC
- manage the production subnets, route tables, endpoints, and security groups as code
- preserve a cost-aware network shape with no NAT Gateway and only the endpoints the app currently needs

## What it creates

- one custom VPC
- two private app subnets
- three private DB subnets
- one shared app route table
- one shared DB route table
- one S3 gateway endpoint for the app route table
- one SSM interface endpoint
- dedicated security groups for Lambda, RDS, and the SSM endpoint
- one DB subnet group for the future RDS migration, including the current production RDS Availability Zone

## Cost posture

This stack is intentionally cost-aware:

- no public subnets
- no Internet Gateway
- no NAT Gateway
- no extra interface endpoints beyond SSM

## Important caution

This is no longer a blueprint-only stack. It is the live production network.

Do not repurpose or rename resources in this stack casually. Any subnet, security-group, or endpoint change here now affects live production traffic.
