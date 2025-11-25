' ═══════════════════════════════════════════════════════════
'   INSTALLEUR SULTAN AHMED - SANS CONSOLE
' ═══════════════════════════════════════════════════════════

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Chemin du dossier actuel
strPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Vérifier Python
Set objExec = objShell.Exec("python --version")
If objExec.ExitCode <> 0 Then
    MsgBox "Python n'est pas installé!" & vbCrLf & vbCrLf & _
           "Téléchargez-le depuis python.org", vbCritical, "Erreur"
    WScript.Quit
End If

' Installer les dépendances silencieusement
objShell.Run "cmd /c python -m pip install --quiet --disable-pip-version-check Pillow pywin32 winshell psutil mysql-connector-python python-dotenv", 0, True

' Trouver pythonw.exe
pythonw = "pythonw.exe"
pythonPath = objShell.ExpandEnvironmentStrings("%LocalAppData%") & "\Programs\Python\Python*\pythonw.exe"

' Lancer l'installeur SANS fenêtre (0 = invisible)
objShell.Run """" & pythonw & """ """ & strPath & "\install.py""", 0, False

Set objShell = Nothing
Set objFSO = Nothing