# 🎤 Text-to-Speech AWS App

A serverless **Text-to-Speech** application using **AWS Lambda**, **Polly**, **S3**, and **Terraform**. Convert text into audio (MP3) files that are stored in S3 and can be accessed via a pre-signed URL.

🔗 Live Site: **https://texttospeach.khalidhashim.com/**

---

## 🚀 Features

- 📝 Converts any text input to MP3 audio using **AWS Polly**.
- 💾 Stores generated audio files in **Amazon S3**.
- 🔑 Returns **pre-signed URLs** for secure, temporary access to audio files.
- ⚙️ Fully automated deployment using **Terraform**.
- ☁️ Serverless architecture with **AWS Lambda** for scalability.
- 🌐 CORS-enabled for integration with web frontends.

---

## 🏗 Architecture

The Text-to-Speech application leverages a **fully serverless architecture** on AWS to deliver scalable, cost-efficient, and secure audio generation.  

### **Core Components**

1. **🟢 AWS Lambda**
   - Handles incoming requests from the API.
   - Invokes **AWS Polly** to convert text to speech.
   - Generates and uploads MP3 files to **Amazon S3**.
   - Returns a **pre-signed URL** for temporary access to the audio file.
   - Stateless design ensures **high scalability** and **low latency**.  

2. **🎙️ Amazon Polly**
   - Converts input text into natural-sounding speech.
   - Supports multiple languages and voices.
   - Integrated seamlessly with Lambda for real-time TTS.  

3. **🪣 Amazon S3**
   - Stores generated MP3 files securely.
   - Provides durable and cost-efficient storage.
   - Pre-signed URLs enable **secure, temporary access** without exposing buckets publicly.  

4. **🌉 API Gateway**
   - Serves as the **entry point** for web or mobile clients.
   - Routes requests to the Lambda function.
   - Configured with **CORS** to allow integration with web frontends.  

5. **🛠️ Terraform**
   - **Infrastructure-as-Code (IaC)** for automated deployment.
   - Defines Lambda, S3 buckets, IAM roles, and API Gateway in reusable, version-controlled code.
   - Ensures **repeatable deployments**, **easy updates**, and **environment isolation**.  

### **🔄 Workflow**

1. 🧑‍💻 User sends text input via **API Gateway** endpoint.
2. 🚪 API Gateway triggers the **Lambda function**.
3. 🎙️ Lambda calls **Polly** to generate speech audio.
4. 💾 Audio is uploaded to **S3**.
5. 🔑 Lambda generates a **pre-signed URL** and returns it to the user.
6. 🎧 User accesses the MP3 via the temporary URL.

---

### **💡 Key Skills Demonstrated**
- **Serverless development:** AWS Lambda, API Gateway, Polly.
- **Cloud storage & security:** S3 with pre-signed URLs, IAM roles.
- **Infrastructure as Code:** Terraform for automated, maintainable deployments.
- **Scalable API design:** CORS-enabled endpoints, stateless architecture.
- **Cloud-native architecture:** Fully serverless, cost-efficient, and highly available.
