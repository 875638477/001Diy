Function VField(S : String) : String;
Var I : Integer;
Begin
 Result := S;
 For I := 1 To Length(Result) Do
  If (Result[I]=#9) Or (Result[I]=#10) Or (Result[I]=#13) Then Result[I] := ' ';
End;

Procedure DumpViolations;
Var W : IWorkspace;
    P : IProject;
    V : IViolation;
    L : TStringList;
    I : Integer;
    Root : String;
Begin
 Root := 'D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_pcb_repair_20261023\ad18_native_research\';
 W := GetWorkspace;
 If W=Nil Then Exit;
 P := W.DM_OpenProject(Root+'source_copy\lga1700.PrjPCB',False);
 If P=Nil Then Exit;
 L := TStringList.Create;
 Try
  L.Add('index'+#9+'error_level'+#9+'error_kind'+#9+'descriptor'+#9+'detail'+#9+'stage'+#9+'related_count');
  For I := 0 To P.DM_ViolationCount-1 Do
  Begin
   V := P.DM_Violations(I);
   If V<>Nil Then
    L.Add(IntToStr(I)+#9+IntToStr(Ord(V.DM_ErrorLevel))+#9+IntToStr(Ord(V.DM_ErrorKind))+#9+VField(V.DM_DescriptorString)+#9+VField(V.DM_DetailString)+#9+IntToStr(Ord(V.DM_CompilationStage))+#9+IntToStr(V.DM_RelatedObjectCount));
  End;
  L.SaveToFile(Root+'native_violations.tsv');
 Finally
  L.Free;
 End;
End;
