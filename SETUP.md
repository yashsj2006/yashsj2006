# Setup & Deployment Instructions

1. **Create Special GitHub Repository**:
   - Go to GitHub and create a new public repository named **`yashsj2006`** (matching your GitHub username `yashsj2006`).
   - Leave it empty (do not initialize with README).

2. **Push Workspace Code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "feat: initial animated profile README setup"
   git branch -M main
   git remote add origin https://github.com/yashsj2006/yashsj2006.git
   git push -u origin main
   ```

3. **Configure Workflow Permissions**:
   - On GitHub, navigate to: **Settings** -> **Actions** -> **General** -> **Workflow permissions**.
   - Select **Read and write permissions** and click **Save**.

4. **Enable Jet Heatmap Automation**:
   - Go to the **Actions** tab in your repository.
   - Select **Update jet heatmap SVG** and click **Run workflow**.
   - The workflow will run automatically every day at 05:30 UTC to fetch your real GitHub contribution calendar and animate the jet heatmap.

5. **Regenerating ASCII Portrait (Optional)**:
   - Your photo has already been converted into `portrait.txt` and built into `dark.svg` / `light.svg`.
   - If you ever want to update your photo in the future, run:
     ```bash
     python image_to_ascii.py new_photo.jpg
     python build_profile.py
     ```
