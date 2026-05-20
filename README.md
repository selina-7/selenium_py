# 🧪 SauceDemo Automated Testing Framework

> Automated end-to-end testing framework for [SauceDemo](https://www.saucedemo.com/) built with **Selenium WebDriver**, **Python**, and **Pytest** — following the Page Object Model (POM) architecture.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.x-green.svg)](https://www.selenium.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-7.x-yellow.svg)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)](https://opensource.org/licenses/MIT)

---

## 📌 About the Project

This project is a **test automation framework** designed to validate e-commerce flows on the SauceDemo demo application. The framework demonstrates industry-standard practices in QA automation engineering:

- ✅ **Page Object Model (POM)** — clean separation between test logic and page interactions
- ✅ **Pytest fixtures** — reusable setup/teardown logic with `conftest.py`
- ✅ **Custom HTML reports** — visually styled test reports with screenshots
- ✅ **Automatic ChromeDriver management** — no manual driver setup needed
- ✅ **Failure screenshots** — automatic screenshot capture on test failures

This project was built as part of my journey to deepen my understanding of test automation principles within a software engineering curriculum.

---

## ✨ Features

- 🔐 **Login flow testing** — valid credentials, invalid credentials, locked-out users
- 🛒 **Shopping cart automation** — add/remove items, verify cart state
- 💳 **End-to-end checkout flow** — complete purchase journey simulation
- 📸 **Auto-screenshot on failure** — captured in `reports/screenshots/`
- 📊 **HTML test reports** — generated automatically after each run
- 🎨 **Custom-styled reports** — purple/pink theme for better readability

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Language** | Python 3.9+ |
| **Automation** | Selenium WebDriver 4.x |
| **Test Runner** | Pytest |
| **Pattern** | Page Object Model (POM) |
| **Reporting** | pytest-html with custom CSS |
| **Driver Management** | webdriver-manager |

---

## 📂 Project Structure

```
selenium_py/
│
├── pages/
│   └── login_page.py          # Page Object for the login screen
│
├── tests/
│   ├── test_final.py          # End-to-end test suite
│   ├── test_pom.py            # POM-based tests
│   └── test_sauce.py          # SauceDemo functional tests
│
├── reports/
│   ├── screenshots/           # Auto-captured failure screenshots
│   └── report.html            # Generated test report
│
├── conftest.py                # Pytest fixtures and configuration
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

> **Note:** Adjust this structure to match your actual project files.

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.9 or higher
- Google Chrome browser
- Git

### Step-by-step

```bash
# 1. Clone the repository
git clone https://github.com/selina-7/selenium_py.git
cd selenium_py

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # macOS / Linux
# OR
venv\Scripts\activate      # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Running the Tests

### Run all tests
```bash
pytest
```

### Run a specific test file
```bash
pytest tests/test_sauce.py
```

### Generate an HTML report
```bash
pytest --html=reports/report.html --self-contained-html
```

### Run with verbose output
```bash
pytest -v
```

---

## 📊 Sample Test Report

After running tests, an interactive HTML report is generated in `reports/report.html` with:
- Test results summary (passed/failed counts)
- Detailed logs for each test
- Embedded failure screenshots
- Test execution time metrics

---

## 🎓 What I Learned

Building this framework taught me several core QA engineering principles:

1. **The value of POM** — Separating page interactions from test logic makes tests dramatically easier to maintain when the UI changes.
2. **Pytest fixtures over setUp/tearDown** — Fixtures provide cleaner, more flexible test setup compared to traditional unittest patterns.
3. **Reporting matters as much as testing** — A test that passes is only useful if stakeholders can read why it passed; investing in custom reports paid off immediately.
4. **Automatic screenshots are non-negotiable** — When a test fails on CI, screenshots are the difference between a 5-minute debug and a 5-hour one.

---

## 🔧 Test Coverage

| Test Case | Status |
|-----------|--------|
| Valid user login | ✅ |
| Invalid user login | ✅ |
| Locked-out user handling | ✅ |
| Add product to cart | ✅ |
| Remove product from cart | ✅ |
| Complete checkout flow | ✅ |
| Logout functionality | ✅ |

---

## 🌱 Future Improvements

- [ ] Add CI/CD integration with GitHub Actions
- [ ] Implement parallel test execution with `pytest-xdist`
- [ ] Add cross-browser testing (Firefox, Edge)
- [ ] Integrate with Allure for advanced reporting
- [ ] Add BDD layer using `pytest-bdd` or Behave
- [ ] Dockerize for consistent CI environments

---

## 📝 Notes

> **Important:** SauceDemo (https://www.saucedemo.com/) is a publicly-available test site created by Sauce Labs specifically for practicing browser automation. This project uses it for educational and portfolio demonstration purposes only. I do not own or claim any rights to the SauceDemo website.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Selina Kudret**


Software Engineering Student at Near East University, graduating June 2026.
Software Engineer Intern at Eazy Financial Services (EazyPay), Bahrain — Summer 2025.

- 🔗 LinkedIn: [linkedin.com/in/selina-kudret](https://linkedin.com/in/selina-kudret)
- 💻 GitHub: [@selina-7](https://github.com/selina-7)
- 📧 Email: kudretselina7@gmail.com

---
**Svetlana Caraseni**


Software Engineering Student at Near East University, graduating June 2026.

- 🔗 LinkedIn: https://www.linkedin.com/in/sveta-caraseni-91b903291/
- 💻 GitHub: https://github.com/scaraseni
- 📧 Email: scaraseni@gmail.com
⭐ If you find this project helpful, please consider giving it a star!
