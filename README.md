### Text-to-Speech Web App

This project demonstrates a full-stack web application that converts text into audio using AWS services. It was built to **learn how to integrate multiple AWS services into a working solution**.

**Live Site:** [texttospeech.khalidhashim.com](https://texttospeech.khalidhashim.com)

**Implementation Highlights:**

1. **AWS Lambda:** Created a Lambda function to process text-to-speech conversion.  
2. **API Gateway:** Deployed the API and enabled **CORS** so the frontend could securely access it from any domain.  
3. **S3 Storage:** Stored generated audio files in an **S3 bucket** with public access and versioning enabled.  
4. **Frontend Hosting:** Hosted the HTML frontend using **AWS Amplify** for secure and reliable delivery.  

**Challenges & Learnings:**  
- Resolved permission issues and 404 errors by correctly configuring **CORS** for both the API and S3 bucket.  
- Fixed frontend formatting issues when receiving audio URLs from the API.  
- Gained hands-on experience connecting **Lambda, API Gateway, S3, and Amplify** into a functional solution.  

This project helped me understand **end-to-end AWS service integration**, providing a real-world technical solution while improving my cloud skills.
