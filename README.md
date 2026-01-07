# CPU Monitor

A simple web app that displays AWS EC2 instance CPU usage over time using Flask and Chart.js.

## Requirements

- Python 3.x
- AWS account with EC2 instances
- AWS credentials with EC2 and CloudWatch read permissions

## Setup

1. Clone the repo:
2. Install dependencies:
```
pip install flask boto3 python-dotenv
```
3. Create a `.env` file in the project folder:
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=your_region
DEFAULT_IP=
```
4. Run the app:
```
python app.py
```
5. Open http://127.0.0.1:5000 in your browser.

6. Enjoy :)

