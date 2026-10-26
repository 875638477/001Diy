from pathlib import Path
R=Path('D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025/tools/pcb_eco')
s=(R/'Invoke-NativeLocal.ps1').read_text(encoding='utf-8-sig')
s=s.replace('[string]$CompareBoard)', '[string]$CompareBoard,[Parameter(Mandatory=$true)][string]$TargetExpression)',1)
lines=s.splitlines()
idx=next(i for i,x in enumerate(lines) if x.startswith('[IO.File]::WriteAllLines($scr,'))
lines[idx]='''if(!$CompareBoard){throw 'Top-level second-design validation requires CompareBoard'}
[IO.File]::WriteAllLines($scr,@('set NOCONFIRM',('skill errset(load('+(S $script)+') t)'),('skill errset('+$Expression.Replace('{RUN}', $run.Replace('\\','/'))+' t)'),('edit '+(S $compareCopy)),('skill errset('+$TargetExpression.Replace('{RUN}', $run.Replace('\\','/'))+' t)'),'quit','fillin "yes"'),[Text.Encoding]::ASCII)'''
out=R/'Invoke-NativeTopLevel13.ps1';assert not out.exists();out.write_text('\n'.join(lines)+'\n',encoding='utf-8')