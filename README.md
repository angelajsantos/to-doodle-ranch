# ⚔ to-doodle ranch

a gamified task tracker where every quest you create hatches a pet companion. complete quests to graduate your pets to the hall of fame!

## Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/training-grounds.git
cd training-grounds

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your MongoDB URI (get this from MongoDB Atlas)
export MONGODB_URI="mongodb+srv://<user>:<password>@<cluster>.mongodb.net/?appName=training-grounds"

# 5. Run
python app.py
# Visit http://localhost:5050
```

## AWS EC2 Deployment

### 1. Launch EC2 Instance
- Ubuntu 22.04, t2.micro (free tier)
- Security group: open port 5050 and 22

### 2. SSH into your instance and set up
```bash
ssh -i your-key.pem ubuntu@YOUR_EC2_IP

# Install Python & git
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git

# Clone your repo
git clone https://github.com/YOUR_USERNAME/training-grounds.git
cd training-grounds
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set up systemd service (auto-restart)
```bash
# Edit the service file with your real MongoDB URI first
sudo cp training-grounds.service /etc/systemd/system/
sudo nano /etc/systemd/system/training-grounds.service   # set MONGODB_URI

sudo systemctl daemon-reload
sudo systemctl enable training-grounds
sudo systemctl start training-grounds
sudo systemctl status training-grounds   # should show "active (running)"
```

### 4. Set up GitHub Actions CI/CD

Add these 3 secrets in your GitHub repo → Settings → Secrets → Actions:

| Secret       | Value                              |
|--------------|------------------------------------|
| `EC2_HOST`   | Your EC2 public IP or DNS          |
| `EC2_USER`   | `ubuntu`                           |
| `EC2_KEY`    | Contents of your `.pem` private key |

Now every push to `main` auto-deploys to EC2! 🚀

## Project Structure
```
training-grounds/
├── app.py                        # Flask backend
├── requirements.txt
├── training-grounds.service      # systemd service for EC2
├── templates/
│   └── index.html                # Frontend (HTML/CSS/JS)
└── .github/
    └── workflows/
        └── deploy.yml            # GitHub Actions CI/CD
```
