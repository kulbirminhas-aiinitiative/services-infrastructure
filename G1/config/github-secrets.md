# OOM GitHub Secrets Configuration
# This file lists all the secrets needed for the OOM system to function properly

## Required Secrets (Critical for system operation)

### Database & Storage
DATABASE_URL=postgresql://username:password@host:port/database
REDIS_URL=redis://password@host:port
REDIS_PASSWORD=your_redis_password

### Security & Authentication
JWT_SECRET_KEY=your_jwt_secret_key_here
ENCRYPTION_KEY=your_32_character_encryption_key
API_SECRET_KEY=your_api_secret_key_here

### Container Registry
DOCKER_REGISTRY_USERNAME=github_username
DOCKER_REGISTRY_PASSWORD=github_personal_access_token

## AI/ML Service Secrets (Optional but recommended)

### OpenAI Integration
OPENAI_API_KEY=sk-your_openai_api_key_here

### Anthropic Integration
ANTHROPIC_API_KEY=your_anthropic_api_key_here

### Hugging Face Integration
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

### Vector Database (Pinecone)
PINECONE_API_KEY=your_pinecone_api_key_here

## Cloud Provider Secrets (Choose based on your deployment)

### AWS Configuration
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
ECR_REGISTRY=123456789012.dkr.ecr.us-west-2.amazonaws.com

### Azure Configuration
AZURE_CLIENT_ID=your_azure_client_id
AZURE_CLIENT_SECRET=your_azure_client_secret
AZURE_TENANT_ID=your_azure_tenant_id
AZURE_SUBSCRIPTION_ID=your_azure_subscription_id

### Google Cloud Configuration
GCP_SERVICE_ACCOUNT_KEY=base64_encoded_service_account_json
GCP_PROJECT_ID=your_gcp_project_id

## Message Broker Secrets (If using managed services)

### Kafka (Confluent Cloud, AWS MSK, etc.)
KAFKA_USERNAME=your_kafka_username
KAFKA_PASSWORD=your_kafka_password

## Monitoring & Observability Secrets

### Grafana
GRAFANA_API_KEY=your_grafana_api_key
GRAFANA_PASSWORD=admin_password

### DataDog (Optional)
DATADOG_API_KEY=your_datadog_api_key
DATADOG_APP_KEY=your_datadog_app_key

### Prometheus (if using managed service)
PROMETHEUS_URL=https://your-prometheus-instance.com

## Notification Secrets

### Slack Integration
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK

### Email Configuration
SMTP_USERNAME=your_smtp_username
SMTP_PASSWORD=your_smtp_password

## Backup Configuration

### S3 Backup
BACKUP_S3_BUCKET=your-backup-bucket-name

## Instructions for Setting Up Secrets

1. **Using GitHub CLI (Recommended)**:
   ```bash
   # Navigate to your OOM repository
   cd /path/to/oom

   # Run the interactive setup script
   ./scripts/setup-github-secrets.sh
   ```

2. **Using GitHub Web Interface**:
   - Go to your repository: https://github.com/kulbirminhas-aiinitiative/oom
   - Navigate to Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Add each secret from the list above

3. **Using GitHub CLI manually**:
   ```bash
   # Install GitHub CLI if not already installed
   brew install gh

   # Authenticate
   gh auth login

   # Add secrets
   gh secret set DATABASE_URL
   gh secret set JWT_SECRET_KEY
   gh secret set OPENAI_API_KEY
   # ... continue for all required secrets
   ```

## Environment-Specific Secrets

### Development Environment
- Most AI/ML API keys can be omitted
- Use local database configurations
- Mock external services where possible

### Staging Environment
- Use staging/test API keys
- Configure with non-production databases
- Enable experimental features

### Production Environment
- All secrets must be properly configured
- Use production API keys and databases
- Enable all monitoring and backup features

## Security Best Practices

1. **Never commit secrets to version control**
2. **Use different secrets for different environments**
3. **Rotate secrets regularly (every 90 days recommended)**
4. **Limit secret access to necessary team members only**
5. **Use least-privilege access for API keys**
6. **Monitor secret usage and access logs**

## Validation

After setting up secrets, you can validate them using:

```bash
# Run the health check script
./scripts/health_check.py --check-secrets

# Or manually trigger the GitHub Action
gh workflow run setup-secrets.yml
```

## Troubleshooting

### Common Issues:

1. **Secret not found**: Ensure the secret name matches exactly (case-sensitive)
2. **Invalid format**: Check that secrets follow the expected format
3. **Permissions**: Ensure your GitHub token has sufficient permissions
4. **Rate limits**: API keys may have rate limits that need configuration

### Debug Commands:

```bash
# List all configured secrets (names only, not values)
gh secret list

# Check GitHub Actions logs
gh run list --workflow=ci-cd.yml

# Validate system configuration
python scripts/health_check.py --verbose
```

## Additional Notes

- The system is designed to work with minimal secrets for development
- Production deployment requires most secrets to be configured
- Some features may be disabled if related secrets are not available
- The Mind Engine and other AI components can operate in mock mode without API keys
