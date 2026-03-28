locals {
  name_prefix = "${var.project_name}-${var.environment_name}-media"
  origin_id   = "${local.name_prefix}-origin"

  tags = merge(
    {
      Project     = var.project_name
      Environment = var.environment_name
      Component   = "media"
      ManagedBy   = "terraform"
    },
    var.tags,
  )
}
