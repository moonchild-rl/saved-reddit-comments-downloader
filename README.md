# **Saved Reddit Comments Downloader**
This is a script that downloads all your saved comments from reddit. It can be used to give each file a name and organize them into folders. The naming and folder scheme is similar to that of the [Bulk Downloader for Reddit (BDFR)](https://github.com/Serene-Arc/bulk-downloader-for-reddit). 

The script is also able to automatically download any images and GIFs found in the comments!

## **Installation**

### **Step 1: Request your data from Reddit**
1. Request your account data using Reddit's [data request form](https://www.reddit.com/settings/data-request).
2. Once you receive the archive, locate the file named `saved_comments.csv`—this file is required for the script.

### **Step 2: Set Up Reddit API Access**
   
1. Go to [Reddit's Developer Portal](https://www.reddit.com/prefs/apps/).
2. Create a new application:
    - Choose **"script"** as the app type.
    - Fill in the details. Make sure to give it a name and redirect URI (use http://localhost).
3. Note down the **Credentials**.
     - **client_id** is the (seemingly random) string under *personal use script*
     - **client_secret** is the *secret*
     - **user_agent** is the name you gave the app
     - **username** is your reddit username
     - **password** is your reddit password
     - Tip: Make sure none of the credentials contain any white spaces (otherwise it won't work)

### **Step 3: Install Required Libraries**
Use [pip](https://pypi.org/project/pip/) to install praw and pandas
```bash
pip install praw pandas
```

### **Step 4: Download the Script**

Above you will find the python script called `save_comments.py`.
You will also find a json called `config.json`.
Download the files or clone this repository.

### **Step 5: Configure the Script**
1. Open `config.json` in your preferred editor.
2. Replace placeholders (e.g., YOUR_CLIENT_ID, YOUR_CLIENT_SECRET) with the credentials from Step 2.
3. Make sure the necessary files `saved_comments.csv`, `save_comments.py` and `config.json` are all in the same folder.
    - This behavior may also be changed using input parameters (see *options*). They only have to be in the same folder by default.

## **Usage**

### **Run the Script**
   
```bash
python3 save_comments.py
```

### **Options**
The following options are possible to add in order to change download behavior:
  - `--config`
    - If the path to a configuration file is supplied with this option, the script will use the specified config
    - Default is `config.json` in the same folder that the script is in
  - `--file-scheme`
    - This flag lets you set a custom naming scheme for files
    - Default is `{TITLE}_{POSTID}_{COMMENTID}`
    - Possible Placeholders are `{TITLE}`, `{POSTID}`, `{COMMENTID}`, and `{SUBREDDIT}`
  - `--input`
    - Path to the input CSV file containing saved comments
    - Default is `saved_comments.csv` in the same folder that the script is in
  - `--output`
    - Path to the directory to save the downloaded comments in
    - Default is a folder called `saved_comments` within the folder that the script was executed in
  - `--skip-images`
    - If set, does not download images or GIFs linked in comments
  - `--unsave`
    - If set, unsaves the downloaded comments from Reddit
   
**Example**: To name each file only according to the comment ID:
```bash
python3 save_comments.py --file-scheme {COMMENTID}
```

**Example**: To unsave every comment after downloading: 
```bash
python3 save_comments.py --unsave
```

**Example**: To supply a different name for the _config_ and a different folder for the _output_: 
```bash
python3 save_comments.py --input different_config.json --output path/to/your/folder
```

### **Output**
- Files are stored in folders named after their respective `{SUBREDDIT}`(e.g. `r/funny`).
- This mirrors the default behavior of [BDFR](https://github.com/Serene-Arc/bulk-downloader-for-reddit#downloader-options).

---

## Thank you
If you read this far, thank you for taking the time.
I am very much open to discussion about the topic. If you have any suggestions, opinions or constructive criticism please let me know!
