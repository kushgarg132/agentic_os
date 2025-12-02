# Complete Setup Guide: API Keys & Secrets

This guide will walk you through obtaining all the required API keys, secrets, and credentials for your Agentic AI OS project.

---

## 📋 Overview

Your `.env` file needs the following:
1. **Google OAuth Credentials** (for accessing Gmail, Drive, Calendar, etc.)
2. **Google Gemini API Key** (for AI agents)
3. **Security Keys** (for encryption and JWT tokens)
4. **Database & Redis** (handled by Docker)

---

## 🔐 Step-by-Step Setup

### Step 1: Google OAuth Credentials (GOOGLE_CLIENT_ID & GOOGLE_CLIENT_SECRET)

These credentials allow your app to access Google services (Gmail, Drive, Calendar, Docs, Contacts) on behalf of users.

#### 1.1 Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Select a project"** → **"New Project"**
3. Enter project name: `Agentic AI OS` (or any name you prefer)
4. Click **"Create"**
5. Wait for the project to be created, then select it

#### 1.2 Enable Required APIs

1. In your project, go to **"APIs & Services"** → **"Library"**
2. Search for and enable the following APIs (click each, then click "Enable"):
   - **Gmail API**
   - **Google Drive API**
   - **Google Calendar API**
   - **Google Docs API**
   - **Google Contacts API** (People API)

#### 1.3 Configure OAuth Consent Screen

1. Go to **"APIs & Services"** → **"OAuth consent screen"**
2. Choose **"External"** (unless you have a Google Workspace account)
3. Click **"Create"**
4. Fill in the required fields:
   - **App name**: `Agentic AI OS`
   - **User support email**: Your email
   - **Developer contact email**: Your email
5. Click **"Save and Continue"**
6. **Scopes**: Click **"Add or Remove Scopes"** and add:
   - `https://www.googleapis.com/auth/gmail.readonly`
   - `https://www.googleapis.com/auth/gmail.send`
   - `https://www.googleapis.com/auth/drive.readonly`
   - `https://www.googleapis.com/auth/calendar`
   - `https://www.googleapis.com/auth/contacts.readonly`
   - Or simply search for "Gmail", "Drive", "Calendar", "Contacts" and select appropriate scopes
7. Click **"Save and Continue"**
8. **Test users**: Add your email address (required for testing)
9. Click **"Save and Continue"**

#### 1.4 Create OAuth Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. Choose **"Web application"**
4. Name it: `Agentic AI OS Web Client`
5. Under **"Authorized redirect URIs"**, click **"Add URI"** and add:
   ```
   http://localhost:8000/api/v1/auth/callback
   ```
6. Click **"Create"**
7. A popup will show your credentials:
   - **Client ID**: Copy this → This is your `GOOGLE_CLIENT_ID`
   - **Client Secret**: Copy this → This is your `GOOGLE_CLIENT_SECRET`
8. Click **"Download JSON"** and save it as `client_secrets.json` in your backend folder

> [!IMPORTANT]
> Keep these credentials secure! Never commit them to version control.

---

### Step 2: Google Gemini API Key (GOOGLE_API_KEY)

This is for the AI models that power your agents.

#### 2.1 Get Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Select **"Create API key in new project"** or choose an existing project
5. Copy the API key → This is your `GOOGLE_API_KEY`

> [!TIP]
> Gemini offers a generous free tier! Check the [pricing page](https://ai.google.dev/pricing) for limits.

---

### Step 3: Security Keys

#### 3.1 Generate SECRET_KEY (for JWT tokens)

This is used for signing JWT tokens for user authentication.

**Option A: Using Python**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Option B: Using OpenSSL**
```bash
openssl rand -base64 32
```

Copy the output → This is your `SECRET_KEY`

#### 3.2 Generate ENCRYPTION_KEY (for encrypting sensitive data)

This must be a 32-byte base64-encoded key for AES encryption.

**Using Python:**
```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Copy the output → This is your `ENCRYPTION_KEY`

---

### Step 4: Database & Redis Configuration

These are handled by Docker Compose, but you can customize them if needed.

#### Default Values (already in docker-compose.yml):
- **POSTGRES_SERVER**: `localhost` (or `db` when using Docker)
- **POSTGRES_USER**: `postgres`
- **POSTGRES_PASSWORD**: `password` (⚠️ Change this in production!)
- **POSTGRES_DB**: `agentic_os`
- **REDIS_HOST**: `redis` (when using Docker) or `localhost`
- **REDIS_PORT**: `6379`

> [!WARNING]
> Change the default database password in production!

---

### Step 5: Neo4j Configuration (for Knowledge Graph)

If you're using the default Docker setup, Neo4j credentials are:
- **NEO4J_URI**: `bolt://localhost:7687`
- **NEO4J_USER**: `neo4j`
- **NEO4J_PASSWORD**: `password` (⚠️ Change this!)

You can modify these in your `docker-compose.yml` file.

---

## 📝 Creating Your .env File

Now that you have all the credentials, create your `.env` file:

1. Copy the example file:
   ```bash
   cd backend
   cp .env.example .env
   ```

2. Edit `.env` with your favorite editor:
   ```bash
   nano .env
   # or
   vim .env
   # or
   code .env
   ```

3. Fill in all the values:

```bash
PROJECT_NAME="Agentic AI OS"

# Database (using Docker defaults)
DATABASE_URL=postgresql://postgres:password@db/agentic_os

# Redis (using Docker defaults)
REDIS_HOST=redis
REDIS_PORT=6379

# Security Keys (generate these!)
SECRET_KEY=your_generated_secret_key_here
ENCRYPTION_KEY=your_generated_encryption_key_here

# Google OAuth (from Step 1)
GOOGLE_CLIENT_ID=your_client_id_from_google_cloud.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret_from_google_cloud
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/callback

# Google Gemini API (from Step 2)
GOOGLE_API_KEY=your_gemini_api_key_here

# Neo4j (using Docker defaults)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
```

---

## 🚀 Installation & Running

### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Start Services with Docker

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database
- Redis
- Neo4j

### Run the Backend

```bash
cd backend
uvicorn main:app --reload
```

Your API will be available at: `http://localhost:8000`

---

## ✅ Verification Checklist

- [ ] Google Cloud Project created
- [ ] Gmail, Drive, Calendar, Docs, Contacts APIs enabled
- [ ] OAuth consent screen configured
- [ ] OAuth credentials created (Client ID & Secret)
- [ ] `client_secrets.json` downloaded
- [ ] Gemini API key obtained
- [ ] `SECRET_KEY` generated
- [ ] `ENCRYPTION_KEY` generated
- [ ] `.env` file created and filled
- [ ] Dependencies installed
- [ ] Docker services running
- [ ] Backend server starts without errors

---

## 🔍 Troubleshooting

### "Invalid client" error
- Check that `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` match your OAuth credentials
- Verify the redirect URI in Google Cloud Console matches your `.env` file

### "API not enabled" error
- Go back to Google Cloud Console and enable the required APIs

### Gemini API errors
- Check your API key is correct
- Verify you haven't exceeded the free tier limits
- Ensure you're using a supported region

### Database connection errors
- Make sure Docker containers are running: `docker-compose ps`
- Check the database URL format is correct

---

## 📚 Additional Resources

- [Google Cloud Console](https://console.cloud.google.com/)
- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [OAuth 2.0 Guide](https://developers.google.com/identity/protocols/oauth2)

---

## 🔒 Security Best Practices

1. **Never commit `.env` to version control**
   - Add `.env` to your `.gitignore`
2. **Use strong passwords** for production databases
3. **Rotate keys regularly** in production
4. **Use environment-specific configs** (dev, staging, prod)
5. **Enable 2FA** on your Google account
6. **Monitor API usage** to detect unusual activity

---

Good luck with your Agentic AI OS! 🎉
