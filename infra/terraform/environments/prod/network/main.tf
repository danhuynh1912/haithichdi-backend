module "custom_vpc_minimal" {
  source = "../../../modules/custom_vpc_minimal"

  project_name                = var.project_name
  environment_name            = var.environment_name
  aws_region                  = var.aws_region
  vpc_cidr                    = var.vpc_cidr
  secondary_vpc_cidr_blocks   = var.secondary_vpc_cidr_blocks
  private_app_subnets         = var.private_app_subnets
  private_db_subnets          = var.private_db_subnets
  db_subnet_group_name        = var.db_subnet_group_name
  s3_gateway_endpoint_name    = var.s3_gateway_endpoint_name
  ssm_interface_endpoint_name = var.ssm_interface_endpoint_name
  s3_gateway_endpoint_policy  = var.s3_gateway_endpoint_policy
  tags                        = var.tags
}
