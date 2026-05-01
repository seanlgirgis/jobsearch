**Go To JobSearch Root**
```powershell
cd D:\Workarea\jobsearch
```

**Run Duplicate Check On Intake**
```powershell
.\job-chatgpt-check.ps1 "intake\intake.md"
```

**Accept Job And Create UUID + Folder Shell**
```powershell
.\job-chatgpt-accept.ps1
```

**Render Resume + Cover From Manual JSON Files**
```powershell
.\job-chatgpt-render.ps1
```

**Mark Application As Submitted On Dice**
```powershell
.\job-chatgpt-apply.ps1 -Method "Dice"
```