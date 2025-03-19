#!/bin/bash

# Prompt the user to enter the tag name
read -p "Enter the tag name (e.g., test0.1.0): " TAG_NAME

# Delete the local tag if it exists
if git tag | grep -q "^$TAG_NAME$"; then
  echo "Deleting local tag: $TAG_NAME"
  git tag -d "$TAG_NAME"
else
  echo "Local tag $TAG_NAME does not exist."
fi

# Delete the remote tag if it exists
if git ls-remote --tags origin | grep -q "refs/tags/$TAG_NAME"; then
  echo "Deleting remote tag: $TAG_NAME"
  git push origin --delete "$TAG_NAME"
else
  echo "Remote tag $TAG_NAME does not exist."
fi

# Recreate the tag
echo "Recreating tag: $TAG_NAME"
git tag -a "$TAG_NAME" -m "$TAG_NAME"

# Push the new tag to the remote
echo "Pushing tag: $TAG_NAME"
git push origin "$TAG_NAME"

echo "Tag $TAG_NAME has been reset and pushed successfully."


