Output views/preview.gif
Set FontSize 16
Set Width 1366
Set Height 900
Set Margin 30
Set Theme "Catppuccin Frappe"
Set WindowBar Colorful
Set MarginFill "#3b82f6"
Set BorderRadius 20
Set TypingSpeed 0ms
Set Shell bash

Hide

Type "source venv/bin/activate"
Enter
Type "export PS1='> '"
Enter

Wait />/

Type "clear"
Enter

Set TypingSpeed 90ms
Sleep 3s
Show

Type "docstr-health --pypi-package requests"
Enter

Wait />/
Sleep 3s

Set TypingSpeed 45ms
Type "docstr-health --repo-url https://github.com/django/django --compact"
Enter
Wait />/
Sleep 10s