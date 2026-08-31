@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title Hytale Turkce Ceviri Full - KLYC - Kurulum

echo ======================================================
echo   Hytale Turkce Ceviri Full  -  KLYC
echo   Kurulum (Windows)
echo ======================================================
echo.

set "BURASI=%~dp0"
set "APPSUP=%AppData%\Hytale"

if not exist "%APPSUP%" (
  echo [HATA] Hytale bulunamadi: %APPSUP%
  echo Once Hytale'i kur ve bir kez calistir.
  echo.
  pause
  exit /b 1
)

REM --- 1. Language klasorunu bul (en-US'in yaninda) ---
set "LANGDIR="
for /f "delims=" %%D in ('dir /s /b /ad "%APPSUP%\install\en-US" 2^>nul') do (
  set "LANGDIR=%%~dpD"
  set "LANGDIR=!LANGDIR:~0,-1!"
)
if not defined LANGDIR (
  echo [HATA] Oyunun dil klasoru bulunamadi.
  echo Hytale guncel mi ve bir kez calistirildi mi?
  echo.
  pause
  exit /b 1
)
echo Dil klasoru bulundu:
echo    %LANGDIR%
echo.

REM --- 2. Oyun ici ceviri (mod paketi) ---
echo [1/3] Oyun ici ceviri (mod paketi) kuruluyor...
set "MODS=%APPSUP%\UserData\Mods"
if not exist "%MODS%" mkdir "%MODS%"
del /q "%MODS%\KLYC-Turkce-Ceviri-v*.zip" 2>nul
del /q "%MODS%\Turkce-Ceviri-v*.zip" 2>nul
set "MODZIP="
for %%F in ("%BURASI%mod\KLYC-Turkce-Ceviri-v*.zip") do set "MODZIP=%%F"
if not defined MODZIP (
  echo [HATA] mod klasorunde ceviri paketi yok. Indirmeyi eksiksiz aldin mi?
  echo.
  pause
  exit /b 1
)
copy /y "!MODZIP!" "%MODS%\" >nul
for %%F in ("!MODZIP!") do echo    Kuruldu: %%~nxF
echo.

REM --- 3. Menu cevirisi ---
echo [2/3] Menu cevirisi uygulaniyor...
if not exist "%BURASI%menu\tr-TR\client.lang" (
  echo [HATA] menu\tr-TR\client.lang yok. Indirmeyi eksiksiz aldin mi?
  echo.
  pause
  exit /b 1
)
if exist "%LANGDIR%\tr-TR" rmdir /s /q "%LANGDIR%\tr-TR"
mkdir "%LANGDIR%\tr-TR"
copy /y "%BURASI%menu\tr-TR\client.lang" "%LANGDIR%\tr-TR\client.lang" >nul
copy /y "%BURASI%menu\tr-TR\meta.lang"   "%LANGDIR%\tr-TR\meta.lang" >nul
echo    tr-TR dil dosyalari eklendi.
echo    (Windows'ta yeniden imzalama gerekmiyor.)
echo.

REM --- 4. Oyun dilini tr-TR yap ---
echo [3/3] Dil ayari yapiliyor...
set "SET=%APPSUP%\UserData\Settings.json"
if exist "%SET%" (
  powershell -NoProfile -Command ^
    "try { $p='%SET%'; $j=Get-Content -Raw -Encoding UTF8 $p ^| ConvertFrom-Json; $j.Language='tr-TR'; ($j ^| ConvertTo-Json -Depth 20) ^| Set-Content -Encoding UTF8 $p } catch {}"
)
echo    Tamam.
echo.

echo ======================================================
echo   KURULUM TAMAM!
echo ======================================================
echo.
echo   - Oyunu tamamen kapat, launcher'dan yeniden ac.
echo   - Menu + oyun ici her sey Turkce olmali.
echo   - Menu Ingilizce ise: Ayarlar -^> Dil -^> Turkce.
echo.
echo   ONEMLI: Oyun guncellenirse menu cevirisi silinebilir.
echo   Guncellemeden sonra bu KUR-Windows.bat dosyasina tekrar cift tikla.
echo.
echo   Geri almak icin: KALDIR-Windows.bat
echo.
pause
