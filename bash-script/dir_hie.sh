#!/bin/bash

# Define directories for your repositories (internet connection required)
REPOS=(
    "$HOME/tets_1/patch_dir/opencve_repos/opencve-kb"
    "$HOME/tets_1/patch_dir/opencve_repos/opencve-nvd"
    "$HOME/tets_1/patch_dir/opencve_repos/opencve-redhat"
)

# Mapping repository folder names to GitHub URLs
declare -A REPO_URLS
REPO_URLS["opencve-kb"]="git@github.com:opencve/opencve-kb.git"
REPO_URLS["opencve-nvd"]="git@github.com:opencve/opencve-nvd.git"
REPO_URLS["opencve-redhat"]="git@github.com:opencve/opencve-redhat.git"

# Ensure the transfers directory exists
PATCH_BASE_DIR="$HOME/transfers_dir"
mkdir -p "$PATCH_BASE_DIR"

# Iterate over each repository
for REPO in "${REPOS[@]}"; do
    BASENAME=$(basename "$REPO")
    PATCH_DIR="$PATCH_BASE_DIR/$BASENAME"
    mkdir -p "$PATCH_DIR"

    if [ ! -d "$REPO" ]; then
        echo "Repository $REPO not found, attempting to clone..."
        mkdir -p "$(dirname "$REPO")"
        git clone "${REPO_URLS[$BASENAME]}" "$REPO"
        if [ $? -ne 0 ]; then
            echo "Failed to clone repository $BASENAME, skipping."
            continue
        fi
    fi

    echo "Processing repository: $REPO"
    cd "$REPO" || continue

    # Make sure we're on a branch
    CURRENT_BRANCH=$(git symbolic-ref --quiet --short HEAD)
    if [ -z "$CURRENT_BRANCH" ]; then
        echo "Not on any branch in $REPO, skipping."
        continue
    fi

    # Fetch remote changes
    git fetch --all

    # Check differences between local HEAD and remote branch
    REMOTE_BRANCH="origin/$CURRENT_BRANCH"
    if git rev-parse --verify --quiet "$REMOTE_BRANCH" >/dev/null; then
        LOCAL_SHA=$(git rev-parse --short HEAD)
        REMOTE_SHA=$(git rev-parse --short "$REMOTE_BRANCH")

        if [ "$LOCAL_SHA" != "$REMOTE_SHA" ]; then
            # Get UTC timestamp of the latest remote commit
            REMOTE_COMMIT_TIMESTAMP=$(git log -1 --format=%ct "$REMOTE_BRANCH")
            UTC_TIMESTAMP=$(date -u -d @"$REMOTE_COMMIT_TIMESTAMP" +'%Y%m%d%H%M%S')
            
            PREFIX_DIR="${UTC_TIMESTAMP}-${LOCAL_SHA}-${REMOTE_SHA}"
            PATCH_OUTPUT_DIR="$PATCH_DIR/$PREFIX_DIR"
            mkdir -p "$PATCH_OUTPUT_DIR"

            echo "Generating patch files for changes in $BASENAME..."
            git format-patch "$LOCAL_SHA..$REMOTE_SHA" -o "$PATCH_OUTPUT_DIR"

            echo "Patch file created: ${PATCH_OUTPUT_DIR}/${PREFIX}"

            echo "Pulling changes from remote branch $REMOTE_BRANCH."
            git pull origin "$CURRENT_BRANCH"
            if [ $? -eq 0 ]; then
                echo "Repository updated successfully in $REPO"
            else
                echo "Failed to update repository in $REPO"
            fi
        else
            echo "No changes between local and $REMOTE_BRANCH in $REPO"
        fi
    else
        echo "Remote branch $REMOTE_BRANCH does not exist in $REPO, skipping."
        continue
    fi

done

# Apply the patch file to the repository without internet connection
#git am < ~/transfers_dir/opencve-kb/path/to/patch/file.
#anything goes wrong run "git am --abort" and re-run above command.