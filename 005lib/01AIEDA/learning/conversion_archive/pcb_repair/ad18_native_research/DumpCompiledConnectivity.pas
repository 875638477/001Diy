{ Research draft, not yet run in AD18. Never saves design documents.
  Compile only an isolated source_copy project. Output is confined to this folder.
  API references are recorded in research_report.json. }

Function AuditField(S : String) : String;
Var
    I : Integer;
Begin
    Result := S;
    For I := 1 To Length(Result) Do
        If (Result[I] = #9) Or (Result[I] = #10) Or (Result[I] = #13) Then
            Result[I] := ' ';
End;

Procedure AuditProgress(S : String);
Var L : TStringList;
Begin
 L := TStringList.Create;
 Try
  L.Add(S);
  L.SaveToFile('D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_pcb_repair_20261023\ad18_native_research\native_progress.txt');
 Finally
  L.Free;
 End;
End;

Procedure DumpCompiledConnectivity;
Var
    Root, ProjectPath, Line, NetKey : String;
    Workspace : IWorkspace;
    Project : IProject;
    FlatDoc, Doc : IDocument;
    Net : INet;
    Comp : IComponent;
    Pin : INetItem;
    Nets, NetPins, Pins, Status : TStringList;
    D, C, P, N : Integer;
Begin
    AuditProgress('phase=script_entered');
    Root := 'D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_pcb_repair_20261023\ad18_native_research\';
    ProjectPath := Root + 'source_copy\lga1700.PrjPCB';
    If Not FileExists(ProjectPath) Then
    Begin
        ShowMessage('Isolated source_copy project is missing. Original AD project will not be opened.');
        Exit;
    End;
    Workspace := GetWorkspace;
    If Workspace = Nil Then Exit;
    Project := Workspace.DM_OpenProject(ProjectPath, False);
    If Project = Nil Then
    Begin
        ShowMessage('Cannot open the isolated AD project.');
        Exit;
    End;

    { Do not change project options, document contents, or source annotation. }
    AuditProgress('phase=project_opened');
    Project.DM_Compile;
    AuditProgress('phase=project_compiled');
    FlatDoc := Project.DM_DocumentFlattened;
    If FlatDoc = Nil Then
    Begin
        ShowMessage('Native compile did not provide a flattened document.');
        Exit;
    End;

    Nets := TStringList.Create;
    NetPins := TStringList.Create;
    Pins := TStringList.Create;
    Status := TStringList.Create;
    Try
        Nets.Add('net_index' + #9 + 'net_number' + #9 + 'net_name' + #9 + 'full_net_name' + #9 + 'pin_count' + #9 + 'label_count' + #9 + 'power_count' + #9 + 'port_count');
        NetPins.Add('net_index' + #9 + 'physical_ref' + #9 + 'logical_ref' + #9 + 'pin_number' + #9 + 'pin_name' + #9 + 'flattened_net_name' + #9 + 'item_net_number' + #9 + 'pin_unique_id');
        Pins.Add('document_index' + #9 + 'document' + #9 + 'component_index' + #9 + 'pin_index' + #9 + 'physical_ref' + #9 + 'logical_ref' + #9 + 'pin_number' + #9 + 'pin_name' + #9 + 'flattened_net_name' + #9 + 'item_net_number' + #9 + 'pin_unique_id');

        { Keep the native net index even when two distinct native nets have the same name. }
        For N := 0 To FlatDoc.DM_NetCount - 1 Do
        Begin
            Net := FlatDoc.DM_Nets(N);
            If Net <> Nil Then
            Begin
                NetKey := IntToStr(N);
                Nets.Add(NetKey + #9 + AuditField(Net.DM_NetNumber) + #9 + AuditField(Net.DM_NetName) + #9 + AuditField(Net.DM_FullNetName) + #9 + IntToStr(Net.DM_PinCount) + #9 + IntToStr(Net.DM_NetLabelCount) + #9 + IntToStr(Net.DM_PowerObjectCount) + #9 + IntToStr(Net.DM_PortCount));
                For P := 0 To Net.DM_PinCount - 1 Do
                Begin
                    Pin := Net.DM_Pins(P);
                    If Pin <> Nil Then
                        NetPins.Add(NetKey + #9 + AuditField(Pin.DM_PhysicalPartDesignator) + #9 + AuditField(Pin.DM_LogicalPartDesignator) + #9 + AuditField(Pin.DM_PinNumber) + #9 + AuditField(Pin.DM_PinName) + #9 + AuditField(Pin.DM_FlattenedNetName) + #9 + AuditField(Pin.DM_NetNumber) + #9 + AuditField(Pin.DM_FullUniqueId));
                End;
            End;
        End;

        { The complete pin census also records pins with no usable flattened net. }
        For D := 0 To Project.DM_PhysicalDocumentCount - 1 Do
        Begin
            Doc := Project.DM_PhysicalDocuments(D);
            If Doc <> Nil Then
            Begin
                For C := 0 To Doc.DM_ComponentCount - 1 Do
                Begin
                    Comp := Doc.DM_Components(C);
                    If Comp <> Nil Then
                    Begin
                        For P := 0 To Comp.DM_PinCount - 1 Do
                        Begin
                            Pin := Comp.DM_Pins(P);
                            If Pin <> Nil Then
                            Begin
                                Line := IntToStr(D) + #9 + AuditField(Doc.DM_FullPath) + #9 + IntToStr(C) + #9 + IntToStr(P);
                                Pins.Add(Line + #9 + AuditField(Pin.DM_PhysicalPartDesignator) + #9 + AuditField(Pin.DM_LogicalPartDesignator) + #9 + AuditField(Pin.DM_PinNumber) + #9 + AuditField(Pin.DM_PinName) + #9 + AuditField(Pin.DM_FlattenedNetName) + #9 + AuditField(Pin.DM_NetNumber) + #9 + AuditField(Pin.DM_FullUniqueId));
                            End;
                        End;
                    End;
                End;
            End;
        End;
        Nets.SaveToFile(Root + 'native_flat_nets.tsv');
        NetPins.SaveToFile(Root + 'native_flat_net_pins.tsv');
        Pins.SaveToFile(Root + 'native_all_pins.tsv');
        Status.Add('project=' + Project.DM_ProjectFullPath);
        Status.Add('native_net_count=' + IntToStr(FlatDoc.DM_NetCount));
        Status.Add('physical_document_count=' + IntToStr(Project.DM_PhysicalDocumentCount));
        Status.Add('violation_count=' + IntToStr(Project.DM_ViolationCount));
        Status.Add('status=export_completed_requires_diagnostic_review');
        Status.SaveToFile(Root + 'native_export_status.txt');
        AuditProgress('phase=export_completed');
    Finally
        Status.Free;
        Pins.Free;
        NetPins.Free;
        Nets.Free;
    End;
    { Deliberately leave AD open; never terminate a possible user session. }
End;
