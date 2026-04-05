#!/bin/bash

# ============================================================================
# DEPLOYMENT SCRIPT FOR GOOGLE CLOUD RUN
# ============================================================================

PROJECT_ID="your-project-id"
SERVICE_NAME="ai-video-editor"
REGION="us-central1"

echo "🚀 Deploying to Google Cloud Run"
echo "=================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Install it first:"
    echo "curl https://sdk.cloud.google.com | bash"
    exit 1
fi

# Authenticate
echo "🔐 Authenticating with Google Cloud..."
gcloud auth login
gcloud config set project $PROJECT_ID

# Create .dockerignore if it doesn't exist
echo "📝 Creating .dockerignore..."
cat > .dockerignore <<EOF
__pycache__
.env
.git
.gitignore
*.pyc
venv/
.vscode/
.idea/
node_modules/
build/
dist/
*.egg-info/
.pytest_cache/
EOF

# Build Docker image
echo "🐳 Building Docker image..."
gcloud builds submit \
    --tag gcr.io/$PROJECT_ID/$SERVICE_NAME \
    --source backend

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars="ENVIRONMENT=production,DEBUG=false" \
    --memory 2Gi \
    --cpu 2 \
    --timeout 3600 \
    --max-instances 100

# Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format='value(status.url)')

echo ""
echo "✅ Deployment Complete!"
echo "======================="
echo "Service URL: $SERVICE_URL"
echo "API Docs: $SERVICE_URL/docs"
echo ""
echo "Next steps:"
echo "1. Update your frontend API_BASE_URL to: $SERVICE_URL/api"
echo "2. Configure Cloud Storage for file uploads (optional)"
echo "3. Set up monitoring and logging"
