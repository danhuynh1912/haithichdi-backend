data "aws_region" "current" {}

data "aws_iam_policy_document" "parameter_store_read" {
  count = length(var.ssm_parameter_arns) == 0 ? 0 : 1

  statement {
    sid    = "AllowReadNamedParameters"
    effect = "Allow"

    actions = [
      "ssm:GetParameter",
      "ssm:GetParameters",
    ]

    resources = var.ssm_parameter_arns
  }

  statement {
    sid    = "AllowDecryptNamedParametersViaSSM"
    effect = "Allow"

    actions = [
      "kms:Decrypt",
    ]

    resources = ["*"]

    condition {
      test     = "StringEquals"
      variable = "kms:ViaService"
      values   = ["ssm.${data.aws_region.current.name}.amazonaws.com"]
    }

    condition {
      test     = "ForAnyValue:StringEquals"
      variable = "kms:EncryptionContext:PARAMETER_ARN"
      values   = var.ssm_parameter_arns
    }
  }
}

resource "aws_lambda_function" "this" {
  function_name = var.function_name
  description   = var.function_description
  role          = var.role_arn
  package_type  = "Image"
  image_uri     = var.image_uri
  timeout       = var.timeout
  memory_size   = var.memory_size
  architectures = var.architectures

  ephemeral_storage {
    size = var.ephemeral_storage_size
  }

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = var.security_group_ids
  }

  environment {
    variables = var.lambda_environment_variables
  }

  tracing_config {
    mode = var.tracing_mode
  }

  lifecycle {
    # Image rollouts can stay in a separate release workflow while Terraform
    # owns runtime configuration, networking, and environment variables.
    ignore_changes = [image_uri]
  }

  tags = local.tags
}

resource "aws_iam_role_policy_attachment" "media_writer" {
  role       = var.role_name
  policy_arn = var.media_writer_policy_arn
}

resource "aws_iam_policy" "parameter_store_read" {
  count = length(var.ssm_parameter_arns) == 0 ? 0 : 1

  name        = "${var.project_name}-${var.environment_name}-backend-ssm-read"
  description = "Read named SecureString parameters for the backend runtime"
  policy      = data.aws_iam_policy_document.parameter_store_read[0].json

  tags = local.tags
}

resource "aws_iam_role_policy_attachment" "parameter_store_read" {
  count = length(var.ssm_parameter_arns) == 0 ? 0 : 1

  role       = var.role_name
  policy_arn = aws_iam_policy.parameter_store_read[0].arn
}
