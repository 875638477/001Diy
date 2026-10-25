param([Parameter(Mandatory=$true)][string]$DataFile,[Parameter(Mandatory=$true)][string]$OutputFile)
$taskRoot=[IO.Path]::GetFullPath('D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
$target=[IO.Path]::GetFullPath($OutputFile)
if(-not $target.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Output outside task directory'}
Add-Type -AssemblyName System.Drawing
$inputData=Get-Content -LiteralPath $DataFile -Raw -Encoding UTF8 | ConvertFrom-Json
$scale=20.0
function XY($point){[Drawing.PointF]::new([single](20+$scale*$point[0]),[single](1260-$scale*$point[1]))}
function RingPoints($ring){[Drawing.PointF[]]@(foreach($pt in $ring){XY $pt})}
$bitmap=[Drawing.Bitmap]::new(1640,1300)
$gr=[Drawing.Graphics]::FromImage($bitmap)
$gr.SmoothingMode=[Drawing.Drawing2D.SmoothingMode]::AntiAlias
$gr.Clear([Drawing.Color]::FromArgb(248,248,241))
$board=[Drawing.PointF[]]@(XY @(2,0);XY @(78,0);XY @(80,2);XY @(80,58);XY @(78,60);XY @(2,60);XY @(0,58);XY @(0,2))
$boardBrush=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(231,224,207));$gr.FillPolygon($boardBrush,$board);$boardBrush.Dispose()
$planeBrush=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(52,40,142,92))
foreach($poly in $inputData.planes){$path=[Drawing.Drawing2D.GraphicsPath]::new([Drawing.Drawing2D.FillMode]::Alternate);$path.AddPolygon((RingPoints $poly.outer));foreach($hole in $poly.holes){$path.AddPolygon((RingPoints $hole))};$gr.FillPath($planeBrush,$path);$path.Dispose()};$planeBrush.Dispose()
$bodyPen=[Drawing.Pen]::new([Drawing.Color]::FromArgb(130,100,100,100),.6)
foreach($b in $inputData.bodies){if($b.bbox){$bb=$b.bbox;$gr.DrawRectangle($bodyPen,[single](20+$scale*$bb[0][0]),[single](1260-$scale*$bb[1][1]),[single]($scale*($bb[1][0]-$bb[0][0])),[single]($scale*($bb[1][1]-$bb[0][1])))}};$bodyPen.Dispose()
$padBrush=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(200,179,80))
foreach($q in $inputData.pads){$bb=$q.bbox;$gr.FillRectangle($padBrush,[single](20+$scale*$bb[0][0]),[single](1260-$scale*$bb[1][1]),[single]($scale*($bb[1][0]-$bb[0][0])),[single]($scale*($bb[1][1]-$bb[0][1])))};$padBrush.Dispose()
$colors=@{GND='#418d6a';V3V3='#c32d92';V5='#dc7926';BUCK_SW='#db270c';BUCK_BOOT='#dc691b';BUCK_FB='#ad592d';USB_DP='#d024d0';USB_DM='#256ed8';PA12_SHARED='#c62a95';PA11_SHARED='#2992c0';ADC_IN='#0095a2';NRST='#a555c4'}
foreach($q in $inputData.routes){if(-not $q.width -or $q.points.Count -lt 2){continue};$c=if($colors.ContainsKey($q.net)){$colors[$q.net]}elseif($q.layer -eq 'TOP'){'#ae443d'}else{'#3777b2'};$pen=[Drawing.Pen]::new([Drawing.ColorTranslator]::FromHtml($c),[single]($scale*$q.width));$pen.StartCap=[Drawing.Drawing2D.LineCap]::Round;$pen.EndCap=[Drawing.Drawing2D.LineCap]::Round;$pen.LineJoin=[Drawing.Drawing2D.LineJoin]::Round;$gr.DrawLines($pen,(RingPoints $q.points));$pen.Dispose()}
$viaBrush=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(170,146,65));$holeBrush=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(248,248,241))
foreach($v in $inputData.vias){$pt=XY $v.xy;$r=$scale*$v.radius;$hr=$scale*$v.drill/2;$gr.FillEllipse($viaBrush,[single]($pt.X-$r),[single]($pt.Y-$r),[single](2*$r),[single](2*$r));$gr.FillEllipse($holeBrush,[single]($pt.X-$hr),[single]($pt.Y-$hr),[single](2*$hr),[single](2*$hr))}
foreach($p in @(@(5,5),@(75,5),@(75,55),@(5,55))){$pt=XY $p;$gr.FillEllipse($holeBrush,[single]($pt.X-20),[single]($pt.Y-20),40,40)}
$viaBrush.Dispose();$holeBrush.Dispose()
$font=[Drawing.Font]::new('Arial',9);$textBrush=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(45,45,45));foreach($b in $inputData.bodies){$pt=XY $b.xy;$gr.DrawString($b.ref,$font,$textBrush,[single]($pt.X+2),[single]($pt.Y-14))};$font.Dispose()
$titleFont=[Drawing.Font]::new('Arial',14);$gr.DrawString($inputData.label,$titleFont,$textBrush,20,10);$titleFont.Dispose();$textBrush.Dispose()
$bitmap.Save($target,[Drawing.Imaging.ImageFormat]::Png);$gr.Dispose();$bitmap.Dispose();Write-Output $target
