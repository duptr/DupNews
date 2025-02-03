# DupNews 📰

## RSS News Collection, Summarization, and Management System

![image(1).jpg](https://i.imgur.com/V54VLHa.jpeg)

## ✨ Key Features

- 📡 **Multiple RSS Source Management – Add unlimited sources with a single config file**

- 🤖 **Smart Summarization – NLP-based news summarization algorithm**

- 🌐 **Multi-language Support – Automatic translation in 100+ languages (Google Translate API integration)**

- 💾 **Data Management – Store news both in SQLite and TXT format**

- 📊 **Logging System – Detailed log of all processes (logs/ folder)**

## 🔧 Installation

### Requirements:

```powershell
aiohttp==3.11.10
beautifulsoup4==4.12.3
feedparser==6.0.11
googletrans==3.1.0a0
langdetect==1.0.9
torch==2.5.1+cu118
transformers==4.48.2

```

- **You can install the required libraries for the project by running the following command:**

```powershell
pip install -r requirements.txt

```

### Running the Project:

- **Go to the directory where you saved it.**

**Example:**

```powershell
C:\Users\PC>cd DupNews

```

- **Run the project:**

```powershell
C:\Users\PC\DupNews>python dupnews.py

```

## 🌍 Usage

### Config Setup:

- **Keep and store your RSS sources and categories in the "_config/make_json.py_” file. Instead of deleting sources that you need to filter, comment them out using “#”. This way, you won't lose the source, and you can apply the filter as needed. Running the file will generate your "_config.json_" file.**

#### make_json

![make_json](https://i.imgur.com/nASArSO.png)

#### config.json

![config_json](https://i.imgur.com/GUe8bRw.png)

### Output:

- **Run the program to fetch and summarize news. Optionally, you can also activate the translation feature.**
- **If you want to read your news right away, you can read it from the “.txt” file.**

#### Example:

![text](https://i.imgur.com/YBZyb2c.png)

- **To view the past news and perform analysis, you can use the “db” file.**

**Once “dupnews.py” is running, the news will be added to the database.**

**To inspect the database, install a database management software.**

**For example, if you are using Visual Studio Code, you can install the SQLite extension from the extensions section.**

![extension](https://i.imgur.com/IoxCxUF.png)

**You can run queries on the database:**

```sql
--To get the output of all data:
SELECT * FROM news;

```

**Example Usage:**

![sqlite_workflow_1.gif](https://i.imgur.com/6yOHacl.gif)


## License

**This project is licensed under the MIT License - see the LICENSE file for details.**


## Contributing
**_If you would like to contribute to this project, please open an issue or submit a pull request._**
