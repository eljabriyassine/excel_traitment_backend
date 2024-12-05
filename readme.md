
# Deploying a Flask App on a Local Network with Gunicorn & NGINX

## Introduction

This guide explains how to deploy a Flask web application on your local network using **Gunicorn** and **NGINX**. The deployment allows other devices on the same network to access your app.

---

## Requirements

- Python 3.x
- Flask
- Gunicorn
- NGINX (optional for reverse proxy)
- A local Wi-Fi or Ethernet network

---

## Setup Instructions

### 1. Install Required Packages

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip nginx
```

### 2. Set Up Your Flask Application

#### Clone Your Project
```bash
git clone clone https://github.com/eljabriyassine/excel_traitment_backend
cd excel_traitment_backend
```

#### Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

If `Gunicorn` is not in your requirements:
```bash
pip install gunicorn
```

---

### 3. Run Flask with Gunicorn

Run Gunicorn to serve your Flask app:
```bash
gunicorn --workers 3 --bind 0.0.0.0:5000 main:app
```

---

### 4. Optional: Configure NGINX as a Reverse Proxy

#### Install NGINX
```bash
sudo apt install nginx
```

#### Create NGINX Configuration
```bash
sudo nano /etc/nginx/sites-available/flask_app
```

Add the following content:
```nginx
server {
    listen 80;
    server_name 192.168.11.116;  # Replace with your machine’s private IP
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Enable Configuration & Restart NGINX
```bash
sudo ln -s /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

---

### 5. Firewall Settings

Ensure port `80` (for NGINX) or `5000` (for Flask/Gunicorn) is open:
```bash
sudo ufw allow 80/tcp
sudo ufw allow 5000/tcp
```

---

### 6. Access the App

Get your server’s IP address:
```bash
ip a
```

Access the app in a browser:
```
http://<server-ip>
```

---

### Exposing to the Public Internet (Optional)

1. **Port Forwarding** on your router.
2. **Use a Static IP** or dynamic DNS (DDNS).
3. **Enable HTTPS** for secure communication.

---

## Conclusion

You’ve successfully deployed your Flask app on your local network. Using NGINX enhances performance and scalability for production environments.

---

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Gunicorn Documentation](https://gunicorn.org/)
- [NGINX Documentation](https://nginx.org/)