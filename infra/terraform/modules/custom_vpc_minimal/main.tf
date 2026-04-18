resource "aws_vpc" "this" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = merge(
    local.tags,
    {
      Name = "${var.project_name}-${var.environment_name}-vpc"
    },
  )
}

resource "aws_vpc_ipv4_cidr_block_association" "secondary" {
  for_each = toset(var.secondary_vpc_cidr_blocks)

  vpc_id     = aws_vpc.this.id
  cidr_block = each.value
}

resource "aws_subnet" "private_app" {
  for_each = local.private_app_subnet_map

  vpc_id                  = aws_vpc.this.id
  availability_zone       = each.value.availability_zone
  cidr_block              = each.value.cidr_block
  map_public_ip_on_launch = false

  tags = merge(
    local.tags,
    {
      Name = "${var.project_name}-${var.environment_name}-private-app-${replace(each.value.availability_zone, "${var.aws_region}", "")}"
      Tier = "app"
    },
  )

  depends_on = [aws_vpc_ipv4_cidr_block_association.secondary]
}

resource "aws_subnet" "private_db" {
  for_each = local.private_db_subnet_map

  vpc_id                  = aws_vpc.this.id
  availability_zone       = each.value.availability_zone
  cidr_block              = each.value.cidr_block
  map_public_ip_on_launch = false

  tags = merge(
    local.tags,
    {
      Name = "${var.project_name}-${var.environment_name}-private-db-${replace(each.value.availability_zone, "${var.aws_region}", "")}"
      Tier = "db"
    },
  )

  depends_on = [aws_vpc_ipv4_cidr_block_association.secondary]
}

resource "aws_route_table" "private_app" {
  vpc_id = aws_vpc.this.id

  tags = merge(
    local.tags,
    {
      Name = "${var.project_name}-${var.environment_name}-private-app-rt"
      Tier = "app"
    },
  )
}

resource "aws_route_table" "private_db" {
  vpc_id = aws_vpc.this.id

  tags = merge(
    local.tags,
    {
      Name = "${var.project_name}-${var.environment_name}-private-db-rt"
      Tier = "db"
    },
  )
}

resource "aws_route_table_association" "private_app" {
  for_each = aws_subnet.private_app

  subnet_id      = each.value.id
  route_table_id = aws_route_table.private_app.id
}

resource "aws_route_table_association" "private_db" {
  for_each = aws_subnet.private_db

  subnet_id      = each.value.id
  route_table_id = aws_route_table.private_db.id
}

module "s3_gateway_endpoint" {
  source = "../s3_gateway_endpoint"

  project_name     = var.project_name
  environment_name = var.environment_name
  aws_region       = var.aws_region
  vpc_id           = aws_vpc.this.id
  route_table_ids  = [aws_route_table.private_app.id]
  policy           = var.s3_gateway_endpoint_policy
  name             = var.s3_gateway_endpoint_name
  tags = merge(
    var.tags,
    {
      Component = "network"
    },
  )
}

resource "aws_security_group" "lambda_runtime" {
  name        = "${var.project_name}-${var.environment_name}-v2-lambda-runtime-sg"
  description = "Dedicated security group for backend Lambda runtimes in the custom VPC"
  vpc_id      = aws_vpc.this.id

  tags = merge(
    local.tags,
    {
      Name = "${var.project_name}-${var.environment_name}-v2-lambda-runtime-sg"
      Role = "lambda-runtime"
    },
  )
}

resource "aws_vpc_security_group_egress_rule" "lambda_runtime_all" {
  security_group_id = aws_security_group.lambda_runtime.id
  description       = "Allow outbound traffic from Lambda runtimes; routes still keep the VPC private"
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

resource "aws_security_group" "rds" {
  name        = "${var.project_name}-${var.environment_name}-v2-rds-sg"
  description = "Dedicated security group for RDS in the custom VPC"
  vpc_id      = aws_vpc.this.id

  tags = merge(
    local.tags,
    {
      Name = "${var.project_name}-${var.environment_name}-v2-rds-sg"
      Role = "rds"
    },
  )
}

resource "aws_vpc_security_group_ingress_rule" "rds_from_lambda" {
  security_group_id            = aws_security_group.rds.id
  referenced_security_group_id = aws_security_group.lambda_runtime.id
  description                  = "Allow PostgreSQL from the Lambda runtime security group"
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
}

resource "aws_security_group" "ssm_interface_endpoint" {
  count = var.enable_ssm_interface_endpoint ? 1 : 0

  name        = "${var.project_name}-${var.environment_name}-v2-ssm-vpce-sg"
  description = "Allows Lambda runtimes to reach the SSM interface endpoint over HTTPS"
  vpc_id      = aws_vpc.this.id

  ingress {
    description     = "HTTPS from the Lambda runtime security group"
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.lambda_runtime.id]
  }

  egress {
    description = "Allow outbound traffic from the endpoint ENIs"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    local.tags,
    {
      Name = "${var.project_name}-${var.environment_name}-v2-ssm-vpce-sg"
      Role = "ssm-endpoint"
    },
  )
}

resource "aws_vpc_endpoint" "ssm_interface" {
  count = var.enable_ssm_interface_endpoint ? 1 : 0

  vpc_id              = aws_vpc.this.id
  service_name        = "com.amazonaws.${var.aws_region}.ssm"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = values(aws_subnet.private_app)[*].id
  security_group_ids  = [aws_security_group.ssm_interface_endpoint[0].id]
  private_dns_enabled = true

  tags = merge(
    local.tags,
    {
      Name = var.ssm_interface_endpoint_name
    },
  )
}

resource "aws_db_subnet_group" "this" {
  name       = var.db_subnet_group_name
  subnet_ids = values(aws_subnet.private_db)[*].id

  tags = merge(
    local.tags,
    {
      Name = var.db_subnet_group_name
    },
  )
}
