# GitVerse 🌌

**Explore GitHub. Visualize Your Work. Showcase Your Code.**

GitVerse is a web-based GitHub profile analytics tool that allows users to explore public GitHub profiles, compare developers, visualize repository statistics, and generate a downloadable portfolio using GitHub profile data.

The project uses the GitHub REST API to retrieve profile and repository information and presents it through an interactive dashboard with charts and profile cards.

---

## ✨ Features

### 1. GitHub Profile Search
- Search for any GitHub user using their username.
- Retrieve public profile information directly from the GitHub API.
- Display profile picture, name, username, and bio.
- View important statistics:
  - Total public repositories
  - Followers
  - Following
  - Total stars across the retrieved repositories
- Display the user's location and website when available.

### 2. Compare GitHub Profiles
- Compare two GitHub users using the Compare option.
- View both developers' profile cards together.
- Analyze combined programming language usage.
- Compare repository performance through star analytics.
- View top repositories from both users.

### 3. Repository Analytics
GitVerse transforms repository information into visual insights.

**Language Usage**
- Displays the distribution of programming languages used across repositories.
- Uses a pie chart to represent language statistics.
- Helps understand a developer's programming language preferences.

**Repository Star Analytics**
- Displays the most-starred repositories.
- Uses a horizontal bar chart to visualize repository stars.
- Makes it easier to identify popular projects.

### 4. Top Repositories
Explore the most-starred repositories with information such as:
- Repository name
- Repository description
- Stars
- Forks
- Primary programming language

Repository names also link directly to their respective GitHub pages.

### 5. Portfolio Generator
GitVerse can generate a downloadable HTML portfolio using the searched GitHub profile.

The generated portfolio includes:
- Developer name and GitHub username
- Profile picture
- Bio
- Followers and public repository count
- Top programming languages
- Top repositories with descriptions and star counts

The generated portfolio is downloaded as an HTML file and can be opened directly in a browser.

### 6. Animated Landing Page
- Dedicated landing page introducing GitVerse.
- GSAP-powered entrance animations.
- Navigation to the analytics dashboard through the Enter button.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| HTML5 | Structure of the application |
| CSS3 | Styling, layout, and responsive presentation |
| JavaScript | Application logic and API integration |
| GitHub REST API | Fetching public GitHub profile and repository data |
| Chart.js | Language and repository analytics |
| GSAP | Landing page animations |
| Google Fonts | Space Mono typography |

---

## 🏗️ Project Structure

```text
GitVerse/
│
├── index.html          # Landing page
├── index.css           # Landing page styling
├── index.js            # GSAP landing page animations
│
├── dashboard.html      # Main analytics dashboard
├── dashboard.css       # Dashboard styling
├── dashboard.js        # API integration and application logic
│
└── README.md           # Project documentation
```

---

## ⚙️ Getting Started

GitVerse is a frontend-only project. It does not require a backend, database, or package installation.

### Prerequisites

- A modern web browser
- Internet connection to access the GitHub API and external libraries

### 1. Clone the Repository

```bash
git clone https://github.com/Akanksha-1708/GitVerse.git
```

### 2. Navigate to the Project Directory

```bash
cd GitVerse
```

### 3. Run the Application

Open `index.html` in your browser.

Alternatively, use the Live Server extension in VS Code:

1. Open the GitVerse folder in VS Code.
2. Install the Live Server extension if it is not already installed.
3. Right-click `index.html`.
4. Select **Open with Live Server**.

### 4. Explore GitVerse

1. Click **Enter** on the landing page.
2. Enter a GitHub username.
3. Click **Search** to view profile information and analytics.
4. Enable **Compare** and enter a second username to compare profiles.
5. Click **Generate Portfolio** to download an HTML portfolio.

---

## 🔄 How It Works

GitVerse follows a simple frontend-based workflow:

```text
        User Opens GitVerse
                |
                v
          Landing Page
                |
                v
         Analytics Dashboard
                |
                v
       Enter GitHub Username
                |
                v
       GitHub REST API Requests
                |
          +-----+-----+
          |           |
          v           v
      User Data   Repository Data
          |           |
          +-----+-----+
                |
                v
        Data Processing
                |
       +--------+--------+
       |        |        |
       v        v        v
    Profile  Analytics  Top Repos
     Cards     Charts
                |
                v
       Generate HTML Portfolio
                |
                v
        Download Portfolio
```

### Data Processing

The application retrieves two types of information from GitHub:

- **User endpoint:** Fetches public profile information.
- **Repositories endpoint:** Fetches up to 100 owned repositories, sorted by recently updated.

JavaScript processes the retrieved data to calculate language distribution, total stars, and top repositories.

Chart.js then visualizes the processed information.

---

## 🌐 API Integration

GitVerse uses the GitHub REST API.

**Endpoints used:**

| Endpoint | Purpose |
|---|---|
| `GET /users/{username}` | Fetch GitHub profile information |
| `GET /users/{username}/repos` | Fetch public repositories |

Official documentation:

[GitHub REST API Documentation](https://docs.github.com/en/rest)

**Note:** GitVerse currently retrieves public GitHub data without authentication. GitHub applies API rate limits to unauthenticated requests, so repeated searches may temporarily fail when the limit is reached.

---

## 📌 Current Scope and Limitations

- The application currently works with public GitHub profile and repository information.
- Repository retrieval is limited to the first 100 results.
- Language analytics are based on the primary language reported for each repository, rather than actual code-line percentages.
- Portfolio generation produces a standalone HTML file.
- The project does not currently have a backend or database.
- API availability and rate limits depend on GitHub.

---

## 🚀 Future Enhancements

Some improvements planned for future development:

- More detailed repository analytics and contribution insights.
- Improved developer comparison with additional metrics.
- Enhanced portfolio templates and customization.
- Better portfolio styling and downloadable formats.
- Improved error handling and loading states.
- More advanced GitHub activity visualizations.
- Improved mobile responsiveness.

---

## 🎯 Project Objective

GitVerse was developed as a hands-on project to explore frontend development, JavaScript, API integration, and data visualization.

The main objective is to make GitHub profile information easier to understand and present by transforming raw profile and repository data into meaningful visual insights.

Through this project, I explored:
- Working with REST APIs and asynchronous JavaScript.
- Fetching and processing JSON data.
- DOM manipulation and dynamic UI rendering.
- Data visualization using Chart.js.
- Animations using GSAP.
- Generating downloadable HTML content using JavaScript Blob APIs.

---

## 👩‍💻 Author

**Akanksha Dwivedi**

B.Tech Computer Science and Engineering Student

- GitHub: [Akanksha-1708](https://github.com/Akanksha-1708)
- Project Repository: [GitVerse](https://github.com/Akanksha-1708/GitVerse)

---

⭐ If you find this project interesting, consider giving the repository a star!
