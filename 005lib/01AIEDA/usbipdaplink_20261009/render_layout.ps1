param([string]$InputJson,[string]$OutputPng,[string]$Title='Compact placement - native Allegro data')
Add-Type -AssemblyName System.Drawing
$layout = Get-Content -LiteralPath $InputJson -Raw | ConvertFrom-Json
$canvas = New-Object System.Drawing.Bitmap 1900,1100
$draw = [System.Drawing.Graphics]::FromImage($canvas)
$draw.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$draw.Clear([System.Drawing.Color]::FromArgb(18,23,29))
$scale=19.5
function lx([double]$value) { [single](55+($value+148)*$scale) }
function ly([double]$value) { [single](75+(10-$value)*$scale) }
$smallFont=New-Object System.Drawing.Font 'Consolas',7.5
$titleFont=New-Object System.Drawing.Font 'Consolas',16
$labelFont=New-Object System.Drawing.Font 'Consolas',10
$bodyPen=New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(220,208,187,85)),1
$boardPen=New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(130,225,150)),2
$pinBrush=New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(190,170,170,175))
$viaPen=New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(200,200,135)),1
$draw.DrawString($Title,$titleFont,[System.Drawing.Brushes]::White,35,18)
$draw.DrawString('TOP: red    BOTTOM: blue    P28 vertical / P29 horizontal    Type-C: right',$labelFont,[System.Drawing.Brushes]::LightGray,35,48)
$rect=$layout.board
$draw.FillRectangle((New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(17,75,90,65))),(lx $rect[0]),(ly $rect[3]),[single](($rect[2]-$rect[0])*$scale),[single](($rect[3]-$rect[1])*$scale))
$draw.DrawRectangle($boardPen,(lx $rect[0]),(ly $rect[3]),[single](($rect[2]-$rect[0])*$scale),[single](($rect[3]-$rect[1])*$scale))
foreach($line in $layout.geometry) {
  if($line.CLASS -eq 'ETCH' -and $line.GRAPHIC_DATA_NAME -eq 'LINE' -and $line.SUBCLASS -in @('TOP','BOTTOM')) {
    $color=[System.Drawing.Color]::FromArgb(195,220,85,75)
    if($line.SUBCLASS -eq 'BOTTOM'){$color=[System.Drawing.Color]::FromArgb(175,75,145,230)}
    $tracePen=New-Object System.Drawing.Pen $color,([single][Math]::Max(0.8,[double]$line.GRAPHIC_DATA_5*$scale))
    $draw.DrawLine($tracePen,(lx $line.GRAPHIC_DATA_1),(ly $line.GRAPHIC_DATA_2),(lx $line.GRAPHIC_DATA_3),(ly $line.GRAPHIC_DATA_4))
    $tracePen.Dispose()
  }
}
foreach($symbol in $layout.symbols) {
  $x1=[double]$symbol.SYM_BOX_X1; $x2=[double]$symbol.SYM_BOX_X2
  $y1=[double]$symbol.SYM_BOX_Y1; $y2=[double]$symbol.SYM_BOX_Y2
  $draw.DrawRectangle($bodyPen,(lx $x1),(ly $y2),[single](($x2-$x1)*$scale),[single](($y2-$y1)*$scale))
  $draw.DrawString($symbol.REFDES,$smallFont,[System.Drawing.Brushes]::White,(lx $symbol.SYM_X),(ly $symbol.SYM_Y))
}
foreach($pin in $layout.pins) {
  $draw.FillEllipse($pinBrush,[single]((lx $pin.PIN_X)-2),[single]((ly $pin.PIN_Y)-2),4,4)
}
$viaCoordinates=@{}
foreach($via in $layout.geometry) {
  if($via.CLASS -eq 'VIA CLASS' -and $via.SUBCLASS -eq 'TOP' -and $via.GRAPHIC_DATA_NAME -eq 'CIRCLE') {
    $key=$via.GRAPHIC_DATA_1+','+$via.GRAPHIC_DATA_2
    if(-not $viaCoordinates.ContainsKey($key)) {
      $viaCoordinates[$key]=$true
      $draw.DrawEllipse($viaPen,[single]((lx $via.GRAPHIC_DATA_1)-3),[single]((ly $via.GRAPHIC_DATA_2)-3),6,6)
    }
  }
}
$draw.DrawString(('Outline: {0:F1} x {1:F1} mm - placement review, no new routing' -f ($rect[2]-$rect[0]),($rect[3]-$rect[1])),$labelFont,[System.Drawing.Brushes]::LightGray,35,1055)
$canvas.Save([System.IO.Path]::GetFullPath($OutputPng),[System.Drawing.Imaging.ImageFormat]::Png)
$draw.Dispose(); $canvas.Dispose()
