# Production Database Stack

This stack manages the production RDS instance inside the active custom VPC network.

## Scope

- existing production RDS DB instance `haithichdi-db`
- network placement through the target DB subnet group
- attached RDS security group in the target VPC
- public versus private accessibility during the cutover

## Safety posture

- `prevent_destroy = true` on the DB instance resource
- the stack reads the target DB subnet group and RDS security group from the active network remote state

## Important caution

For future changes, keep `prevent_destroy = true` and treat this root as the single source of truth for the production database.
