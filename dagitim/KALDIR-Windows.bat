@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title Hytale Turkce Ceviri Full - KLYC - Kaldirma

echo ======================================================
echo   Hytale Turkce Ceviri Full - Kaldirma (Windows)
echo ======================================================
echo.

set "APPSUP=%AppData%\Hytale"
if not exist "%APPSUP%" ( echo [HATA] Hytale bulunamadi. & pause & exit /b 1 )

REM --- 1. Menu cevirisini kaldir (tr-TR klasorunu sil) ---
echo [1/3] Menu cevirisi kaldiriliyor...
set "LANGDIR="
for /f "delims=" %%D in ('dir /s /b /ad "%APPSUP%\install\en-US" 2^>nul') do (
  set "LANGDIR=%%~dpD"
  set "LANGDIR=!LANGDIR:~0,-1!"
)
if defined LANGDIR (
  if exist "!LANGDIR!\tr-TR" (
    rmdir /s /q "!LANGDIR!\tr-TR"
    echo    tr-TR dil klasoru silindi.
  ) else (
    echo    Zaten yok.
  )
) else (
  echo    Dil klasoru bulunamadi, atlaniyor.
)
echo.

REM --- 2. Mod paketini sil ---
echo [2/3] Mod paketi siliniyor...
del /q "%APPSUP%\UserData\Mods\KLYC-Turkce-Ceviri-v*.zip" 2>nul
del /q "%APPSUP%\UserData\Mods\Turkce-Ceviri-v*.zip" 2>nul
echo    Silindi.
echo.

REM --- 3. Dil ayarini sifirla ---
echo [3/3] Dil ayari sifirlaniyor...
set "SET=%APPSUP%\UserData\Settings.json"
if exist "%SET%" (
  powershell -NoProfile -Command ^
    "try { $p='%SET%'; $j=Get-Content -Raw -Encoding UTF8 $p ^| ConvertFrom-Json; if ($j.Language -eq 'tr-TR') { $j.Language=$null }; ($j ^| ConvertTo-Json -Depth 20) ^| Set-Content -Encoding UTF8 $p } catch {}"
)
echo    Tamam.
echo.

echo ======================================================
echo   KALDIRMA TAMAM. Oyunu kapat-ac.
echo ======================================================
echo.
echo   Not: Windows'ta oyun dosyasi degistirilmedigi icin
echo   (sadece tr-TR klasoru eklenmisti) geri alma temizdir.
echo   Gerekirse launcher'da Verify/Repair yapabilirsin.
echo.
pause
