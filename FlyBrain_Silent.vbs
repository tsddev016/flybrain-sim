Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
dir = fso.GetParentFolderName(WScript.ScriptFullName)
sh.CurrentDirectory = dir
pyw = "pythonw """ & dir & "\FlyBrain.pyw"""
On Error Resume Next
sh.Run pyw, 1, False
If Err.Number <> 0 Then
  Err.Clear
  sh.Run "python """ & dir & "\main.py""", 1, False
End If
