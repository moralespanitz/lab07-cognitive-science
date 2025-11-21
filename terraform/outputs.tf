output "question1_api_url" {
  description = "Question 1 - Exchange Rates API URL"
  value       = "${aws_lambda_function_url.question1_url.function_url}rates"
}

output "question1_health_url" {
  description = "Question 1 - Health check URL"
  value       = "${aws_lambda_function_url.question1_url.function_url}health"
}

output "question2_api_url" {
  description = "Question 2 - Vehicle Catalog API URL"
  value       = "${aws_lambda_function_url.question2_url.function_url}vehicles"
}

output "question2_vehicle_detail_url" {
  description = "Question 2 - Vehicle detail API URL (replace {id} with vehicle ID)"
  value       = "${aws_lambda_function_url.question2_url.function_url}vehicle/{id}"
}

output "rds_endpoint" {
  description = "RDS PostgreSQL endpoint"
  value       = aws_db_instance.vehicle_db.endpoint
}

output "rds_address" {
  description = "RDS PostgreSQL address only"
  value       = aws_db_instance.vehicle_db.address
}

output "lambda_question1_name" {
  description = "Question 1 Lambda function name"
  value       = aws_lambda_function.exchange_rates.function_name
}

output "lambda_question2_name" {
  description = "Question 2 Lambda function name"
  value       = aws_lambda_function.vehicle_catalog.function_name
}
