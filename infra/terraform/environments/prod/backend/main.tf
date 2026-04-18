module "backend_runtime" {
  source = "../../../modules/backend_runtime"

  project_name                 = var.project_name
  environment_name             = var.environment_name
  function_name                = var.function_name
  function_description         = var.function_description
  image_uri                    = var.image_uri
  role_arn                     = var.role_arn
  role_name                    = var.role_name
  architectures                = var.architectures
  memory_size                  = var.memory_size
  timeout                      = var.timeout
  ephemeral_storage_size       = var.ephemeral_storage_size
  subnet_ids                   = local.lambda_subnet_ids
  security_group_ids           = local.lambda_security_group_ids
  lambda_environment_variables = local.lambda_environment_variables
  media_writer_policy_arn      = data.terraform_remote_state.media.outputs.writer_policy_arn
  ssm_parameter_arns           = local.secret_parameter_arns
  tracing_mode                 = var.tracing_mode
  tags                         = var.tags
}

check "runtime_secret_source_configured" {
  assert {
    condition = (
      var.runtime_use_ssm_parameter_store
      || var.inject_runtime_secrets_from_ssm
      || (
        contains(keys(var.runtime_secret_environment_variables), "POSTGRES_PASSWORD")
        && contains(keys(var.runtime_secret_environment_variables), "DJANGO_SECRET_KEY")
      )
    )
    error_message = "Runtime secret source is missing. Either keep runtime_use_ssm_parameter_store=true, set inject_runtime_secrets_from_ssm=true, or provide POSTGRES_PASSWORD and DJANGO_SECRET_KEY in runtime_secret_environment_variables."
  }
}
