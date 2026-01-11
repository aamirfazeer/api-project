# Cloud-Native API with Automated CI/CD Pipeline

A production-ready microservice demonstrating modern DevOps practices including containerization, cloud deployment, and automated CI/CD workflows.

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

## 🚀 Features

- **RESTful API** built with FastAPI
- **JWT Authentication** with secure password hashing
- **User Registration & Login** endpoints
- **Docker containerization** for consistent deployment
- **AWS EC2 deployment** on Ubuntu Linux
- **Automated CI/CD pipeline** using GitHub Actions
- **Zero-downtime deployments** on every git push
- **Production-ready** with health checks and logging

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Backend** | Python 3.10, FastAPI |
| **Authentication** | JWT (JSON Web Tokens), OAuth2 |
| **Security** | bcrypt, python-jose |
| **Containerization** | Docker |
| **Cloud Platform** | AWS EC2 (Ubuntu 22.04) |
| **CI/CD** | GitHub Actions |
| **Version Control** | Git |

## 📋 Architecture

```
Developer Push → GitHub → GitHub Actions → Build Docker Image → Deploy to EC2 → Live API
```

## 🏗️ Project Structure

```
API_Project/
├── main.py                 # FastAPI application with authentication
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── .github/
│   └── workflows/
│       └── deploy.yml     # CI/CD pipeline
├── .gitignore            # Git ignore rules
├── .dockerignore         # Docker ignore rules
└── README.md             # Project documentation
```

## 🔧 Local Development

### Prerequisites

- Python 3.10+
- Docker Desktop (optional, for containerized development)

### Setup

```bash
# Clone repository
git clone https://github.com/aamirfazeer/API_Project.git
cd API_Project

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn main:app --reload
```

### Docker Development

```bash
# Build Docker image
docker build -t api-project .

# Run container
docker run -p 8000:8000 api-project
```

Access the API at: **http://localhost:8000**

Interactive API documentation: **http://localhost:8000/docs**

## 🌐 API Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/` | GET | Health check and status | ❌ |
| `/info` | GET | API information | ❌ |
| `/docs` | GET | Interactive API documentation (Swagger UI) | ❌ |
| `/register` | POST | Register a new user | ❌ |
| `/login` | POST | Login and get JWT token | ❌ |
| `/me` | GET | Get current user information | ✅ |

### Example API Usage

#### Register a New User
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "full_name": "John Doe"
  }'
```

#### Login
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=securepassword123"
```

#### Access Protected Endpoint
```bash
curl -X GET "http://localhost:8000/me" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🚀 Deployment

### Automated Deployment (CI/CD)

Every push to `main` branch triggers:

1. ✅ GitHub Actions workflow
2. ✅ Docker image build
3. ✅ Deployment to AWS EC2
4. ✅ Container restart with zero downtime

### Manual Deployment

```bash
# SSH to EC2
ssh -i key.pem ubuntu@<EC2_IP>

# Navigate to project directory
cd ~/api-project

# Pull latest code
git pull origin main

# Rebuild and restart
docker build -t api_project .
docker stop api_project-container || true
docker rm api_project-container || true
docker run -d -p 8000:8000 --name api_project-container --restart unless-stopped api_project
```

## 🔐 Environment Setup

### Required GitHub Secrets

Configure these secrets in your GitHub repository settings:

- `EC2_HOST` - EC2 public IP address
- `EC2_SSH_KEY` - Private SSH key for EC2 access

### EC2 Security Group Configuration

Ensure your EC2 security group allows inbound traffic on:
- **Port 8000** (HTTP) - for API access
- **Port 22** (SSH) - for deployment

## 📊 Key Learnings

- ✅ Containerization best practices with Docker
- ✅ Linux server administration (Ubuntu)
- ✅ AWS EC2 instance management and security groups
- ✅ Automated deployment pipelines with GitHub Actions
- ✅ REST API development with FastAPI
- ✅ JWT authentication and OAuth2 implementation
- ✅ Password hashing and security best practices
- ✅ Infrastructure as Code concepts

## 🎯 Future Enhancements

- [ ] Add automated testing in CI/CD pipeline
- [ ] Implement HTTPS with SSL certificates
- [ ] Add monitoring and logging (Prometheus/Grafana)
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Load balancing for multiple instances
- [ ] Kubernetes deployment
- [ ] Rate limiting and API throttling
- [ ] Email verification for user registration
- [ ] Password reset functionality
- [ ] Role-based access control (RBAC)

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Aamir Fazeer**

- GitHub: [@aamirfazeer](https://github.com/aamirfazeer)
- LinkedIn: [Aamir Fazeer](https://linkedin.com/in/aamirfazeer)

---

⭐ If you find this project helpful, please give it a star!
