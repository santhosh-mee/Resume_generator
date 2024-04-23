from flask import Flask, render_template, request, Response
from jinja2 import Template
import boto3

app = Flask(__name__)

AWS_ACCESS_KEY_ID = 'YOUR ACCESS KEY'
AWS_SECRET_ACCESS_KEY = 'YOUR SECRET KEY'
AWS_REGION = 'us-east-1'
S3_BUCKET = 'bucketbabu2003'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    # Retrieve form data
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    linkedin = request.form.get('linkedin', '')  # LinkedIn profile link (optional)
    github = request.form.get('github', '')  # GitHub profile link (optional)
    education = request.form['education']
    experience = request.form['experience']
    projects = request.form.get('projects', '')  # Projects section (optional)
    resume_text = f"\nName: {name}\nEmail: {email}\nPhone: {phone}\n"
    if linkedin:
        resume_text += f"LinkedIn: {linkedin}\n"
    if github:
        resume_text += f"GitHub: {github}\n"
    resume_text += f"\nEducation:\n{education}\n\nExperience:\n{experience}\n"
    if projects:
        resume_text += f"\nProjects:\n{projects}"
    
    # Upload resume text to S3 bucket
    s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION)
    bucket_name = S3_BUCKET
    key = 'resume.txt'
    s3.put_object(Bucket=bucket_name, Key=key, Body=resume_text)
    
    return render_template('resume.html', resume_text=resume_text)

@app.route('/download_resume')
def download_resume():
    # Retrieve resume text from S3 bucket
    s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
) 
    key = 'resume.txt'
    response = s3.get_object(Bucket=S3_BUCKET, Key=key)
    resume_text = response['Body'].read().decode('utf-8')
    
    # Return resume text as a downloadable file
    return Response(resume_text, mimetype='text/plain', headers={'Content-Disposition': 'attachment; filename=resume.txt'})

if __name__ == '__main__':
    app.run(debug=True)
