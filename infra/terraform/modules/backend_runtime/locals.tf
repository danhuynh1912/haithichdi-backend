locals {
  tags = {
    Project     = var.project_name
    Environment = var.environment_name
    Component   = "backend-runtime"
  }
}
