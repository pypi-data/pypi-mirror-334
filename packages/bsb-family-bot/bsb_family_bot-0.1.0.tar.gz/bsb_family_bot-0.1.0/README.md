# bsb-family-bot
# BSB Family Bot

**BSB Family Bot** is a Python package that monitors various events on a device—such as new photos, text files, SMS messages, app installations, and new contacts—and sends notifications via a Telegram Bot.

## Features

- **New Photo Detection:** Monitors the device's camera directory (typically `/sdcard/DCIM/Camera`) for new photos.
- **New Text File Detection:** Monitors a specified directory (typically `/sdcard/Documents`) for new text files.
- **SMS Monitoring:** Uses the Termux API to list SMS messages and detect new messages.
- **App Installation Monitoring:** Monitors newly installed apps using the `pm list packages` command.
- **Contacts Monitoring:** Uses the Termux API to list contacts and detect new additions.

> **Note:**  
> This package is designed primarily for Termux/Android environments. SMS and Contacts monitoring require Termux API and proper permissions.

## Installation

```bash
pip install bsb-family-bot
