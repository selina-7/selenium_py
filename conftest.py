"""
Pytest configuration file.
- Chrome driver management
- Automatic screenshot on test failure
- Detailed error logging with English explanations
- Soft pastel theme HTML report
"""
import pytest
import os
import base64
import traceback
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    ElementNotInteractableException,
)
from webdriver_manager.chrome import ChromeDriverManager

REPORTS_DIR     = os.path.join(os.path.dirname(__file__), "reports")
SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, "screenshots")
LOGS_DIR        = os.path.join(REPORTS_DIR, "logs")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)


# Soft pastel theme CSS
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

* { box-sizing: border-box; }

body {
    font-family: 'Inter', -apple-system, sans-serif !important;
    background: #faf7fc !important;
    color: #2d2438 !important;
    line-height: 1.6 !important;
    padding: 24px !important;
}

h1 {
    color: #6d4f8a !important;
    font-weight: 700 !important;
    font-size: 28px !important;
    border-bottom: 3px solid #d4b8e8 !important;
    padding-bottom: 12px !important;
    margin-bottom: 24px !important;
}

h2 {
    color: #8a6ba8 !important;
    font-weight: 600 !important;
    margin-top: 32px !important;
}

p { color: #5a4a6e !important; }

#environment, #results-table {
    background: #ffffff !important;
    border-radius: 12px !important;
    padding: 16px !important;
    box-shadow: 0 2px 8px rgba(141, 107, 168, 0.08) !important;
    border: 1px solid #ece4f3 !important;
}

#environment td:first-child {
    font-weight: 600 !important;
    color: #6d4f8a !important;
    width: 200px !important;
}

#results-table thead tr {
    background: linear-gradient(135deg, #b89dd0 0%, #d4a8c8 100%) !important;
    color: #ffffff !important;
}

#results-table thead th {
    padding: 14px 12px !important;
    font-weight: 600 !important;
    text-align: left !important;
}

#results-table tbody tr {
    border-bottom: 1px solid #f3ebf8 !important;
}

#results-table tbody tr:hover {
    background: #f8f1fb !important;
}

.passed {
    background: #f0f8ed !important;
    color: #4a6b3d !important;
    border-left: 4px solid #8bc97a !important;
}

.failed {
    background: #fdf0f3 !important;
    color: #8b4a5c !important;
    border-left: 4px solid #e89aa8 !important;
    font-weight: 500 !important;
}

.error {
    background: #fdf6ee !important;
    color: #8b6a3d !important;
    border-left: 4px solid #e8b87a !important;
}

.skipped {
    background: #eef4f8 !important;
    color: #4a6580 !important;
    border-left: 4px solid #9bb8d4 !important;
}

.col-result { font-weight: 600 !important; padding: 12px !important; }
.col-name   { font-family: 'JetBrains Mono', monospace !important; font-size: 13px !important; }

.log {
    background: #f8f4fb !important;
    border: 1px solid #ece4f3 !important;
    border-radius: 8px !important;
    padding: 16px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    color: #3d2e4f !important;
    white-space: pre-wrap !important;
}

.error-section {
    background: #fdf0f3 !important;
    border: 1px solid #f5d4dc !important;
    border-radius: 8px !important;
    padding: 16px !important;
    margin: 12px 0 !important;
}

.test-description {
    background: #f0eaf6 !important;
    border-left: 3px solid #b89dd0 !important;
    padding: 10px 14px !important;
    margin: 8px 0 !important;
    border-radius: 4px !important;
    font-style: italic !important;
    color: #5a4a6e !important;
}

img {
    max-width: 100% !important;
    border-radius: 8px !important;
    box-shadow: 0 2px 12px rgba(141, 107, 168, 0.15) !important;
    margin-top: 12px !important;
}

button, input[type="button"], .filter-container label {
    background: #e8d5f0 !important;
    color: #5a3d75 !important;
    border: 1px solid #d4b8e8 !important;
    border-radius: 6px !important;
    padding: 6px 14px !important;
    font-weight: 500 !important;
}

button:hover { background: #d4b8e8 !important; }
"""


def pytest_configure(config):
    """Set report metadata."""
    config._metadata = {
        "Project Name": "SauceDemo Automated Testing Framework",
        "Tested Site": "https://www.saucedemo.com",
        "Framework": "Selenium WebDriver + Pytest",
        "Architecture": "Page Object Model (POM)",
        "Test Date": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "Developers": "Selina Kudret, Svetlana Caraseni, Abdulmuhsen Alzouba",
    }


def pytest_html_report_title(report):
    report.title = "Test Report - Detailed Analysis"


def pytest_html_results_summary(prefix, summary, postfix):
    """Add custom CSS and description to report header."""
    prefix.extend([
        "<style>" + CUSTOM_CSS + "</style>",
        """
        <div style='background: #fff; padding: 20px; border-radius: 12px; margin: 16px 0; border: 1px solid #ece4f3;'>
            <h3 style='color: #6d4f8a; margin-top: 0;'>About This Report</h3>
            <p style='color: #5a4a6e; margin-bottom: 8px;'>
                This report shows the results of automated tests run on the SauceDemo e-commerce site.
                Each test includes a description, expected behavior, actual result, and on failure
                a screenshot is embedded with technical details for debugging.
            </p>
            <p style='color: #5a4a6e; margin-bottom: 0;'>
                <strong>Color Codes:</strong>
                <span style='color: #4a6b3d; font-weight: 600;'>● Green</span> Passed |
                <span style='color: #8b4a5c; font-weight: 600;'>● Red</span> Failed |
                <span style='color: #8b6a3d; font-weight: 600;'>● Orange</span> Error |
                <span style='color: #4a6580; font-weight: 600;'>● Blue</span> Skipped
            </p>
        </div>
        """
    ])


@pytest.fixture(scope="function")
def driver():
    """Opens new Chrome for each test, closes after test ends."""
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    drv.maximize_window()

    yield drv

    drv.quit()


def classify_error(exception):
    """Translate Selenium errors into human-readable explanations with possible causes and fixes."""
    if isinstance(exception, TimeoutException):
        return {
            "type": "Timeout (TimeoutException)",
            "meaning": "The expected element was not found on the page within the given time.",
            "possible_causes": [
                "Page has not fully loaded yet (slow internet or slow server)",
                "Element ID or CSS selector is defined incorrectly",
                "Element may be covered by another element",
                "Page structure (HTML) may have changed",
            ],
            "solution": "Increase WebDriverWait duration or verify the element selector.",
        }
    elif isinstance(exception, NoSuchElementException):
        return {
            "type": "Element Not Found (NoSuchElementException)",
            "meaning": "The searched element does not exist on the page at all.",
            "possible_causes": [
                "Element ID/class name is incorrect",
                "You are on the wrong page",
                "Element is dynamically created via JavaScript",
            ],
            "solution": "Check the actual element selector using browser DevTools.",
        }
    elif isinstance(exception, ElementClickInterceptedException):
        return {
            "type": "Click Intercepted (ElementClickInterceptedException)",
            "meaning": "Another element (popup, banner) is overlapping the target element.",
            "possible_causes": [
                "Cookie banner or modal is blocking the element",
                "Page needs to be scrolled",
            ],
            "solution": "Close the blocking element first, or use scrollIntoView.",
        }
    elif isinstance(exception, StaleElementReferenceException):
        return {
            "type": "Stale Element Reference (StaleElementReferenceException)",
            "meaning": "Element was found but the page has been reloaded; reference is invalid.",
            "possible_causes": [
                "Page updated content via AJAX",
                "DOM has been re-rendered",
            ],
            "solution": "Re-find the element; do not cache element references.",
        }
    elif isinstance(exception, ElementNotInteractableException):
        return {
            "type": "Element Not Interactable (ElementNotInteractableException)",
            "meaning": "Element exists in DOM but cannot be interacted with (hidden, disabled, or covered).",
            "possible_causes": [
                "Element is hidden via CSS (display:none, visibility:hidden)",
                "Element is disabled or read-only",
                "Element is outside the viewport",
            ],
            "solution": "Wait for element to become interactable or scroll into view.",
        }
    elif isinstance(exception, AssertionError):
        return {
            "type": "Assertion Error (AssertionError)",
            "meaning": "The expected outcome did not match the actual outcome.",
            "possible_causes": [
                "Site did not behave as expected",
                "Test data is incorrect",
                "Previous step failed; effect carries over",
            ],
            "solution": "Verify test logic and test data.",
        }
    else:
        return {
            "type": type(exception).__name__,
            "meaning": str(exception)[:200],
            "possible_causes": ["Unexpected error"],
            "solution": "Inspect the full stack trace.",
        }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Called after each test. On failure, generates screenshot + detailed log."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    if rep.when == "call" and rep.failed:
        drv = item.funcargs.get("driver")
        if drv is None:
            return

        ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = item.name.replace("[", "_").replace("]", "")
        screenshot_path = os.path.join(SCREENSHOTS_DIR, f"FAIL_{name}_{ts}.png")
        log_path        = os.path.join(LOGS_DIR, f"FAIL_{name}_{ts}.txt")

        try:
            drv.save_screenshot(screenshot_path)
        except Exception as e:
            print(f"\n[WARNING] Screenshot could not be taken: {e}")
            return

        exception  = call.excinfo.value if call.excinfo else None
        error_info = classify_error(exception) if exception else {}
        test_doc   = (item.function.__doc__ or "").strip() or "No description available."

        try:
            current_url   = drv.current_url
            current_title = drv.title
        except Exception:
            current_url, current_title = "Could not retrieve", "Could not retrieve"

        # Write detailed log file
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("=" * 70 + "\n")
            f.write("TEST FAILURE REPORT\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Test Name        : {item.name}\n")
            f.write(f"Date             : {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
            f.write(f"Test Description : {test_doc}\n")
            f.write(f"URL at Failure   : {current_url}\n")
            f.write(f"Page Title       : {current_title}\n\n")
            f.write("-" * 70 + "\n")
            f.write(f"ERROR TYPE       : {error_info.get('type', 'Unknown')}\n")
            f.write(f"WHAT IT MEANS    : {error_info.get('meaning', '')}\n\n")
            f.write("POSSIBLE CAUSES:\n")
            for cause in error_info.get("possible_causes", []):
                f.write(f"  - {cause}\n")
            f.write(f"\nSUGGESTED FIX    : {error_info.get('solution', '')}\n\n")
            f.write("-" * 70 + "\n")
            f.write("FULL ERROR MESSAGE:\n")
            f.write(str(exception) + "\n\n")
            f.write("STACK TRACE:\n")
            f.write("".join(traceback.format_exception(type(exception), exception, exception.__traceback__)))

        # Console summary
        print(f"\n{'='*60}")
        print(f"TEST FAILED: {item.name}")
        print(f"   Description : {test_doc[:80]}")
        print(f"   Error Type  : {error_info.get('type', 'Unknown')}")
        print(f"   URL         : {current_url}")
        print(f"   Screenshot  : reports/screenshots/FAIL_{name}_{ts}.png")
        print(f"   Detail Log  : reports/logs/FAIL_{name}_{ts}.txt")
        print(f"{'='*60}")

        # Embed in HTML report
        if hasattr(rep, "extras"):
            try:
                import pytest_html

                with open(screenshot_path, "rb") as f:
                    img_b64 = base64.b64encode(f.read()).decode()

                html_detail = f"""
                <div class='error-section'>
                    <h4 style='color: #8b4a5c; margin-top: 0;'>Test Description</h4>
                    <div class='test-description'>{test_doc}</div>

                    <h4 style='color: #8b4a5c;'>Error Details</h4>
                    <table style='width: 100%; border-collapse: collapse;'>
                        <tr><td style='padding: 6px; font-weight: 600; width: 180px;'>Error Type:</td>
                            <td style='padding: 6px;'>{error_info.get('type', 'Unknown')}</td></tr>
                        <tr><td style='padding: 6px; font-weight: 600;'>What It Means:</td>
                            <td style='padding: 6px;'>{error_info.get('meaning', '')}</td></tr>
                        <tr><td style='padding: 6px; font-weight: 600;'>URL at Failure:</td>
                            <td style='padding: 6px;'><code>{current_url}</code></td></tr>
                        <tr><td style='padding: 6px; font-weight: 600;'>Page Title:</td>
                            <td style='padding: 6px;'>{current_title}</td></tr>
                    </table>

                    <h4 style='color: #8b4a5c;'>Possible Causes</h4>
                    <ul style='color: #5a4a6e;'>
                        {''.join(f'<li>{c}</li>' for c in error_info.get('possible_causes', []))}
                    </ul>

                    <h4 style='color: #8b4a5c;'>Suggested Fix</h4>
                    <p style='color: #5a4a6e; padding: 10px; background: #f0f8ed; border-radius: 6px; border-left: 3px solid #8bc97a;'>
                        {error_info.get('solution', '')}
                    </p>

                    <h4 style='color: #8b4a5c;'>Screenshot at Time of Failure</h4>
                </div>
                """

                rep.extras.append(pytest_html.extras.html(html_detail))
                rep.extras.append(pytest_html.extras.image(f"data:image/png;base64,{img_b64}"))

            except Exception as e:
                print(f"[WARNING] HTML detail could not be added: {e}")
