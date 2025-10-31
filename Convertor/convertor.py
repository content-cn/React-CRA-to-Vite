#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
convertor.py: An automated script to migrate a Create React App (CRA) project
to a Vite project structure.

This script performs the following actions:
1.  Sets up a new Vite project directory.
2.  Copies and renames source files from .js to .jsx.
3.  Uses the Google Gemini API to intelligently update internal import paths within .jsx files.
4.  Uses the Google Gemini API to transform the CRA entry point (index.js) to Vite's main.jsx.
5.  Creates Vite-specific configuration files (vite.config.js, package.json, etc.).

Usage:
    python convertor.py /path/to/your/CRA_Project

Prerequisites:
    - Python 3.x
    - google-generativeai library (`pip install google-generativeai`)
    - A valid Google Gemini API Key.
"""

import os
import sys
import shutil
import google.generativeai as genai

# --- CONFIGURATION ---
# IMPORTANT: Replace "YOUR_GEMINI_API_KEY" with your actual Google Gemini API key.
GEMINI_API_KEY = ""

# --- STATIC CONTENT FOR NEW FILES ---

# A. index.html
INDEX_HTML_CONTENT = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>react-app</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body></html>
"""

# B. package.json
PACKAGE_JSON_CONTENT = """
{
  "name": "vite-converted-app",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:run": "vitest run",
    "test:ui": "vitest --ui"
  },
  "dependencies": {
    "firebase": "9.17.1",
    "glob": "^11.0.3",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-toastify": "9.1.1"
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^6.9.1",
    "@testing-library/react": "^16.3.0",
    "@testing-library/user-event": "^14.6.1",
    "@testing-library/dom": "^10.4.0",
    "@vitejs/plugin-react": "^5.0.4",
    "eslint": "^8.57.0",
    "@eslint/js": "^9.8.0",
    "eslint-plugin-react-hooks": "^5.1.0-rc.0",
    "eslint-plugin-react-refresh": "^0.4.9",
    "globals": "^15.8.0",
    "jsdom": "^27.0.0",
    "vitest": "^3.2.4",
    "@originjs/vite-plugin-commonjs": "^1.0.3"
  },
  "type": "module"
}
"""

# C. vite.config.js
VITE_CONFIG_JS_CONTENT = """
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { viteCommonjs } from '@originjs/vite-plugin-commonjs';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), viteCommonjs()],
  test: {
    environment: "jsdom",
    globals: true,           
  },
    resolve: {
    alias: {
      // make @ point to /src
      '@': path.resolve(__dirname, 'src'),
    },
  },
})
"""

# D. eslint.config.js
ESLINT_CONFIG_JS_CONTENT = """
import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import { defineConfig, globalIgnores } from 'eslint/config'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{js,jsx}'],
    extends: [
      js.configs.recommended,
    ],
     plugins: {
        'react-hooks': reactHooks,
        'react-refresh': reactRefresh
    },
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
      parserOptions: {
        ecmaVersion: 'latest',
        ecmaFeatures: { jsx: true },
        sourceType: 'module',
      },
    },
    rules: {
      'no-unused-vars': ['error', { varsIgnorePattern: '^[A-Z_]' }],
      'react-refresh/only-export-components': 'warn'
    },
  },
])
"""


def call_gemini_api(prompt, content):
    """
    Calls the Gemini API with a specific prompt and content, and returns the response.
    Includes error handling for API calls.
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        full_prompt = f"{prompt}\n\n---\n\n{content}"
        response = model.generate_content(full_prompt)
        # Clean up the response to remove markdown code blocks
        cleaned_text = response.text.strip()
        if cleaned_text.startswith("```jsx"):
            cleaned_text = cleaned_text[5:]
        if cleaned_text.startswith("```javascript"):
            cleaned_text = cleaned_text[13:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
        return cleaned_text.strip()
    except Exception as e:
        print(f"\n❌ Error during Gemini API call: {e}")
        print("Please ensure your API key is valid and you have internet access.")
        return None


def main():
    """Main execution function."""
    print("🚀 Starting CRA to Vite Conversion...")

    # --- 1. Directory Setup and Validation ---
    if len(sys.argv) != 2:
        print("\n❌ Error: Invalid usage.")
        print("   Usage: python convertor.py <path_to_cra_project_directory>")
        sys.exit(1)

    source_dir = sys.argv[1]
    if not os.path.isdir(source_dir):
        print(f"\n❌ Error: Source directory '{source_dir}' not found.")
        sys.exit(1)

    source_src_dir = os.path.join(source_dir, 'src')
    if not os.path.isdir(source_src_dir):
        print(f"\n❌ Error: 'src' directory not found in '{source_dir}'. Is this a valid CRA project?")
        sys.exit(1)

    # Configure Gemini API
    try:
        genai.configure(api_key=API_KEY)
    except Exception as e:
        print(f"\n❌ Error configuring Gemini API: {e}")
        sys.exit(1)

    # Create output directory
    base_name = os.path.basename(os.path.normpath(source_dir))
    dest_dir = f"{base_name}-Vite"
    print(f"   Input CRA Project: {source_dir}")
    print(f"   Output Vite Project: {dest_dir}")

    try:
        if os.path.exists(dest_dir):
            print(f"   Destination '{dest_dir}' already exists. Removing it.")
            shutil.rmtree(dest_dir)
        
        dest_src_dir = os.path.join(dest_dir, 'src')
        dest_public_dir = os.path.join(dest_dir, 'public')
        os.makedirs(dest_src_dir)
        os.makedirs(dest_public_dir)
        print("✅ Directory structure created successfully.")
    except OSError as e:
        print(f"\n❌ Error creating directories: {e}")
        sys.exit(1)


    # --- 2. Create Static/New Files ---
    print("\n📄 Creating Vite configuration files...")
    try:
        with open(os.path.join(dest_dir, 'index.html'), 'w') as f:
            f.write(INDEX_HTML_CONTENT)
        with open(os.path.join(dest_dir, 'package.json'), 'w') as f:
            f.write(PACKAGE_JSON_CONTENT)
        with open(os.path.join(dest_dir, 'vite.config.js'), 'w') as f:
            f.write(VITE_CONFIG_JS_CONTENT)
        with open(os.path.join(dest_dir, 'eslint.config.js'), 'w') as f:
            f.write(ESLINT_CONFIG_JS_CONTENT)
        
        # Create placeholder/empty files
        open(os.path.join(dest_public_dir, 'vite.svg'), 'w').close()
        with open(os.path.join(dest_src_dir, 'App.test.jsx'), 'w') as f:
            f.write("// Tests will be migrated for Vitest.")
        open(os.path.join(dest_src_dir, 'index.css'), 'w').close()
        print("✅ Vite configuration files created.")
    except IOError as e:
        print(f"\n❌ Error writing configuration files: {e}")
        sys.exit(1)


    # --- 3. File Extension and Content Transformation ---
    print("\n🔄 Transforming source files...")

    # Handle src/index.js separately
    original_index_js_path = os.path.join(source_src_dir, 'index.js')
    index_js_content = ""
    if os.path.exists(original_index_js_path):
        with open(original_index_js_path, 'r', encoding='utf-8') as f:
            index_js_content = f.read()
    else:
        print(f"   ⚠️ Warning: 'src/index.js' not found in source directory. Cannot generate 'main.jsx'.")
    
    # Process all other files in src/
    jsx_files_to_process = []
    for root, _, files in os.walk(source_src_dir):
        for filename in files:
            if filename == 'index.js':
                continue # Skip the original entry point

            source_path = os.path.join(root, filename)
            # Determine relative path to maintain sub-directory structure
            relative_path = os.path.relpath(source_path, source_src_dir)
            dest_path = os.path.join(dest_src_dir, relative_path)

            # Create subdirectories in destination if they don't exist
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            try:
                if filename.endswith('.js'):
                    dest_path = dest_path[:-3] + '.jsx'
                    shutil.copy2(source_path, dest_path)
                    jsx_files_to_process.append(dest_path)
                    print(f"   Copied and renamed: {filename} -> {os.path.basename(dest_path)}")
                else:
                    shutil.copy2(source_path, dest_path)
                    print(f"   Copied: {filename}")
            except Exception as e:
                print(f"   ❌ Error copying file {filename}: {e}")

    print("✅ File copying complete.")

    # --- 4. Gemini API Integration ---
    print("\n🧠 Using Gemini API for intelligent code transformation...")

    # Task 1: Update imports in all new .jsx files
    print("   TASK 1: Updating import statements in .jsx files...")
    import_update_prompt = (
        "Analyze the following JavaScript/JSX code. Your task is to update all relative import "
        "statements that point to other local JavaScript files. If an import path like './MyComponent' "
        "or './MyComponent.js' is found, change it to './MyComponent.jsx'. Do not modify imports from "
        "external libraries (e.g., 'react') or imports for non-JavaScript assets (e.g., './logo.svg', './App.css'). "
        "Return ONLY the modified code block, without any explanations or markdown formatting."
    )
    for file_path in jsx_files_to_process:
        try:
            with open(file_path, 'r+', encoding='utf-8') as f:
                original_code = f.read()
                print(f"      - Processing {os.path.basename(file_path)}...")
                updated_code = call_gemini_api(import_update_prompt, original_code)
                if updated_code:
                    f.seek(0)
                    f.write(updated_code)
                    f.truncate()
                else:
                    print(f"      - ⚠️ Failed to update imports for {os.path.basename(file_path)}. Skipping.")
        except Exception as e:
            print(f"      - ❌ Error processing file {file_path}: {e}")
    print("   ✅ Import update task complete.")

    # Task 2: Convert index.js to main.jsx
    print("\n   TASK 2: Converting CRA entry point to Vite's main.jsx...")
    main_jsx_prompt = (
    "You are an expert React migration assistant. Convert the following Create React App `index.js` "
    "code to be compatible with Vite's `main.jsx` format. Your output must be concise and follow modern best practices.\n"
    "The main requirements are:\n"
    "1. Replace `ReactDOM.render(...)` with the modern `ReactDOM.createRoot` API.\n"
    "2. The root rendering logic MUST be a single, chained statement: `createRoot(document.getElementById('root')).render(...)`.\n"
    "3. Ensure that if `React.StrictMode` is used, it is preserved within the render method.\n"
    "4. Update any relative component imports (e.g., `import App from './App'`) to use the `.jsx` extension (e.g., `import App from './App.jsx'`).\n"
    "5. Preserve all other imports, such as CSS imports (e.g., `import './index.css'`).\n\n"
    "For example, a typical output should look like this:\n"
    "```jsx\n"
    "import { StrictMode } from 'react';\n"
    "import { createRoot } from 'react-dom/client';\n"
    "import './index.css';\n"
    "import App from './App.jsx';\n\n"
    "createRoot(document.getElementById('root')).render(\n"
    "  <StrictMode>\n"
    "    <App />\n"
    "  </StrictMode>\n"
    ");\n"
    "```\n\n"
    "Now, convert the following code. Return ONLY the complete, new `main.jsx` code block, without any explanations or surrounding markdown."
    )
    if index_js_content:
        main_jsx_content = call_gemini_api(main_jsx_prompt, index_js_content)
        if main_jsx_content:
            try:
                main_jsx_path = os.path.join(dest_src_dir, 'main.jsx')
                with open(main_jsx_path, 'w', encoding='utf-8') as f:
                    f.write(main_jsx_content)
                print("   ✅ 'main.jsx' created successfully.")
            except IOError as e:
                print(f"   ❌ Error writing 'main.jsx': {e}")
        else:
            print("   ❌ Gemini API failed to generate content for 'main.jsx'.")
    else:
        print("   ⚠️ Skipped 'main.jsx' creation due to missing 'index.js'.")

    print("\n\n🎉 CONVERSION COMPLETE! 🎉")
    print("\nNext Steps:")
    print(f"1. Navigate to your new project: cd {dest_dir}")
    print("2. Install dependencies: npm install (or yarn, or pnpm)")
    print("3. Start the development server: npm run dev")
    print("\nNOTE: Please review the generated package.json and add any missing dependencies from your original project.")


if __name__ == "__main__":
    if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
        print("\n🛑 CRITICAL ERROR: Gemini API Key is not set!")
        print("   Please open the `convertor.py` script and replace 'YOUR_GEMINI_API_KEY' with your actual key.")
        sys.exit(1)
    main()
