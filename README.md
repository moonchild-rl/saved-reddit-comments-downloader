# **Saved Reddit Comments Downloader**
This is a script that can download all your saved comments from reddit. It can be used to give each file a unique name and organize them into folders. The naming scheme and folder structure is similar to that of the [Bulk Downloader for Reddit (BDFR)](https://github.com/Serene-Arc/bulk-downloader-for-reddit).

## **Installation**

### **Step 1: Request your data from Reddit**
1. Request your account data using Reddit's [data request form](https://www.reddit.com/settings/data-request).
2. Once you receive the archive, locate the file named `saved_comments.csv`—this file is required for the script.

### **Step 2: Set Up Reddit API Access**
   
1. Go to [Reddit's Developer Portal](https://www.reddit.com/prefs/apps/).
2. Create a new application:
    - Choose **"script"** as the app type.
    - Fill in the details, such as a name and redirect URL (use http://localhost).
3. Note down the **client ID**, **secret**, and your **username**.
     - Tip: The Client ID is the (random) string under the application name (where it says *personal use script*)
     - Tip Tip: Make sure the *secret* has no leading white space (because that happened to me and is FREAKING annoying)

### **Step 3: Install Required Libraries**
Use [pip](https://pypi.org/project/pip/) to install praw and pandas
```bash
pip install praw pandas
```

### **Step 4: Download the Script**

Above you will find the python script called `srcd.py`.
Download that file or clone this repository.

### **Step 5: Configure the Script**
1. Open `srcd.py` in your preferred editor.
2. Replace placeholders (e.g., YOUR_CLIENT_ID, YOUR_CLIENT_SECRET) with the credentials from Step 2.
3. Move the `saved_comments.csv` file into the same folder as `srcd.py`.

## **Usage**

### **Run the Script**
   
```bash
python3 srcd.py
```

### **Options**
Add the following option in order to change download behavior:
  - `--file-scheme`
    - This flag lets you set a custom naming scheme for files
    - Default is `{TITLE}_{POSTID}_{COMMENTID}`
    - Possible Placeholders are `{TITLE}`, `{POSTID}`, `{COMMENTID}`, and `{SUBREDDIT}`
   
**Example**: To save files using only the comment ID:
```bash
python3 srcd.py --file-scheme {COMMENTID}
```

### **Output**
- Files are stored in folders named after their respective `{SUBREDDIT}`(e.g. `r/funny`).
- This mirrors the default behavior of [BDFR](https://github.com/Serene-Arc/bulk-downloader-for-reddit#downloader-options).

---

## Thank you
If you read this far, thank you for taking the time.
I am very much open to discussion about the topic. If you have any suggestions, opinions or constructive criticism please let me know!
