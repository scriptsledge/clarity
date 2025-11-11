# Contributing to Clarity

First off, thank you for considering contributing! This project is a learning journey for all of us. This guide will walk you through the entire process of making a contribution, from setting up your environment to getting your code merged.

We use a workflow called **GitHub Flow**. The core idea is simple: the `main` branch is always stable, and all new work is done in separate branches and then merged into `main` through a **Pull Request (PR)**.

---

## 📝 The Development Workflow: A Step-by-Step Guide

Here is the complete workflow for making a change. Follow these steps every time you start a new task.

### **Step 1: Set Up Your Local Environment (First-Time Only)**

If this is your first time contributing, you need to set up a local copy of the project.

1.  **Fork the Repository**
    *   Go to the main project repository: [https://github.com/scriptsledge/clarity](https://github.com/scriptsledge/clarity)
    *   Click the **"Fork"** button in the top-right corner. This creates a personal copy of the project under your own GitHub account.

2.  **Clone Your Fork**
    *   Go to your forked repository on GitHub (e.g., `https://github.com/YourUsername/clarity`).
    *   Click the green **"Code"** button and copy the HTTPS URL.
    *   On your local machine, run this command to download your fork:
        ```bash
        git clone https://github.com/YourUsername/clarity.git
        ```
    *   This creates a `clarity` folder on your computer. Navigate into it:
        ```bash
        cd clarity
        ```

3.  **Connect to the Main Repository**
    *   You need to tell your local copy about the main project so you can keep it updated. We do this by adding an "upstream" remote.
        ```bash
        git remote add upstream https://github.com/scriptsledge/clarity.git
        ```

### **Step 2: The Contribution Loop (For Every New Task)**

Once your setup is complete, you'll follow this loop for every new feature or bug fix.

1.  **Sync Your Fork**
    *   Before you start any new work, make sure your local `main` branch is up-to-date with the main project's `main` branch.
        ```bash
        # Switch to your main branch
        git switch main

        # Pull the latest changes from the main project
        git pull upstream main
        ```

2.  **Create a New Branch**
    *   Create a new branch for your task. This isolates your changes. Use a descriptive name, like `your-name/add-login-button`.
        ```bash
        git switch -c your-name/your-feature-name
        ```

3.  **Do the Work**
    *   Now, you can write your code! Make your changes to the files.
    *   As you work, run the project locally to test your changes and make sure everything works as expected.

4.  **Commit Your Changes**
    *   Once you're happy with your changes, you need to "commit" them. A commit is a snapshot of your work.
        ```bash
        # Add all the files you've changed
        git add .

        # Commit them with a descriptive message
        git commit -m "feat: Add a cool new feature"
        ```
    *   **Good Commit Messages Are Important!** Start your message with a type like `feat:` (for a new feature), `fix:` (for a bug fix), or `docs:` (for documentation).

5.  **Push Your Branch to Your Fork**
    *   Send your new branch and its commits up to your fork on GitHub.
        ```bash
        git push -u origin your-name/your-feature-name
        ```

6.  **Open a Pull Request (PR)**
    *   Go to your fork on GitHub (`https://github.com/YourUsername/clarity`).
    *   GitHub will see your new branch and show a button to **"Compare & pull request"**. Click it.
    *   You'll be taken to a new page. Make sure the base repository is `scriptsledge/clarity` and the branch is `main`.
    *   Write a clear title and description for your PR. Explain **why** you made the change and **what** it does. If it fixes a GitHub Issue, mention it (e.g., "Fixes #12").
    *   Click **"Create pull request"**.

### **Step 3: Code Review**

*   Once your PR is open, other team members will review your code.
*   They might leave comments or request changes. This is a normal and healthy part of collaboration!
*   If you need to make changes, just make more commits to your branch and push them. The PR will update automatically.
*   Once your PR is approved, it will be merged into the `main` branch. Congratulations!

---

Thank you for contributing and helping us make Clarity awesome!
