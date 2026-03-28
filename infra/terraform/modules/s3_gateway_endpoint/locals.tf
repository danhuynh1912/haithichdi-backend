locals {
  tags = merge(
    {
      Name        = var.name
      Project     = var.project_name
      Environment = var.environment_name
      Component   = "network"
      ManagedBy   = "terraform"
    },
    var.tags,
  )
}
