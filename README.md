# Automated-Organizing-Download-Files

A personal background script designed to automatically clean up duplicate files and keep your Downloads folder organized.

## 🚀 Purpose

We've all been there: downloading the same file multiple times and ending up with a cluttered directory that requires manual sorting and deleting. This script runs quietly in the background to monitor your Downloads folder whenever a new file is added. 

If it detects an existing file with the same name, it automatically deletes the older version and keeps the newly downloaded one.

## ⚠️ Current Limitations & Roadmap

- **Name-Based Comparison:** Currently, the script only compares file names, not file contents. This means if two files have identical content but different names, the duplicate won't be caught. 
- **Next Steps:** I am actively working on implementing content-based hashing (such as MD5 or SHA-256) to handle files with different names but identical contents.
