locals {
  tags = merge(
    {
      Project     = var.project_name
      Environment = var.environment_name
      Component   = "terraform-state"
      ManagedBy   = "terraform"
    },
    var.tags,
  )
}
