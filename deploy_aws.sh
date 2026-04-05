#!/bin/bash

# ============================================================================
# DEPLOYMENT SCRIPT FOR AWS EC2
# ============================================================================

set -e

echo "🚀 AI Video Editor - AWS EC2 Deployment Script"
echo "=============================================="

# Update system
echo "📦 Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install dependencies
echo "📥 Installing dependencies..."
sudo apt install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    ffmpeg \
    git \
    nginx \
    supervisor \
    postgresql \
    postgresql-contrib

# Create app directory
echo "📁 Creating application directory..."
APP_DIR="/opt/ai-video-editor"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Clone repository
echo "📝 Setting up application..."
cd $APP_DIR
git clone YOUR_REPO_URL .

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
cd backend
python3.10 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup environment variables
echo "🔧 Configuring environment..."
cp .env.example .env
# Edit .env with proper values
nano .env

# Initialize database
echo "💾 Initializing database..."
python3 database.py

# Create systemd service for backend
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/ai-video-editor.service > /dev/null <<EOF
[Unit]
Description=AI Video Editor API
After=network.target

[Service]
Type=notify
User=$USER
WorkingDirectory=$APP_DIR/backend
Environment="PATH=$APP_DIR/backend/venv/bin"
ExecStart=$APP_DIR/backend/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app.main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
echo "🔄 Starting service..."
sudo systemctl daemon-reload
sudo systemctl enable ai-video-editor
sudo systemctl start ai-video-editor

# Setup Nginx reverse proxy
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/ai-video-editor > /dev/null <<EOF
server {
    listen 80;
    server_name _;
    
    client_max_body_size 500M;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_buffering off;
    }
    
    # API docs
    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
    }
    
    location /openapi.json {
        proxy_pass http://127.0.0.1:8000/openapi.json;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/ai-video-editor /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Setup SSL with Let's Encrypt (optional)
echo "🔐 Setting up SSL (optional)..."
echo "Install certbot: sudo apt install certbot python3-certbot-nginx"
echo "Then run: sudo certbot --nginx -d yourdomain.com"

# Create log rotation
echo "📊 Setting up log rotation..."
sudo tee /etc/logrotate.d/ai-video-editor > /dev/null <<EOF
$APP_DIR/backend/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0644 $USER $USER
    sharedscripts
    postrotate
        systemctl reload ai-video-editor > /dev/null 2>&1 || true
    endscript
}
EOF

# Verify installation
echo ""
echo "✅ Deployment Summary"
echo "===================="
echo "Application: $APP_DIR"
echo "Service: ai-video-editor (systemctl status ai-video-editor)"
echo "API: http://your-server-ip/docs"
echo "Logs: /var/log/syslog or journalctl -u ai-video-editor"
echo ""
echo "Next steps:"
echo "1. Update .env with your configuration"
echo "2. Set up domain name and SSL certificate"
echo "3. Configure database connection"
echo "4. Start receiving requests!"
