import os
from pathlib import Path

# فایل‌ها و پوشه‌هایی که نباید در خروجی نهایی بیایند
EXCLUDE_DIRS = {
    '.git', '__pycache__', 'migrations', 'staticfiles', 'media', 
    'venv', '.venv', 'env', '.pytest_cache', '.idea', '.vscode', '.html', 'node_modules',
    'tests', 'docs', 'build', 'dist', '.eggs', '.tox', '.mypy_cache', 'html document',
    'Markdown document', 'Vision', 'word', '.obsidian'
}
EXCLUDE_FILES = {
    'db.sqlite3', 'exporter.py', 'Pipfile.lock', 'poetry.lock', 
    '.DS_Store', 'manage.py'
}
ALLOWED_EXTENSIONS = {'.py', '.md', '.txt', '.ini', '.yaml', '.yml' }

def generate_tree(dir_path, prefix=""):
    """تولید ساختار درختی پروژه به صورت متنی"""
    tree_str = ""
    paths = sorted(list(Path(dir_path).iterdir()), key=lambda p: (p.is_file(), p.name))
    paths = [p for p in paths if p.name not in EXCLUDE_DIRS and p.name not in EXCLUDE_FILES]
    
    for i, path in enumerate(paths):
        is_last = (i == len(paths) - 1)
        connector = "└── " if is_last else "├── "
        if path.is_dir():
            tree_str += f"{prefix}{connector}{path.name}/\n"
            new_prefix = prefix + ("    " if is_last else "│   ")
            tree_str += generate_tree(path, new_prefix)
        else:
            if path.suffix in ALLOWED_EXTENSIONS:
                tree_str += f"{prefix}{connector}{path.name}\n"
    return tree_str

def export_project_to_markdown(output_file="Sina-Lalehbakhsh-Website.md"):
    root_dir = Path.cwd()
    markdown_content = []
    
    # ۱. بخش هدر و ساختار درختی
    markdown_content.append("# ACRON Project Export\n")
    markdown_content.append("## Project Structure\n```text")
    markdown_content.append(generate_tree(root_dir))
    markdown_content.append("```\n---\n")
    
    # ۲. استخراج کدهای نوشته شده
    markdown_content.append("## Source Code Files\n")
    
    for root, dirs, files in os.walk(root_dir):
        # فیلتر کردن پوشه‌های غیرمجاز
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in sorted(files):
            file_path = Path(root) / file
            if file in EXCLUDE_FILES or file_path.suffix not in ALLOWED_EXTENSIONS:
                continue
                
            relative_path = file_path.relative_to(root_dir)
            markdown_content.append(f"### File: `{relative_path}`")
            
            # تشخیص نوع زبان برای سینتکس هایلایت Markdown
            lang = "python" if file_path.suffix == ".py" else file_path.suffix[1:]
            markdown_content.append(f"```{lang}")
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    markdown_content.append(f.read())
            except Exception as e:
                markdown_content.append(f"# Error reading file: {e}")
                
            markdown_content.append("```\n")
            
    # ذخیره در فایل نهایی
    with open(output_file, "w", encoding="utf-8") as out:
        out.write("\n".join(markdown_content))
        
    print(f"🎉The project structure was successfully saved to the'{output_file}'file.")

if __name__ == "__main__":
    export_project_to_markdown()


