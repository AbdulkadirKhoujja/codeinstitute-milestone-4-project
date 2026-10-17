param(
    [string]$RuntimeDirectory = (Join-Path $env:LOCALAPPDATA 'SkillSeat\runtimes\python-3.13.16')
)

$ErrorActionPreference = 'Stop'
$packageUrl = 'https://api.nuget.org/v3-flatcontainer/python/3.13.16/python.3.13.16.nupkg'
$registrationUrl = 'https://api.nuget.org/v3/registration5-semver1/python/3.13.16.json'
New-Item -ItemType Directory -Path $RuntimeDirectory -Force | Out-Null
$registration = Invoke-RestMethod -Uri $registrationUrl
if ($registration.packageContent -ne $packageUrl -or
    $registration.catalogEntry -notlike 'https://api.nuget.org/v3/catalog0/data/*/python.3.13.16.json') {
    throw 'Unexpected NuGet registration metadata.'
}
$metadata = Invoke-RestMethod -Uri $registration.catalogEntry
if ($metadata.id -ne 'python' -or $metadata.version -ne '3.13.16' -or
    $metadata.authors -ne 'Python Software Foundation' -or
    $metadata.packageHashAlgorithm -ne 'SHA512') {
    throw 'Unexpected Python package identity or hash algorithm.'
}
$archive = Join-Path $RuntimeDirectory 'python.3.13.16.nupkg'
Invoke-WebRequest -Uri $packageUrl -OutFile $archive
$sha512 = [System.Security.Cryptography.SHA512]::Create()
try {
    $actualHash = [Convert]::ToBase64String($sha512.ComputeHash([IO.File]::ReadAllBytes($archive)))
} finally {
    $sha512.Dispose()
}
if ($actualHash -cne $metadata.packageHash) {
    throw 'NuGet SHA-512 mismatch. Package will not be extracted or executed.'
}
Write-Output "Verified NuGet SHA-512: $actualHash"
$metadata | ConvertTo-Json -Depth 20 | Set-Content (Join-Path $RuntimeDirectory 'catalog.json')
$packageDirectory = Join-Path $RuntimeDirectory 'package'
if (-not (Test-Path -LiteralPath $packageDirectory)) {
    Expand-Archive -LiteralPath $archive -DestinationPath $packageDirectory
}
$python = Join-Path $packageDirectory 'tools\python.exe'
& $python -c 'import sys; print(sys.version); print(sys.executable); assert sys.version_info[:3] == (3, 13, 16)'
if ($LASTEXITCODE -ne 0) { throw 'Python runtime verification failed.' }
Write-Output "Use this interpreter: $python"
