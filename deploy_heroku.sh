#!/bin/bash

# ============================================================================
# DEPLOYMENT SCRIPT FOR HEROKU
# ============================================================================

APP_NAME="your-app-name"

echo "🚀 Deploying to Heroku"
echo "======================="

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Install it from https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Create Procfile
echo "📝 Creating Procfile..."
cat > Procfile <<EOF
web: cd backend && gunicorn -w 4 -b 0.0.0.0:\$PORT app.main:app
EOF

# Create runtime.txt
echo "🐍 Creating runtime.txt..."
echo "python-3.10.0" > runtime.txt

# Login to Heroku
echo "🔐 Logging in to Heroku..."
heroku login -i

# Create app if it doesn't exist
echo "📦 Creating Heroku app..."
heroku create $APP_NAME --region us

# Set environment variables
echo "🔧 Setting environment variables..."
heroku config:set -a $APP_NAME \
    ENVIRONMENT=production \
    DEBUG=false \
    GOOGLE_VISION_API_KEY=your_key \
    REMOVEBG_API_KEY=your_key

# Deploy
echo "🚀 Deploying..."
git push heroku main

# Open app
echo ""
echo "✅ Deployment Complete!"
echo "======================="
echo "App URL: https://$APP_NAME.herokuapp.com"
echo "API Docs: https://$APP_NAME.herokuapp.com/docs"
echo ""
echo "View logs: heroku logs -a $APP_NAME -t"
