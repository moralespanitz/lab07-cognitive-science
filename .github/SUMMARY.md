# Lab 07 Summary

## Completed Deliverables

### Question 1: Exchange Rate API (7 pts)
- Flask application that fetches USD, EUR, SOL exchange rates
- Uses exchangerate-api.com for real-time data
- Deployed as AWS Lambda function
- Endpoints: `/rates`, `/health`
- Terraform infrastructure with API Gateway integration

### Question 2: Vehicle Catalog API (13 pts)
- Flask application with vehicle catalog management
- PostgreSQL database (AWS RDS) for data storage
- Auto-initializes with 8 sample vehicles
- Endpoints: `/vehicles`, `/vehicle/{id}`, `/health`
- Terraform infrastructure with VPC and RDS integration

## Infrastructure Components

### AWS Services Used:
1. **Lambda Functions** (2x)
   - question1-exchange-rates
   - question2-vehicle-catalog

2. **API Gateway** (2x)
   - HTTP API endpoints with CORS
   - Integration with Lambda functions

3. **RDS Database**
   - PostgreSQL 14.7
   - db.t3.micro instance
   - Auto-initialization on first Lambda execution

4. **IAM Roles & Policies**
   - Lambda execution role
   - RDS access permissions
   - VPC networking for database access

5. **Security Groups**
   - RDS access from Lambda
   - PostgreSQL port 5432 open

## Files Structure

```
lab07/
├── question1/
│   ├── app.py              (Flask app for exchange rates)
│   └── requirements.txt    (Python dependencies)
├── question2/
│   ├── app.py              (Flask app for vehicle catalog)
│   └── requirements.txt    (Python dependencies)
├── terraform/
│   ├── main.tf             (Main infrastructure)
│   ├── variables.tf        (Variable definitions)
│   ├── outputs.tf          (Output definitions)
│   └── terraform.tfvars    (Configuration values)
├── deploy.sh               (Automated deployment script)
├── README.md               (Comprehensive guide)
├── DEPLOYMENT_GUIDE.txt    (Quick reference)
└── .github/SUMMARY.md      (This file)
```

## Deployment Summary

### Automated Deployment:
```bash
./deploy.sh
```

### Manual Deployment:
1. Build packages
2. Create Lambda layers
3. Run terraform init
4. Run terraform plan
5. Run terraform apply

## API Endpoints

### Question 1:
- GET `/rates` - Exchange rates (USD, EUR, PEN)
- GET `/health` - Health check

### Question 2:
- GET `/vehicles` - List all vehicles
- GET `/vehicle/{id}` - Get vehicle by ID
- GET `/health` - Health check

## Database Schema

```sql
CREATE TABLE vehicles (
  id SERIAL PRIMARY KEY,
  brand VARCHAR(100),
  model VARCHAR(100),
  year INTEGER,
  price DECIMAL(10, 2),
  color VARCHAR(50),
  engine VARCHAR(50),
  fuel_type VARCHAR(50)
);
```

Sample data includes 8 vehicles (Toyota, Honda, Ford, Tesla, BMW, Audi, Mazda, Volkswagen).

## Technology Stack

- **Runtime**: Python 3.11
- **Framework**: Flask 2.3.0
- **Database**: PostgreSQL 14.7
- **IaC**: Terraform 1.x
- **Cloud**: AWS (Lambda, API Gateway, RDS)
- **External API**: exchangerate-api.com

## Cost Estimate

- Lambda: ~$0.20/month (free tier: 1M requests/month)
- RDS: ~$10-15/month
- API Gateway: Free tier covered
- **Total**: ~$15-20/month after free tier

## Key Features

✅ Infrastructure as Code (Terraform)
✅ Serverless deployment (Lambda)
✅ Managed database (RDS)
✅ Auto-scaling API endpoints
✅ CORS-enabled APIs
✅ Database auto-initialization
✅ Real-time exchange rates
✅ Complete documentation

## Cleanup

```bash
cd terraform
terraform destroy
```

This removes all AWS resources created.

---

**Status**: ✅ Complete
**Total Points**: 20 pts (7 + 13)
