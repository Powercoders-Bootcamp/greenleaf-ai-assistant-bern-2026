# 🚀 Project Setup (Docker)

This project runs entirely using **Docker + Docker Compose** (frontend, backend, PostgreSQL).

⚠️ **Important:**
The first setup **may take several minutes** (downloading images, building containers).
This is expected — it is **NOT a MAINER installation :)**.

---

# 📦 1. Install Docker

## Ubuntu

```bash
sudo apt update
sudo apt install docker.io docker-compose -y
```

Start Docker:

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

Add your user to docker group:

```bash
sudo usermod -aG docker $USER
```

Then re-login or run:

```bash
newgrp docker
```

---

## macOS / Windows

Install **Docker Desktop**:

https://www.docker.com/products/docker-desktop/

After installation, verify:

```bash
docker --version
docker-compose --version
```

---

# 📁 2. Clone Repository

```bash
git clone <your-repo-url>
cd <project-folder>
```

---

# ⚙️ 3. Environment Variables

Create the file:

```bash
src/backend/.env
```

👉 The `.env` file will be shared separately (Slack).
Just place it in the correct location.

---

# 🐳 4. Build & Run

## First run (this may take time)

```bash
docker-compose up --build
```

---

## Run in background

```bash
docker-compose up -d
```

---

## Stop containers

```bash
docker-compose down
```

---

# 🌐 5. Access Services

* Frontend → http://localhost:5173
* Backend → http://localhost:8000
* API Docs → http://localhost:8000/docs

---

# 🧠 Notes

* Everything runs inside Docker — **no need for Python venv or Node setup locally**
* No need to install dependencies manually
* Backend auto-reloads (dev mode)
* Frontend uses Vite with hot reload

---

# 📌 Useful Commands

```bash
docker-compose up --build   # build + run
docker-compose down         # stop
docker ps                   # list containers
docker logs app_backend     # backend logs
```

---

# ✅ Done

Open:

👉 http://localhost:5173

---
