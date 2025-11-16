#!/usr/bin/env bash
set -e

if command -v gradle >/dev/null 2>&1; then
  echo "Gradle found. Generating wrapper..."
  gradle wrapper
  echo "Gradle wrapper generated. Commit the generated files (gradlew, gradlew.bat, gradle/wrapper/*)."
else
  echo "Gradle CLI not found. Install Gradle or open the project in Android Studio which can generate the wrapper for you."
  exit 1
fi
