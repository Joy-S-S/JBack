#!/bin/bash

# SIMPLE INSTRUCTIONS TO PUSH WRAPPER FILES TO GITHUB
# Run this from your local machine in the JBack directory

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        JBack - Push Wrapper Files to GitHub                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

cd /workspaces/JBack || exit 1

# Step 1
echo "[1/4] Configuring git..."
git config user.email "build@example.com"
git config user.name "Build System"

# Step 2
echo "[2/4] Adding wrapper files..."
git add gradlew gradlew.bat gradle/wrapper/gradle-wrapper.properties
git status

# Step 3
echo "[3/4] Creating commit..."
git commit -m "Add Gradle wrapper (gradlew, gradlew.bat) for easy CLI builds"

# Step 4
echo "[4/4] Pushing to GitHub..."
git push origin main

echo ""
echo "✓ Done! Wrapper files are now on GitHub!"
echo ""
echo "Verify at: https://github.com/Joy-S-S/JBack"
echo ""
