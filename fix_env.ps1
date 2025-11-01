# ============================================================
# Quick Fix Script for MathAI
# Save as: fix_env.ps1
# Run: .\fix_env.ps1
# ============================================================

Write-Host "🔧 MathAI Quick Fix Script" -ForegroundColor Cyan
Write-Host "=" * 60

# Get project root
$projectRoot = "D:\3. SELF STUDY\2. AI-ML\5. PROJECT\13. MathAI (AI Planets)"
Set-Location $projectRoot

# Step 1: Remove VITE_API_URL from root .env
Write-Host "`n1️⃣ Fixing root .env file..." -ForegroundColor Yellow

$envPath = Join-Path $projectRoot ".env"
if (Test-Path $envPath) {
    $envContent = Get-Content $envPath | Where-Object { $_ -notmatch "VITE_API_URL" }
    $envContent | Set-Content $envPath
    Write-Host "   ✅ Removed VITE_API_URL from root .env" -ForegroundColor Green
} else {
    Write-Host "   ⚠️ Root .env not found!" -ForegroundColor Red
}

# Step 2: Create frontend .env
Write-Host "`n2️⃣ Creating frontend .env..." -ForegroundColor Yellow

$frontendEnv = Join-Path $projectRoot "frontend\.env"
@"
# Frontend Environment Variables
VITE_API_URL=http://localhost:8000/api
"@ | Set-Content $frontendEnv

Write-Host "   ✅ Created frontend/.env" -ForegroundColor Green

# Step 3: Update config.py
Write-Host "`n3️⃣ Checking config.py..." -ForegroundColor Yellow

$configPath = Join-Path $projectRoot "backend\core\config.py"
if (Test-Path $configPath) {
    $configContent = Get-Content $configPath -Raw
    
    if ($configContent -match 'env_file = "\.\.env"') {
        Write-Host "   ✅ config.py already updated" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️ Please update config.py manually:" -ForegroundColor Yellow
        Write-Host "      - Add: env_file = '../.env'" -ForegroundColor Yellow
        Write-Host "      - Add: extra = 'ignore'" -ForegroundColor Yellow
    }
}

# Step 4: Verify API keys
Write-Host "`n4️⃣ Verifying API keys..." -ForegroundColor Yellow

$envContent = Get-Content $envPath
$geminiKey = $envContent | Where-Object { $_ -match "GEMINI_API_KEY=" }
$tavilyKey = $envContent | Where-Object { $_ -match "TAVILY_API_KEY=" }

if ($geminiKey -match "your-gemini-api-key") {
    Write-Host "   ⚠️ Please add your real GEMINI_API_KEY" -ForegroundColor Red
} else {
    Write-Host "   ✅ GEMINI_API_KEY set" -ForegroundColor Green
}

if ($tavilyKey -match "your-tavily-api-key") {
    Write-Host "   ⚠️ Please add your real TAVILY_API_KEY" -ForegroundColor Red
} else {
    Write-Host "   ✅ TAVILY_API_KEY set" -ForegroundColor Green
}

Write-Host "`n" + "=" * 60
Write-Host "✅ Fix completed!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Replace backend/core/config.py with the fixed version"
Write-Host "2. Run: cd backend && python main.py"
Write-Host "3. Run: cd frontend && npm run dev"
Write-Host "=" * 60