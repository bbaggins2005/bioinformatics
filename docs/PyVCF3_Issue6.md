# Remediate [PyVCF3 Issue #6](https://github.com/dridk/PyVCF3/issues/6) 
<br><br>

## Description
When using PyVCF3 on newer versions of Python 3 (Python >= 3.11), users may get an error that states “TypeError: "quotechar" must be a 1-character string.” Three different methods can be used to remedy this problem, which are listed below.
<br><br>

## Methods
<!--ts-->
   * [Fixing with Linux](#Linux)
   * [Fixing with Windows](#Windows)
   * [Fixing with Github](#Github)
<!--te-->
<br></br>
### Linux
#### Grab version of PyVCF3
``` bash
PyVCF_version=$(pip show PyVCF3 | awk '/^Version:/{print $2}')
```
#### If PyVCF3 is version 1.0.3, then make correction
```bash
PyVCF_lib=$(pip show PyVCF3 | awk '/^Location:/{print $2}')
[ "${PyVCF_version}" == "1.0.3" ] && sed -i '/quotechar="",/d' ${PyVCF_lib}/vcf/parser.py
```
<br></br>
### Windows
#### Grab version of PyVCF3
``` powershell
$PyVCF_version = (pip show PyVCF3 | Select-String '^Version:' | ForEach-Object { $_.Line.Split(' ')[1] }).Trim()
```
#### If PyVCF3 is version 1.0.3, then make correction
``` powershell
if ($PyVCF_version -eq "1.0.3") {
$PyVCF_lib = (pip show PyVCF3 | Select-String '^Location:' | ForEach-Object { $_.Line.Split(' ')[1] }).Trim()
    $parserpy_path = Join-Path -Path $PyVCF_lib -ChildPath "vcf/parser.py"
    (Get-Content $parserpy_path) | Where-Object { $_ -notmatch 'quotechar="",' } | Set-Content $parserpy_path
}
```
<br></br>
### Github
Please reference the [PyVCF3 Github repository](https://github.com/dridk/PyVCF3) for implementation.