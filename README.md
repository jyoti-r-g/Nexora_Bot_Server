## 📋 Prerequisites

Before you start, make sure you have these installed:

- 🐍 **Python 3.10+** (check with `python --version`)
- 📦 **Poetry** (Python dependency manager)
- 🐳 **Docker** (for Redis and Supabase)
- 📘 **Node.js** (for Supabase CLI)


## 🔧 Step 1: Install System Dependencies



### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install poppler-utils tesseract-ocr libmagic1
```

> ⚠️ **Note**: These are required for document processing (PDFs, images, etc.)

## 📦 Step 2: Install Python Dependencies

Install all Python packages using Poetry:

```bash
poetry install
```

## 🗄️ Step 3: Setup Supabase

### Initialize Supabase

```bash
npx supabase init
```

### Start Supabase (Docker containers)

```bash
npx supabase start
```

This starts:

- 🐘 PostgreSQL database
- 🔐 Auth service
- 📡 API endpoints
- 🎨 Supabase Studio (UI)

### Run Database Migrations

```bash
npx supabase db reset
```

This runs all migration files and sets up your database schema.

## 🔑 Step 4: Configure Environment Variables

Copy the sample environment file and fill in your values:

```bash
cp .env.sample .env
```

Then edit `.env` with your specific configuration values.

> 💡 **Tip:** Get your Supabase credentials by running `npx supabase status` after starting Supabase locally.

> ⚠️ **Note:** Supabase has updated their naming. The old variable `service_role key` is now simply called `Secret Key`.  








