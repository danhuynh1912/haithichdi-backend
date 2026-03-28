# Managed RDS Instance Module

This module manages an existing Amazon RDS DB instance as Terraform state and is suitable for controlled in-place connectivity changes such as:

- moving the instance to a different DB subnet group
- changing VPC security groups
- switching between public and private accessibility

The module is intentionally conservative:

- `prevent_destroy = true` is enabled
- `engine_version` drift is ignored so routine minor-version patching doesn't create noisy plans

It is not intended to manage every possible RDS feature.
