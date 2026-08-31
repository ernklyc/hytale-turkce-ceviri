#!/bin/bash
# Client'i orijinal (Hypixel imzali) haline dondurur
set -e
CLIENT="/Users/eren/Library/Application Support/Hytale/install/release/package/game/latest/Client"
YEDEK="/Users/eren/hytale-turkce-mod/_client_yedek/Client_v0.6.2_build25"
if [ ! -d "$YEDEK/Hytale.app" ]; then echo "YEDEK YOK: $YEDEK"; exit 1; fi
rm -rf "$CLIENT.bozuk" 2>/dev/null || true
mv "$CLIENT" "$CLIENT.bozuk"
cp -Rp "$YEDEK" "$CLIENT"
rm -rf "$CLIENT.bozuk"
codesign --verify --strict "$CLIENT/Hytale.app" && echo "GERI ALINDI - orijinal imza saglam"
