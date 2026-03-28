data "terraform_remote_state" "target_network" {
  backend = "s3"

  config = {
    bucket = var.state_bucket_name
    key    = var.network_state_key
    region = var.aws_region
  }
}

locals {
  target_db_subnet_group_name = data.terraform_remote_state.target_network.outputs.db_subnet_group_name
  target_rds_security_group_ids = [
    data.terraform_remote_state.target_network.outputs.rds_security_group_id,
  ]
}
