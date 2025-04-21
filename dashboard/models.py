from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from .helpers import generate_slug
from datetime import datetime
import os
import html2text
import subprocess
import base64


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    token = models.CharField(max_length=100)

class BlogModel(models.Model):
    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True)
    description = models.TextField(default="No Description")
    image = models.ImageField(upload_to='staticfiles/example')
    categories = models.JSONField(default=list)  # For simplicity, storing as JSON
    tags = models.JSONField(default=list)
    draft = models.BooleanField(default=False)
    content = RichTextField()
    file_directory = models.CharField(max_length=255, blank=True, editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Generate slug only if not already set
        if not self.slug:
            self.slug = generate_slug(self.title)

        # Set file directory if not already set
        if not self.file_directory:
            self.file_directory = os.path.join(
                'hugo-blog', 'themes', 'Niello', 'exampleSite', 'content', 'en', 'example1'
            )

        # Remove old markdown file if it exists (updating post)
        markdown_file_path = os.path.join(self.file_directory, f"{self.slug}.md")
        if os.path.exists(markdown_file_path):
            os.remove(markdown_file_path)

        super().save(*args, **kwargs)
        self.save_markdown()


    def save_markdown(self):
        folder = self.file_directory

        # Convert content to markdown
        converter = html2text.HTML2Text()
        converter.body_width = 0
        converter.images_as_html = False

        markdown_content = converter.handle(self.content)

        # Embed the image as base64
        try:
            with open(self.image.path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode('utf-8')
                data_url = f"data:image/png;base64,{encoded}"
        except Exception as e:
            print(f"Error reading image: {e}")
            data_url = ""

        # Build frontmatter
        frontmatter = f"""+++
title = "{self.title.replace('"', '\\"')}"
date = {datetime.now().isoformat()}
description = "{self.description.replace('\n', ' ')}"
categories = [{', '.join(f'"{cat}"' for cat in self.categories)}]
tags = [{', '.join(f'"{tag}"' for tag in self.tags)}]
draft = {str(self.draft).lower()}
+++
"""

        # Add image preview if available
        if data_url:
            frontmatter += f"![]({data_url})\n\n"

        # Combine everything
        full_markdown = frontmatter + markdown_content

        # Save markdown file
        markdown_file_path = os.path.join(folder, f"{self.slug}.md")
        try:
            with open(markdown_file_path, 'w', encoding='utf-8') as markdown_file:
                markdown_file.write(full_markdown)
        except Exception as e:
            print(f"Error writing markdown file: {e}")
            return

        # Git commit and push
        try:
            repo_path = os.path.abspath('hugo-blog')
            subprocess.run(['git', 'add', '.'], cwd=repo_path, check=True)
            subprocess.run(['git', 'commit', '-m', f'Add blog: {self.title}'], cwd=repo_path, check=True)
            subprocess.run(['git', 'push'], cwd=repo_path, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Git push failed: {e}")


    def delete(self, *args, **kwargs):
        # Delete the markdown file
        markdown_file_path = os.path.join('hugo-blog', 'themes', 'Niello', 'exampleSite', 'content', 'en','example1', f"{self.slug}.md")
        if os.path.exists(markdown_file_path):
            os.remove(markdown_file_path)
            try:
                repo_path = os.path.abspath('hugo-blog')  # Adjust if your repo root is different
                subprocess.run(['git', 'add', '.'], cwd=repo_path, check=True)
                subprocess.run(['git', 'commit', '-m', f'Add blog: {self.title}'], cwd=repo_path, check=True)
                subprocess.run(['git', 'push'], cwd=repo_path, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Git push failed: {e}")

        # Delete the image file
        if self.image and os.path.exists(self.image.path):
            os.remove(self.image.path)

        super().delete(*args, **kwargs)

    