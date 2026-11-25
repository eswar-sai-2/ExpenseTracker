
[app]

# Application information
title = Expense Tracker
package.name = expensetracker
package.domain = com.saieswar
version = 0.1

# Source code
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_dirs = venv,.git,__pycache__,bin

# Python dependencies
requirements = python3,kivy,requests==2.27.1,charset-normalizer==2.1.1

# Application display settings
orientation = portrait
fullscreen = 0

# Android permissions
android.permissions = INTERNET

# Android architectures
android.archs = arm64-v8a, armeabi-v7a

# Android backup
android.allow_backup = True

# Python-for-Android configuration
p4a.branch = develop


[buildozer]

# Logging
log_level = 2
warn_on_root = 1
