variable "aws_region" {
  description = "AWS region for the backend runtime."
  type        = string
}

variable "state_bucket_name" {
  description = "S3 bucket that stores Terraform remote state."
  type        = string
}

variable "media_state_key" {
  description = "Remote state key for the media stack."
  type        = string
  default     = "shared/media/prod/terraform.tfstate"
}

variable "network_state_key" {
  description = "Remote state key for the active network stack."
  type        = string
  default     = "network/prod/terraform.tfstate"
}

variable "project_name" {
  description = "Logical project name."
  type        = string
}

variable "environment_name" {
  description = "Environment name."
  type        = string
  default     = "prod"
}

variable "function_name" {
  description = "Existing Lambda function name."
  type        = string
}

variable "function_description" {
  description = "Lambda function description."
  type        = string
  default     = ""
}

variable "image_uri" {
  description = "Current image URI of the Lambda function."
  type        = string
}

variable "role_arn" {
  description = "Execution role ARN."
  type        = string
}

variable "role_name" {
  description = "Execution role name."
  type        = string
}

variable "memory_size" {
  description = "Lambda memory size in MB."
  type        = number
  default     = 512
}

variable "timeout" {
  description = "Lambda timeout in seconds."
  type        = number
  default     = 20
}

variable "architectures" {
  description = "Lambda architectures."
  type        = list(string)
  default     = ["x86_64"]
}

variable "ephemeral_storage_size" {
  description = "Lambda ephemeral storage size in MB."
  type        = number
  default     = 512
}

variable "additional_security_group_ids" {
  description = "Optional extra security groups appended to the dedicated Lambda runtime security group from the target network stack."
  type        = list(string)
  default     = []
}

variable "django_settings_module" {
  description = "DJANGO_SETTINGS_MODULE value."
  type        = string
  default     = "backend.settings"
}

variable "postgres_db" {
  description = "PostgreSQL database name."
  type        = string
}

variable "postgres_user" {
  description = "PostgreSQL username."
  type        = string
}

variable "postgres_host" {
  description = "PostgreSQL host."
  type        = string
}

variable "postgres_port" {
  description = "PostgreSQL port."
  type        = string
  default     = "5432"
}

variable "postgres_password_ssm_parameter_name" {
  description = "SSM Parameter Store name that holds the PostgreSQL password."
  type        = string
  default     = null
  nullable    = true

  validation {
    condition = (
      var.runtime_use_ssm_parameter_store == false && var.inject_runtime_secrets_from_ssm == false
      || (
        var.postgres_password_ssm_parameter_name != null
        && trimspace(var.postgres_password_ssm_parameter_name) != ""
      )
    )
    error_message = "Set postgres_password_ssm_parameter_name when runtime_use_ssm_parameter_store or inject_runtime_secrets_from_ssm is true."
  }
}

variable "django_secret_key_ssm_parameter_name" {
  description = "SSM Parameter Store name that holds DJANGO_SECRET_KEY."
  type        = string
  default     = null
  nullable    = true

  validation {
    condition = (
      var.runtime_use_ssm_parameter_store == false && var.inject_runtime_secrets_from_ssm == false
      || (
        var.django_secret_key_ssm_parameter_name != null
        && trimspace(var.django_secret_key_ssm_parameter_name) != ""
      )
    )
    error_message = "Set django_secret_key_ssm_parameter_name when runtime_use_ssm_parameter_store or inject_runtime_secrets_from_ssm is true."
  }
}

variable "runtime_use_ssm_parameter_store" {
  description = "Whether Lambda reads secrets from SSM Parameter Store at runtime."
  type        = bool
  default     = true
}

variable "inject_runtime_secrets_from_ssm" {
  description = "Whether Terraform reads secure values from SSM and injects them directly into Lambda environment variables."
  type        = bool
  default     = false
}

variable "runtime_secret_environment_variables" {
  description = "Direct secret environment variables injected into Lambda runtime (for example DJANGO_SECRET_KEY, POSTGRES_PASSWORD)."
  type        = map(string)
  default     = {}
  sensitive   = true
}

variable "api_gateway_base_path" {
  description = "Legacy API Gateway base path env var retained to match the current runtime."
  type        = string
  default     = "/default"
}

variable "force_script_name" {
  description = "Legacy Django script prefix env var retained to match the current runtime."
  type        = string
  default     = "/default"
}

variable "cors_allowed_origins" {
  description = "Allowed browser origins for Django CORS handling."
  type        = list(string)
  default     = []
}

variable "csrf_trusted_origins" {
  description = "Trusted origins for Django CSRF handling."
  type        = list(string)
  default     = []
}

variable "tracing_mode" {
  description = "Lambda tracing mode."
  type        = string
  default     = "PassThrough"
}

variable "additional_environment_variables" {
  description = "Extra environment variables merged into the Lambda configuration."
  type        = map(string)
  default     = {}
}

variable "tags" {
  description = "Additional tags applied to managed resources."
  type        = map(string)
  default     = {}
}
