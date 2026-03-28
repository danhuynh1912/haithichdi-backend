locals {
  tags = merge(
    {
      ManagedBy = "terraform"
    },
    var.tags,
    {
      Component = "database"
    },
  )
}
