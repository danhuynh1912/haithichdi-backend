locals {
  base_tags = {
    Project     = var.project_name
    Environment = var.environment_name
    Component   = "network"
    ManagedBy   = "terraform"
  }

  tags = merge(local.base_tags, var.tags)

  private_app_subnet_map = {
    for subnet in var.private_app_subnets :
    subnet.availability_zone => subnet
  }

  private_db_subnet_map = {
    for subnet in var.private_db_subnets :
    subnet.availability_zone => subnet
  }
}
