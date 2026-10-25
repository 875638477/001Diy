$ErrorActionPreference='Stop'
$repairRoot='D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_pcb_repair_20261023'
$ar=Join-Path $repairRoot 'xml_equivalence_audit'
$raw=Get-Content -LiteralPath (Join-Path $ar 'verification_raw.json') -Raw | ConvertFrom-Json
function Read-Audit($side,$file){Import-Csv -LiteralPath (Join-Path $ar "$side\$file") -Delimiter "`t"}
function Row-Key($row,[string[]]$columns){($columns|ForEach-Object{[string]$row.$_})-join "`t"}
function Same-Multiset($left,$right,[string[]]$columns){
 $dict=New-Object 'System.Collections.Generic.Dictionary[string,int]' ([StringComparer]::Ordinal)
 foreach($r in $left){$k=Row-Key $r $columns;if($dict.ContainsKey($k)){$dict[$k]++}else{$dict.Add($k,1)}}
 foreach($r in $right){$k=Row-Key $r $columns;if(-not $dict.ContainsKey($k)){return $false};$dict[$k]--}
 return (@($dict.Values|Where-Object{$_ -ne 0}).Count -eq 0)
}
$allowed=@{}
foreach($r in (Import-Csv -LiteralPath (Join-Path $repairRoot 'source_repaired\alias_repairs.tsv') -Delimiter "`t")){$allowed[($r.page+'|'+$r.name+'|'+$r.qualified_name)]=$true}
function Allowed-CacheRename($page,$old,$new){
 if($old -ceq $new){return $true}
 if($allowed.ContainsKey($page+'|'+$old+'|'+$new)){return $true}
 return ($page -ceq 'USB32 GEN1 5G_REAR' -and $old -ceq 'USB_PN6' -and $new -ceq 'GND')
}
$nameChanges=@();$nameErrors=@()
foreach($file in @('pins.tsv','wires.tsv','net_objects.tsv')){
 $columns=switch($file){'pins.tsv'{@('page','reference','full_reference','number','name','nc','x','y')};'wires.tsv'{@('page','points','object_type','line_style','line_width')};'net_objects.tsv'{@('page','kind','name','source_symbol','x','y','hot_x','hot_y','rotation','mirror')}}
 $bm=@{};foreach($r in (Read-Audit before $file)){$bm[(Row-Key $r $columns)]=$r}
 foreach($r in (Read-Audit after $file)){
  $key=Row-Key $r $columns
  if($bm.ContainsKey($key) -and $r.net -cne $bm[$key].net){
   $entry=[pscustomobject]@{file=$file;identity=$key;old=$bm[$key].net;new=$r.net}
   $nameChanges+=$entry
   if(-not (Allowed-CacheRename $r.page $bm[$key].net $r.net)){$nameErrors+=$entry}
  }
 }
}
$wb=@(Read-Audit before 'wires.tsv');$wa=@(Read-Audit after 'wires.tsv')
$first=@($wb|Where-Object{$_.page -ceq 'USB32 GEN1 5G_REAR' -and $_.points -ceq '496,854;606,854'})
$second=@($wb|Where-Object{$_.page -ceq 'USB32 GEN1 5G_REAR' -and $_.points -ceq '606,854;736,854'})
$merged=@($wa|Where-Object{$_.page -ceq 'USB32 GEN1 5G_REAR' -and $_.points -ceq '496,854;736,854'})
$oneMerge=($first.Count -eq 1 -and $second.Count -eq 1 -and $merged.Count -eq 1)
if($oneMerge){
 foreach($r in @($first[0],$second[0],$merged[0])){if($r.object_type -ne '20' -or $r.line_style -ne '0' -or $r.line_width -ne '0' -or $r.net -cne 'USB_PN6'){$oneMerge=$false}}
}
$normalizedWires=@()
foreach($r in $wb){
 if($r.page -ceq 'USB32 GEN1 5G_REAR' -and $r.points -ceq '606,854;736,854'){continue}
 if($r.page -ceq 'USB32 GEN1 5G_REAR' -and $r.points -ceq '496,854;606,854'){$r.points='496,854;736,854'}
 $normalizedWires+=$r
}
$wireGeometry=Same-Multiset $normalizedWires $wa @('page','points','object_type','line_style','line_width')
$ab=@(Read-Audit before 'aliases.tsv');$aa=@(Read-Audit after 'aliases.tsv')
$aliasIdentity=Same-Multiset $ab $aa @('page','name','x','y','rotation')
$ownerChanges=0
foreach($r in $ab){if($r.page -ceq 'USB32 GEN1 5G_REAR' -and $r.name -ceq 'USB_PN6' -and $r.wire_points -ceq '496,854;606,854'){$r.wire_points='496,854;736,854';$ownerChanges++}}
$aliasOwner=Same-Multiset $ab $aa @('page','name','x','y','rotation','wire_points')
$db=@(Read-Audit before 'design_properties.tsv'|Where-Object{-not($_.object -ceq 'design' -and $_.name -ceq 'Name')})
$da=@(Read-Audit after 'design_properties.tsv'|Where-Object{-not($_.object -ceq 'design' -and $_.name -ceq 'Name')})
$designProps=Same-Multiset $db $da @('object','name','value')
$required=@()
$required+=@($raw.checks|Where-Object{$_.file -eq 'instances.tsv' -and $_.columns.Count -eq 0})
$required+=@($raw.checks|Where-Object{$_.file -eq 'instance_trace_properties.tsv' -or $_.file -eq 'object_trace_properties.tsv' -or $_.file -eq 'page_object_counts.tsv'})
$required+=@($raw.checks|Where-Object{$_.file -eq 'pins.tsv' -and $_.columns.Count -gt 0})
$required+=@($raw.checks|Where-Object{$_.file -eq 'net_objects.tsv' -and $_.columns.Count -gt 0})
$pass=($required.Count -eq 6 -and @($required|Where-Object{-not $_.equal}).Count -eq 0 -and $oneMerge -and $wireGeometry -and $aliasIdentity -and $ownerChanges -eq 1 -and $aliasOwner -and $designProps -and $nameErrors.Count -eq 0)
$status=if($pass){'PASS_NATIVE_EQUIVALENCE_WITH_EXPECTED_CONNECTIVITY_REBUILD'}else{'REQUIRES_REVIEW'}
$final=[ordered]@{status=$status;counts=$raw.counts;exact_required_checks=$required;accepted_normalizations=[ordered]@{collinear_usb_wire_merge=$oneMerge;all_other_wire_geometry_equal=$wireGeometry;alias_identity_location_rotation_equal=$aliasIdentity;alias_owner_tracks_merged_wire=$aliasOwner;updated_alias_owners=$ownerChanges;network_cache_name_changes=$nameChanges;unplanned_name_change_count=$nameErrors.Count;unplanned_name_changes=$nameErrors;design_properties_equal_except_audit_copy_file_name=$designProps};native_export=$raw.run_result;source_hashes_unchanged=$raw.hashes_unchanged;raw_comparison_report='verification_raw.json';conclusion='All instance source package/part, value, footprint, geometry; all pin identity/geometry/NC; identifier names/hotspots/orientation; and1244 object plus1132 instance AD trace-property rows are retained. The only wire geometry difference is merging two collinear USB_PN6 segments. All net-text changes match the19-alias repair manifest or the23-pin USB GND separation. Independent AD-gold pin partitions remain a separate required validation.'}
$final|ConvertTo-Json -Depth 10|Set-Content -LiteralPath (Join-Path $ar 'final_verification.json') -Encoding UTF8
[pscustomobject]@{status=$status;required_checks=$required.Count;wire_merge=$oneMerge;wire_geometry=$wireGeometry;alias_geometry=$aliasIdentity;alias_owner=$aliasOwner;unplanned_net_name_changes=$nameErrors.Count;design_properties=$designProps;pin_name_changes=@($nameChanges|Where-Object file -eq 'pins.tsv').Count;wire_name_changes=@($nameChanges|Where-Object file -eq 'wires.tsv').Count;global_name_changes=@($nameChanges|Where-Object file -eq 'net_objects.tsv').Count}|ConvertTo-Json
