Set shell = CreateObject("WScript.Shell")

cmd = "cmd /c " & _
      "cd /d C:\Users\martv\Documents\GitHub\RedditVideoMakerBot && " & _
      ".venv\Scripts\activate && " & _
      "python app.py && " & _
      "python check.py"

shell.Run cmd, 0, False
Set shell = Nothing
