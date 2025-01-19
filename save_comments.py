import praw
import pandas as pd
import os
from urllib.parse import urlparse
import re
import argparse
import json
import requests

# Step 0: Set up argument parsing
parser = argparse.ArgumentParser(description="Download saved Reddit comments")
parser.add_argument(
    "--config",
    default="config.json",
    help="Path to the JSON configuration file containing Reddit API credentials.",
)
parser.add_argument(
    "--file-scheme",
    default="{TITLE}_{POSTID}_{COMMENTID}",
    help="Set the file naming scheme using placeholders {TITLE}, {POSTID}, {COMMENTID}, and {SUBREDDIT}.",
)
parser.add_argument(
    "--input",
    default="saved_comments.csv",
    help="Path to the input CSV file containing saved comments.",
)
parser.add_argument(
    "--output",
    default="saved_comments",
    help="Directory to save the downloaded comments in.",
)
parser.add_argument(
    "--unsave",
    action="store_true",
    help="If set, unsaves the downloaded comments from Reddit.",
)
args = parser.parse_args()

# Step 1: Load configuration file
try:
    with open(args.config, "r") as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    print(f"Configuration file not found: {args.config}")
    exit(1)
except json.JSONDecodeError:
    print(f"Invalid JSON format in configuration file: {args.config}")
    exit(1)

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=config.get("client_id"),
    client_secret=config.get("client_secret"),
    user_agent=config.get("user_agent"),
    username=config.get("username"),
    password=config.get("password"),
)

# Step 2: Load the CSV file
csv_file = args.input
output_dir = args.output
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

        # Step 6: Check for Image/GIF URLs in the comment body and download them too
        image_urls = re.findall(
            r"(?:https:\/\/preview\.redd\.it\/[^\s]+(?:\.jpg|\.jpeg|\.png|\.gif)).*",
            comment.body,
        )
        for img_url in image_urls:
            try:
                # Name the image or gif
                img_name = os.path.basename(urlparse(img_url).path)
                img_path = os.path.join(subreddit_dir, img_name)

                # Download and save the image
                img_data = requests.get(img_url).content
                with open(img_path, "wb") as img_file:
                    img_file.write(img_data)

                print(f"Downloaded image from: {img_url}")

            except Exception as img_error:
                print(f"Error downloading image {img_url}: {img_error}")

        # Step 7: Unsave the comment if the --unsave flag is set
        if args.unsave:
            comment.unsave()
            print(f"Unsaved comment {comment_id}.")

    except Exception as e:
        # print Error and Link if comment could not be saved
        print(f"Error processing {permalink}: {e}")
