<p align="center"><h1 align="center">RED0XTELEGRAMBOT</h1></p>
<p align="center">
	<img src="https://img.shields.io/github/license/maziyar-redox/Red0xTelegramBot?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/maziyar-redox/Red0xTelegramBot?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/maziyar-redox/Red0xTelegramBot?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/maziyar-redox/Red0xTelegramBot?style=default&color=0080ff" alt="repo-language-count">
</p>
<p align="center"><!-- default option, no dependency badges. -->
</p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>
<br>

##  Table of Contents

- [ Overview](#-overview)
- [ Features](#-features)
- [ Project Structure](#-project-structure)
  - [ Project Index](#-project-index)
- [ Getting Started](#-getting-started)
  - [ Prerequisites](#-prerequisites)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Testing](#-testing)
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)

---

##  Project Structure

```sh
└── Red0xTelegramBot/
    ├── README.md
    ├── Red0xBot
    │   ├── __init__.py
    │   ├── bot
    │   ├── config.py
    │   ├── db
    │   ├── server
    │   └── utils
    ├── books_db.csv
    ├── main.py
    └── requirements.txt
```


###  Project Index
<details open>
	<summary><b><code>RED0XTELEGRAMBOT/</code></b></summary>
	<details> <!-- __root__ Submodule -->
		<summary><b>__root__</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/maziyar-redox/Red0xTelegramBot/blob/master/main.py'>main.py</a></b></td>
				<td><code>❯ Application Entry point</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/maziyar-redox/Red0xTelegramBot/blob/master/requirements.txt'>requirements.txt</a></b></td>
				<td><code>❯ Requirements file</code></td>
			</tr>
			</table>
		</blockquote>
	</details>
	<details> <!-- Red0xBot Submodule -->
		<summary><b>Red0xBot</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/maziyar-redox/Red0xTelegramBot/blob/master/Red0xBot/config.py'>config.py</a></b></td>
				<td><code>❯ Bot config</code></td>
			</tr>
			</table>
			<details>
				<summary><b>utils</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/maziyar-redox/Red0xTelegramBot/blob/master/Red0xBot/utils/translation.py'>translation.py</a></b></td>
						<td><code>❯ Bot buttons</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/maziyar-redox/Red0xTelegramBot/blob/master/Red0xBot/utils/time_format.py'>time_format.py</a></b></td>
						<td><code>❯ Datetime formatter</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>server</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/maziyar-redox/Red0xTelegramBot/blob/master/Red0xBot/server/stream_routes.py'>stream_routes.py</a></b></td>
						<td><code>❯ Http routing for downloading file</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/maziyar-redox/Red0xTelegramBot/blob/master/Red0xBot/server/exceptions.py'>exceptions.py</a></b></td>
						<td><code>❯ Server exceptions</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>bot</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/maziyar-redox/Red0xTelegramBot/blob/master/Red0xBot/bot/clients.py'>clients.py</a></b></td>
						<td><code>❯ telegram clients for some features</code></td>
					</tr>
					</table>
					<details>
						<summary><b>plugins</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/maziyar-redox/Red0xTelegramBot/blob/master/Red0xBot/bot/plugins/admin.py'>admin.py</a></b></td>
								<td><code>❯ Admin template</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/maziyar-redox/Red0xTelegramBot/blob/master/Red0xBot/bot/plugins/start.py'>start.py</a></b></td>
								<td><code>❯ User template</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
				</blockquote>
			</details>
			<details>
				<summary><b>db</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/maziyar-redox/Red0xTelegramBot/blob/master/Red0xBot/db/csv_db.py'>csv_db.py</a></b></td>
						<td><code>❯ Book db</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
</details>

---
##  Getting Started

###  Prerequisites

Before getting started with Red0xTelegramBot, ensure your runtime environment meets the following requirements:

- **Programming Language:** Python
- **Package Manager:** Pip


###  Installation

Install Red0xTelegramBot using one of the following methods:

**Build from source:**

1. Clone the Red0xTelegramBot repository:
```sh
❯ git clone https://github.com/maziyar-redox/Red0xTelegramBot
```

2. Navigate to the project directory:
```sh
❯ cd Red0xTelegramBot
```

3. Install the project dependencies:


**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ pip install -r requirements.txt
```




###  Usage
Run Red0xTelegramBot using the following command:
**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ python {entrypoint}
```


###  Testing
Run the test suite using the following command:
**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ pytest
```

---

##  Contributing

- **💬 [Join the Discussions](https://github.com/maziyar-redox/Red0xTelegramBot/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://github.com/maziyar-redox/Red0xTelegramBot/issues)**: Submit bugs found or log feature requests for the `Red0xTelegramBot` project.
- **💡 [Submit Pull Requests](https://github.com/maziyar-redox/Red0xTelegramBot/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/maziyar-redox/Red0xTelegramBot
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/maziyar-redox/Red0xTelegramBot/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=maziyar-redox/Red0xTelegramBot">
   </a>
</p>
</details>

---

##  License

This project is protected under the [MIT](https://choosealicense.com/licenses/mit) License. For more details, refer to the [LICENSE](https://github.com/maziyar-redox/Red0xTelegramBot/blob/main/LICENSE) file.

---

##  Acknowledgments

- List any resources, contributors, inspiration, etc. here.

---