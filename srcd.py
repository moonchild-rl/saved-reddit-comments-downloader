import praw
import pandas as pd
import os
from urllib.parse import urlparse
import re
import argparse

# Step 0: Initialize Reddit API
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="YOUR_APP_NAME",
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)

# Step 1: Set up argument parsing
parser = argparse.ArgumentParser(description="Download saved Reddit comments")
parser.add_argument(
    "--file-scheme",
    default="{TITLE}_{POSTID}_{COMMENTID}",
    help="Set the file naming scheme using placeholders {TITLE}, {POSTID}, {COMMENTID}, and {SUBREDDIT}.",
)
args = parser.parse_args()

# Step 2: Load the CSV file
csv_file = "saved_comments.csv"  # Replace with your CSV file path
output_dir = "saved_comments"  # Directory to save comments in
os.makedirs(output_dir, exist_ok=True)

# Read the CSV file
df = pd.read_csv(csv_file)
comment_ids = df["id"]
permalinks = df["permalink"]

# Step 3: Fetch and Save Comments
for permalink, comment_id in zip(permalinks, comment_ids):
    try:
        # Parse the URL, split the path and remove empty parts
        parsed_url = urlparse(permalink)
        path_parts = [part for part in parsed_url.path.split("/") if part]

        # Extract subreddit, post ID and title
        subreddit = path_parts[1]  # After '/r/'
        post_id = path_parts[3]
        title = path_parts[4]

        # Clean the title to ensure it's safe for file naming
        title = re.sub(r"[^\w\s-]", "", title)

        # Build the directory path for the subreddit
        subreddit_dir = os.path.join(output_dir, subreddit)
        os.makedirs(subreddit_dir, exist_ok=True)

        # Fetch the comment using PRAW
        comment = reddit.comment(id=comment_id)

        # Skip saving if the comment content is [removed] or [deleted]
        if comment.body.strip().lower() in ["[removed]", "[deleted]"]:
            print(f"Comment {comment_id} is {comment.body}: skipping.")
            continue

        # Step 5: Use the file-scheme argument to create the file name
        file_scheme = args.file_scheme
        file_name = (
            file_scheme.format(
                TITLE=title, POSTID=post_id, COMMENTID=comment_id, SUBREDDIT=subreddit
            )
            + ".txt"
        )

        # Build the file path
        file_path = os.path.join(subreddit_dir, file_name)

        # Save the comment body to the file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(comment.body)

        # Print saved file without extension
        file_base, _ = os.path.splitext(file_name)
        print(f"Saved {file_base} to: {subreddit}")

    except Exception as e:
        # print Error and Link if comment could not be saved
        print(f"Error processing {permalink}: {e}")
