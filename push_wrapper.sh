#!/bin/bash
set -e

echo "========================================"
echo "JBack - Git Push Script"
echo "========================================"

cd /workspaces/JBack

# Configure git user for commits
echo "[1/5] Configuring git..."
git config user.email "build@jback.example.com" || true
git config user.name "JBack Build System" || true

# Add wrapper files
echo "[2/5] Adding wrapper files..."
echo "      - gradlew"
git add gradlew || echo "Failed to add gradlew"
echo "      - gradlew.bat"
git add gradlew.bat || echo "Failed to add gradlew.bat"
echo "      - gradle/wrapper/gradle-wrapper.properties"
git add gradle/wrapper/gradle-wrapper.properties || echo "Failed to add properties"

# Show staged changes
echo ""
echo "[3/5] Verifying staged changes..."
git diff --cached --stat || echo "No changes staged"

# Commit
echo ""
echo "[4/5] Creating commit..."
git commit -m "Add Gradle wrapper files (gradlew, gradlew.bat)

Features:
- Enable CLI builds without requiring Gradle pre-installation
- Wrapper automatically downloads Gradle 8.2.0 on first build
- Includes both Unix (gradlew) and Windows (gradlew.bat) scripts
- Configured for Gradle 8.2.0 in gradle-wrapper.properties

This allows users to clone and build with:
  git clone https://github.com/Joy-S-S/JBack.git
  cd JBack
  chmod +x ./gradlew
  ./gradlew assembleDebug --no-daemon" --allow-empty || echo "Commit failed or nothing to commit"

# Push to GitHub
echo ""
echo "[5/5] Pushing to GitHub..."
git push origin main -v

echo ""
echo "========================================"
echo "✓ Push complete!"
echo "========================================"
echo ""
echo "Verify on GitHub:"
echo "  https://github.com/Joy-S-S/JBack/tree/main"
echo ""
