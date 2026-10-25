Procedure NativeProbe;
Var L : TStringList;
Begin
 L := TStringList.Create;
 Try
  L.Add('native_script_entry=verified');
  L.SaveToFile('D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_pcb_repair_20261023\ad18_native_research\native_probe_status.txt');
 Finally
  L.Free;
 End;
End;