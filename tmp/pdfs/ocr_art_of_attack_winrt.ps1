param([int]$Start=1,[int]$End=352,[string]$OutputSubdir='ocr/raw')
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null=[Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime]
$null=[Windows.Storage.Streams.IRandomAccessStream,Windows.Storage.Streams,ContentType=WindowsRuntime]
$null=[Windows.Graphics.Imaging.BitmapDecoder,Windows.Graphics.Imaging,ContentType=WindowsRuntime]
$null=[Windows.Graphics.Imaging.SoftwareBitmap,Windows.Graphics.Imaging,ContentType=WindowsRuntime]
$null=[Windows.Media.Ocr.OcrEngine,Windows.Foundation,ContentType=WindowsRuntime]
$null=[Windows.Globalization.Language,Windows.Globalization,ContentType=WindowsRuntime]
$ocrAwaitMethod=[System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {$_.Name -eq 'AsTask' -and $_.IsGenericMethod -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'} | Select-Object -First 1
function Await-OcrTask($Operation,[Type]$ResultType) {
    $task=$ocrAwaitMethod.MakeGenericMethod($ResultType).Invoke($null,@($Operation))
    $task.Wait()
    return $task.Result
}
$ocrRoot=Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$ocrBase=Join-Path $ocrRoot 'translations/art_of_attack'
$ocrOutput=Join-Path $ocrBase $OutputSubdir
[IO.Directory]::CreateDirectory($ocrOutput) | Out-Null
$ocrLanguage=New-Object Windows.Globalization.Language 'en-US'
$ocrEngine=[Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($ocrLanguage)
for($n=$Start;$n -le $End;$n++) {
    $dest=Join-Path $ocrOutput ('page-{0:000}.json' -f $n)
    if(Test-Path -LiteralPath $dest){continue}
    $watch=[Diagnostics.Stopwatch]::StartNew()
    $source=Join-Path $ocrBase ('source_pages/page-{0:000}.png' -f $n)
    $file=Await-OcrTask ([Windows.Storage.StorageFile]::GetFileFromPathAsync($source)) ([Windows.Storage.StorageFile])
    $stream=Await-OcrTask ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
    $decoder=Await-OcrTask ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
    $bitmap=Await-OcrTask ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
    $result=Await-OcrTask ($ocrEngine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
    $lines=@()
    foreach($line in $result.Lines) {
        $left=1e9;$top=1e9;$right=0;$bottom=0
        foreach($word in $line.Words) {
            $rect=$word.BoundingRect
            $left=[Math]::Min($left,$rect.X);$top=[Math]::Min($top,$rect.Y)
            $right=[Math]::Max($right,$rect.X+$rect.Width);$bottom=[Math]::Max($bottom,$rect.Y+$rect.Height)
        }
        $lines+=@{bbox=@($left,$top,$right,$bottom);text=$line.Text;confidence=$null}
    }
    $data=@{pdf_page=$n;printed_page=$(if($n -ge 3){$n}else{$null});width=$bitmap.PixelWidth;height=$bitmap.PixelHeight;engine='Windows OCR en-US';status='raw_ocr_not_manually_proofread';lines=$lines}
    [IO.File]::WriteAllText($dest,($data | ConvertTo-Json -Depth 8),(New-Object Text.UTF8Encoding $false))
    $bitmap.Dispose();$stream.Dispose()
    Write-Output ('OCR {0}: {1} lines, {2:N1}s' -f $n,$lines.Count,$watch.Elapsed.TotalSeconds)
}
