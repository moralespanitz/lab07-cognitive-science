#!/bin/bash
set -e

echo "=== Lab 07: AWS Services Deployment ==="
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "Error: AWS CLI is not installed"
    exit 1
fi

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "Error: Terraform is not installed"
    exit 1
fi

echo "1. Building Question 1 deployment package..."
cd question1
pip install -r requirements.txt -t python/lib/python3.11/site-packages/
zip -r ../terraform/question1_deployment.zip app.py
cd ..
rm -rf question1/python

echo ""
echo "2. Building Question 1 dependencies layer..."
mkdir -p python/lib/python3.11/site-packages
pip install -r question1/requirements.txt -t python/lib/python3.11/site-packages/
cd terraform
zip -r question1_layer.zip ../python
cd ..
rm -rf python

echo ""
echo "3. Building Question 2 deployment package..."
cd question2
pip install -r requirements.txt -t python/lib/python3.11/site-packages/
zip -r ../terraform/question2_deployment.zip app.py
cd ..
rm -rf question2/python

echo ""
echo "4. Building Question 2 dependencies layer..."
mkdir -p python/lib/python3.11/site-packages
pip install -r question2/requirements.txt -t python/lib/python3.11/site-packages/
cd terraform
zip -r question2_layer.zip ../python
cd ..
rm -rf python

echo ""
echo "5. Initializing Terraform..."
cd terraform
terraform init

echo ""
echo "6. Planning Terraform deployment..."
terraform plan -out=tfplan

echo ""
echo "7. Applying Terraform configuration..."
terraform apply tfplan

echo ""
echo "=== Deployment Complete ==="
echo ""
echo "API Endpoints:"
echo "Question 1 (Exchange Rates): $(terraform output -raw question1_api_url)"
echo "Question 2 (Vehicle Catalog): $(terraform output -raw question2_api_url)"
echo "RDS Endpoint: $(terraform output -raw rds_endpoint)"
