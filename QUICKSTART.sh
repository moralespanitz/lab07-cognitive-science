#!/bin/bash

# Lab 07 Quick Start Script
# This script guides you through the deployment process

set -e

echo "========================================="
echo "Lab 07 - AWS Services Quick Start"
echo "========================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."
echo ""

if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Install it:"
    echo "   brew install awscli"
    exit 1
fi
echo "✅ AWS CLI found: $(aws --version | head -1)"

if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform not found. Install it:"
    echo "   brew install terraform"
    exit 1
fi
echo "✅ Terraform found: $(terraform --version | head -1)"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    exit 1
fi
echo "✅ Python found: $(python3 --version)"

echo ""
echo "========================================="
echo "Step 1: Configure AWS Credentials"
echo "========================================="
echo ""

if aws sts get-caller-identity &>/dev/null; then
    echo "✅ AWS credentials already configured"
    aws sts get-caller-identity
else
    echo "Please configure AWS credentials:"
    echo "Run: aws configure"
    echo ""
    echo "You need:"
    echo "- AWS Access Key ID"
    echo "- AWS Secret Access Key"
    echo "- Region (us-east-1)"
    echo "- Output format (json)"
    exit 1
fi

echo ""
echo "========================================="
echo "Step 2: Update Configuration"
echo "========================================="
echo ""

if [ -f "terraform/terraform.tfvars" ]; then
    echo "Current settings in terraform/terraform.tfvars:"
    grep -E "^[a-z_]+" terraform/terraform.tfvars | head -10
    echo ""
    read -p "Edit terraform/terraform.tfvars? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} terraform/terraform.tfvars
    fi
fi

echo ""
echo "========================================="
echo "Step 3: Run Deployment"
echo "========================================="
echo ""

if [ ! -x "deploy.sh" ]; then
    chmod +x deploy.sh
    echo "Made deploy.sh executable"
fi

echo "Starting deployment... (this will take 5-10 minutes)"
echo ""

./deploy.sh

echo ""
echo "========================================="
echo "Deployment Complete!"
echo "========================================="
echo ""
echo "Your API Endpoints:"
echo ""
cd terraform

echo "Question 1 (Exchange Rates):"
echo "  URL: $(terraform output -raw question1_api_url 2>/dev/null || echo '{API_URL}/rates')"
echo ""

echo "Question 2 (Vehicle Catalog):"
echo "  URL: $(terraform output -raw question2_api_url 2>/dev/null || echo '{API_URL}/vehicles')"
echo ""

echo "RDS Database:"
echo "  Host: $(terraform output -raw rds_address 2>/dev/null || echo '{RDS_HOST}')"
echo ""

cd ..

echo "========================================="
echo "Next Steps:"
echo "========================================="
echo ""
echo "1. Test the APIs:"
echo "   curl \$(cd terraform && terraform output -raw question1_api_url)"
echo "   curl \$(cd terraform && terraform output -raw question2_api_url)"
echo ""
echo "2. View all outputs:"
echo "   cd terraform && terraform output"
echo ""
echo "3. Check CloudWatch logs:"
echo "   aws logs tail /aws/lambda/lab07-question1-exchange-rates --follow"
echo "   aws logs tail /aws/lambda/lab07-question2-vehicle-catalog --follow"
echo ""
echo "4. Cleanup (when done):"
echo "   cd terraform && terraform destroy"
echo ""
echo "For more details, see README.md"
echo ""
