#!/bin/bash

# Define directories for your repositories
REPOS=(
    "$HOME/no-internet/opencve-kb"
    "$HOME/no-internet/opencve-nvd"
    "$HOME/no-internet/opencve-redhat"
)

# Define the base directory where patches are stored
PATCH_BASE_DIR="$HOME/transfers_dir"

# Function to apply patches and remove them
apply_patches() {
    REPO_DIR="$1"
    REPO_NAME=$(basename "$REPO_DIR")
    PATCH_DIR="$PATCH_BASE_DIR/$REPO_NAME"

    if [ ! -d "$REPO_DIR" ]; then
        echo "Repository directory $REPO_DIR does not exist. Skipping."
        return
    fi

    if [ ! -d "$PATCH_DIR" ]; then
        echo "Patch directory $PATCH_DIR does not exist. Skipping."
        return
    fi

    cd "$REPO_DIR" || return

    # Find all patch files in the patch directory and sort them numerically
    find "$PATCH_DIR" -name "*.patch" -print0 | sort -z -n | while IFS= read -r -d $'\0' PATCH_FILE; do
        echo "Applying patch: $PATCH_FILE to $REPO_DIR"
        
        # Apply the patch file
        git am < "$PATCH_FILE"
        if [ $? -eq 0 ]; then
            echo "Patch applied successfully."
            rm "$PATCH_FILE"
            echo "Deleted patch file: $PATCH_FILE"
        else
            echo "Failed to apply patch. Aborting."
            git am --abort
            exit 1
        fi
    done

    # Remove empty subdirectories
    find "$PATCH_DIR" -type d -empty -print0 | sort -z -r | while IFS= read -r -d $'\0' EMPTY_DIR; do
        echo "Removing empty directory: $EMPTY_DIR"
        rmdir "$EMPTY_DIR"
    done
}

# Iterate over each repository and apply patches
for REPO in "${REPOS[@]}"; do
    apply_patches "$REPO"
done

echo "Patch application process completed."