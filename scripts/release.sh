#!/bin/bash
# Release Script - Automatically bump version and push tag

echo "========================================"
echo "Release Script"
echo "========================================"
echo ""

# Get latest tag
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)

if [ -z "$LATEST_TAG" ]; then
    LATEST_TAG="v0.0.0"
    echo "[INFO] No existing tags found, starting from v0.0.0"
else
    echo "[INFO] Current version: $LATEST_TAG"
fi

# Parse version numbers (remove 'v' prefix)
VERSION=${LATEST_TAG#v}
IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION"

# Calculate next versions
NEXT_PATCH=$((PATCH + 1))
NEXT_MINOR=$((MINOR + 1))
NEXT_MAJOR=$((MAJOR + 1))

PATCH_VERSION="v${MAJOR}.${MINOR}.${NEXT_PATCH}"
MINOR_VERSION="v${MAJOR}.${NEXT_MINOR}.0"
MAJOR_VERSION="v${NEXT_MAJOR}.0.0"

echo ""
echo "Select version bump type:"
echo "  [1] Patch : $LATEST_TAG -> $PATCH_VERSION (bug fixes)"
echo "  [2] Minor : $LATEST_TAG -> $MINOR_VERSION (new features)"
echo "  [3] Major : $LATEST_TAG -> $MAJOR_VERSION (breaking changes)"
echo "  [4] Custom version"
echo "  [5] Cancel"
echo ""

read -p "Enter choice (1-5): " CHOICE

case $CHOICE in
    1)
        NEW_VERSION=$PATCH_VERSION
        ;;
    2)
        NEW_VERSION=$MINOR_VERSION
        ;;
    3)
        NEW_VERSION=$MAJOR_VERSION
        ;;
    4)
        read -p "Enter custom version (e.g., v1.2.3): " NEW_VERSION
        ;;
    *)
        echo "[INFO] Release cancelled"
        exit 0
        ;;
esac

echo ""
echo "[INFO] New version: $NEW_VERSION"
echo ""

# Confirm
read -p "Confirm release $NEW_VERSION? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "[INFO] Release cancelled"
    exit 0
fi

echo ""
echo "[INFO] Creating tag $NEW_VERSION..."
git tag "$NEW_VERSION"
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create tag"
    exit 1
fi

echo "[INFO] Pushing tag to origin..."
git push origin "$NEW_VERSION"
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to push tag"
    git tag -d "$NEW_VERSION"
    exit 1
fi

echo ""
echo "========================================"
echo "[OK] Release $NEW_VERSION created!"
echo "========================================"
echo ""
echo "GitHub Actions will now build and publish the release."
echo "Check: https://github.com/911218sky/kiro-pro-free/actions"
echo ""
