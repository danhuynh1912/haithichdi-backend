data "aws_caller_identity" "current" {}

data "terraform_remote_state" "media" {
  backend = "s3"

  config = {
    bucket = var.state_bucket_name
    key    = var.media_state_key
    region = var.aws_region
  }
}

data "terraform_remote_state" "target_network" {
  backend = "s3"

  config = {
    bucket = var.state_bucket_name
    key    = var.network_state_key
    region = var.aws_region
  }
}

locals {
  secret_parameter_arns = [
    "arn:aws:ssm:${var.aws_region}:${data.aws_caller_identity.current.account_id}:parameter${var.postgres_password_ssm_parameter_name}",
    "arn:aws:ssm:${var.aws_region}:${data.aws_caller_identity.current.account_id}:parameter${var.django_secret_key_ssm_parameter_name}",
  ]

  lambda_subnet_ids = data.terraform_remote_state.target_network.outputs.private_app_subnet_ids

  lambda_security_group_ids = concat(
    [data.terraform_remote_state.target_network.outputs.lambda_runtime_security_group_id],
    var.additional_security_group_ids,
  )

  lambda_environment_variables = merge(
    {
      DJANGO_SETTINGS_MODULE          = var.django_settings_module
      POSTGRES_DB                     = var.postgres_db
      POSTGRES_USER                   = var.postgres_user
      POSTGRES_HOST                   = var.postgres_host
      POSTGRES_PORT                   = var.postgres_port
      POSTGRES_PASSWORD_SSM_PARAMETER = var.postgres_password_ssm_parameter_name
      DJANGO_SECRET_KEY_SSM_PARAMETER = var.django_secret_key_ssm_parameter_name
      USE_S3                          = "1"
      AWS_STORAGE_BUCKET_NAME         = data.terraform_remote_state.media.outputs.media_bucket_name
      AWS_S3_REGION_NAME              = var.aws_region
      AWS_S3_CUSTOM_DOMAIN            = data.terraform_remote_state.media.outputs.cloudfront_domain_name
      API_GATEWAY_BASE_PATH           = var.api_gateway_base_path
      FORCE_SCRIPT_NAME               = var.force_script_name
    },
    var.additional_environment_variables,
  )
}
