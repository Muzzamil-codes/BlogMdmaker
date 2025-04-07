from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from .helpers import generate_slug
from datetime import datetime
import os
import html2text


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
    image = models.ImageField(upload_to='exampleSite/static/example')
    caption = models.CharField(max_length=255, blank=True, null=True)
    categories = models.JSONField(default=list)  # For simplicity, storing as JSON
    tags = models.JSONField(default=list)
    draft = models.BooleanField(default=False)
    content = RichTextField()
    file_directory = models.CharField(max_length=255, blank=True, editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.file_directory:
            print(self.file_directory)
            os.remove(self.file_directory.strip())
            self.slug = generate_slug(self.title)
            self.file_directory = os.path.join('exampleSite', 'content', 'en','example1')
            super().save(*args, **kwargs)
            self.save_markdown()
        else:
            
            self.slug = generate_slug(self.title)
            self.file_directory = os.path.join('exampleSite', 'content', 'en','example1')
            
            super().save(*args, **kwargs)
            self.save_markdown()

    def save_markdown(self):
        # Get the year folder path
        folder = os.path.join('exampleSite', 'content', 'en','example1')

        # Convert content to markdown
        converter = html2text.HTML2Text()
        converter.body_width = 0
        converter.images_as_html = False

        markdown_content = converter.handle(self.content)
        markdown_content = markdown_content.replace('src="', 'src="/images/')

        # Build the markdown frontmatter
        frontmatter = f"""+++
title = "{self.title}"
date = {datetime.now().isoformat()}
description = {self.description}
image = images/{os.path.basename(self.image.name)}
caption = {self.caption or ''}
categories = [{','.join(self.categories)}]
tags = [{','.join(self.tags)}]
draft = {str(self.draft).lower()}
+++
"""

        # Combine frontmatter and markdown content
        full_markdown = frontmatter + markdown_content

        # Save markdown file
        markdown_file_path = os.path.join(folder, f"{self.slug}.md")
        with open(markdown_file_path, 'w', encoding='utf-8') as markdown_file:
            markdown_file.write(full_markdown)

    def delete(self, *args, **kwargs):
        # Delete the markdown file
        markdown_file_path = os.path.join('exampleSite', 'content', 'en','example1', f"{self.slug}.md")
        if os.path.exists(markdown_file_path):
            os.remove(markdown_file_path)

        # Delete the image file
        if self.image and os.path.exists(self.image.path):
            os.remove(self.image.path)

        super().delete(*args, **kwargs)

    