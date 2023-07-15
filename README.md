# Subby - A Sub-goal Tracker App

This is a very simple sub-goal / project tracker app built with Python's flutter framework, Flet. It tracks goals based on its sub-goals, which itself have points that can be assigned to them based on their relative difficulties out of 10. A progress bar is shown for each goals based on the points achieved. There are Long-Term Goals mode and Weekly mode, with the only difference being the Weekly mode have a "Restart All Progress" button to be clicked when needed. Currently, Subby is only a desktop app as Flet doesn't seem to have support for mobile app yet, but the app is originally designed for mobile use.

## Libraries

The `main.py` python file uses both flet and datetime libraries. Furthermore, pyinstaller is needed to pack the app. Thus, you need to install them through the commands below to edit the python file.
```
pip install flet
pip install datetime
pip install pyinstaller
```

## Usage

The app needs to be packaged by running the command below while on the same directory as `main.py`.
```
flet pack main.py
```
This will create a `main.exe` file in `/dist` directory. Simply run the file to launch the app. Any data should be saved on client.
