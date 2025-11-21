terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Use existing IAM role from AWS Academy (voclabs role)
data "aws_iam_role" "lambda_role" {
  name = "LabRole"
}

# Security Group for RDS
resource "aws_security_group" "rds_sg" {
  name_prefix = "rds-lambda-"
  description = "Security group for RDS accessed by Lambda"

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# RDS Instance (PostgreSQL)
resource "aws_db_instance" "vehicle_db" {
  identifier          = "lab07-vehicle-db"
  allocated_storage   = 20
  storage_type        = "gp2"
  engine               = "postgres"
  engine_version       = "13"
  instance_class       = "db.t3.micro"
  db_name              = var.db_name
  username             = var.db_username
  password             = var.db_password
  publicly_accessible  = true
  skip_final_snapshot  = true
  vpc_security_group_ids = [aws_security_group.rds_sg.id]

  tags = {
    Name = "lab07-vehicle-database"
  }
}

# Lambda Layer for Question 1 dependencies
resource "aws_lambda_layer_version" "question1_dependencies" {
  filename   = "question1_layer.zip"
  layer_name = "question1-dependencies"
  source_code_hash = filebase64sha256("question1_layer.zip")

  compatible_runtimes = ["python3.11"]
}

# Lambda Layer for Question 2 - removed for simplicity
# Using simple app without external dependencies

# Lambda Function for Question 1
resource "aws_lambda_function" "exchange_rates" {
  filename      = "question1_deployment.zip"
  function_name = "lab07-question1-exchange-rates"
  role          = data.aws_iam_role.lambda_role.arn
  handler       = "app.lambda_handler"
  runtime       = "python3.11"
  timeout       = 30

  source_code_hash = filebase64sha256("question1_deployment.zip")

  layers = [aws_lambda_layer_version.question1_dependencies.arn]

  environment {
    variables = {
      FLASK_ENV = "production"
    }
  }
}

# Lambda Function for Question 2 (without layers for now)
resource "aws_lambda_function" "vehicle_catalog" {
  filename      = "question2_deployment.zip"
  function_name = "lab07-question2-vehicle-catalog"
  role          = data.aws_iam_role.lambda_role.arn
  handler       = "simple_app.lambda_handler"
  runtime       = "python3.11"
  timeout       = 60
  memory_size   = 512

  source_code_hash = filebase64sha256("question2_deployment.zip")

  # No layers for now - using simple version

  environment {
    variables = {
      FLASK_ENV  = "production"
      DB_HOST    = aws_db_instance.vehicle_db.address
      DB_NAME    = var.db_name
      DB_USER    = var.db_username
      DB_PASSWORD = var.db_password
    }
  }

  depends_on = [aws_db_instance.vehicle_db]
}

# Lambda URLs (for AWS Academy - no API Gateway permissions)
resource "aws_lambda_function_url" "question1_url" {
  function_name          = aws_lambda_function.exchange_rates.function_name
  authorization_type     = "NONE"
  cors {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST"]
    allow_headers = ["*"]
  }
}

resource "aws_lambda_function_url" "question2_url" {
  function_name          = aws_lambda_function.vehicle_catalog.function_name
  authorization_type     = "NONE"
  cors {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST"]
    allow_headers = ["*"]
  }
}

