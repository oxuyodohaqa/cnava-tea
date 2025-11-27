#!/usr/bin/env python3
"""
SHEERID ID CARD GENERATOR - ULTRA MEGA FAST - 2000+ IDs/MIN ⚡⚡⚡⚡⚡
✅ EXACT NAMES: Zero modifications to college names from JSON
✅ CURRENT DATES: Within 90 days for SheerID verification
✅ SIMPLE FORMAT: Clean layout like STU36259874.png
✅ SAME FORMAT: STUDENTID_COLLEGEID.png + students.txt
✅ 24 COUNTRIES: US, CA, GB, IN, ID, AU, DE, FR, ES, IT, BR, MX, NL, SE, NO, DK, JP, KR, SG, NZ, ZA, CN, AE, PH
✅ ENGLISH NAMES ONLY: Always generates English student names
✅ ULTRA MEGA FAST: 5000 workers, 250 sessions, 1000 batch, photo cache, aggressive optimization
Updated: 2025-11-11 19:29:07 UTC
User: Adeebaabkhan
Target: 2000+ IDs per minute (10K in 5 minutes)
"""

import sys
import os
import re
import logging
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import requests
from faker import Faker
import qrcode
import random
import json
from datetime import datetime, timedelta, timezone
from io import BytesIO
import time
import concurrent.futures
import threading
from functools import lru_cache
import gc


# --- Logging & Helpers (match b.py style) ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def clean_name(name: str) -> str:
    """Membersihkan nama dari gelar dan karakter yang tidak diinginkan (konsisten dengan b.py)."""

    name = re.sub(r"[.,]", "", name)
    name = re.sub(r"\b(Drs?|Ir|H|Prof|S|M|Bapak|Ibu)\b", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\s+", " ", name).strip()
    return name

# ==================== CONFIGURATION ====================
COUNTRY_CONFIG = {
    'US': {
        'name': 'United States',
        'code': 'us',
        'locale': 'en-us',
        'collegeFile': 'sheerid_us.json',
        'currency': 'USD',
        'currency_symbol': '$',
        'academic_terms': ['Fall 2024', 'Spring 2025', 'Summer 2024'],
        'flag': '🇺🇸'
    },
    'CA': {
        'name': 'Canada',
        'code': 'ca',
        'locale': 'en-ca',
        'collegeFile': 'sheerid_ca.json',
        'currency': 'CAD',
        'currency_symbol': '$',
        'academic_terms': ['Fall 2024', 'Winter 2025', 'Summer 2024'],
        'flag': '🇨🇦'
    },
    'GB': {
        'name': 'United Kingdom',
        'code': 'gb',
        'locale': 'en-gb',
        'collegeFile': 'sheerid_gb.json',
        'currency': 'GBP',
        'currency_symbol': '£',
        'academic_terms': ['Autumn 2024', 'Spring 2025', 'Summer 2024'],
        'flag': '🇬🇧'
    },
    'IN': {
        'name': 'India',
        'code': 'in',
        'locale': 'en-in',
        'collegeFile': 'sheerid_in.json',
        'currency': 'INR',
        'currency_symbol': '₹',
        'academic_terms': ['Monsoon 2024', 'Winter 2025', 'Summer 2024'],
        'flag': '🇮🇳'
    },
    'ID': {
        'name': 'Indonesia',
        'code': 'id',
        'locale': 'id-id',
        'collegeFile': 'sheerid_id.json',
        'currency': 'IDR',
        'currency_symbol': 'Rp',
        'academic_terms': ['Semester 1 2024', 'Semester 2 2025', 'Summer 2024'],
        'flag': '🇮🇩'
    },
    'AU': {
        'name': 'Australia',
        'code': 'au',
        'locale': 'en-au',
        'collegeFile': 'sheerid_au.json',
        'currency': 'AUD',
        'currency_symbol': '$',
        'academic_terms': ['Semester 1 2024', 'Semester 2 2025', 'Summer 2024'],
        'flag': '🇦🇺'
    },
    'DE': {
        'name': 'Germany',
        'code': 'de',
        'locale': 'de-de',
        'collegeFile': 'sheerid_de.json',
        'currency': 'EUR',
        'currency_symbol': '€',
        'academic_terms': ['Wintersemester 2024', 'Sommersemester 2025'],
        'flag': '🇩🇪'
    },
    'FR': {
        'name': 'France',
        'code': 'fr',
        'locale': 'fr-fr',
        'collegeFile': 'sheerid_fr.json',
        'currency': 'EUR',
        'currency_symbol': '€',
        'academic_terms': ['Semestre 1 2024', 'Semestre 2 2025'],
        'flag': '🇫🇷'
    },
    'ES': {
        'name': 'Spain',
        'code': 'es',
        'locale': 'es-es',
        'collegeFile': 'sheerid_es.json',
        'currency': 'EUR',
        'currency_symbol': '€',
        'academic_terms': ['Primer Semestre 2024', 'Segundo Semestre 2025'],
        'flag': '🇪🇸'
    },
    'IT': {
        'name': 'Italy',
        'code': 'it',
        'locale': 'it-it',
        'collegeFile': 'sheerid_it.json',
        'currency': 'EUR',
        'currency_symbol': '€',
        'academic_terms': ['Primo Semestre 2024', 'Secondo Semestre 2025'],
        'flag': '🇮🇹'
    },
    'BR': {
        'name': 'Brazil',
        'code': 'br',
        'locale': 'pt-br',
        'collegeFile': 'sheerid_br.json',
        'currency': 'BRL',
        'currency_symbol': 'R$',
        'academic_terms': ['Semestre 1 2024', 'Semestre 2 2025'],
        'flag': '🇧🇷'
    },
    'MX': {
        'name': 'Mexico',
        'code': 'mx',
        'locale': 'es-mx',
        'collegeFile': 'sheerid_mx.json',
        'currency': 'MXN',
        'currency_symbol': '$',
        'academic_terms': ['Semestre 1 2024', 'Semestre 2 2025'],
        'flag': '🇲🇽'
    },
    'NL': {
        'name': 'Netherlands',
        'code': 'nl',
        'locale': 'nl-nl',
        'collegeFile': 'sheerid_nl.json',
        'currency': 'EUR',
        'currency_symbol': '€',
        'academic_terms': ['Semester 1 2024', 'Semester 2 2025'],
        'flag': '🇳🇱'
    },
    'SE': {
        'name': 'Sweden',
        'code': 'se',
        'locale': 'sv-se',
        'collegeFile': 'sheerid_se.json',
        'currency': 'SEK',
        'currency_symbol': 'kr',
        'academic_terms': ['Hösttermin 2024', 'Vårtermin 2025'],
        'flag': '🇸🇪'
    },
    'NO': {
        'name': 'Norway',
        'code': 'no',
        'locale': 'no-no',
        'collegeFile': 'sheerid_no.json',
        'currency': 'NOK',
        'currency_symbol': 'kr',
        'academic_terms': ['Høstsemester 2024', 'Vårsemester 2025'],
        'flag': '🇳🇴'
    },
    'DK': {
        'name': 'Denmark',
        'code': 'dk',
        'locale': 'da-dk',
        'collegeFile': 'sheerid_dk.json',
        'currency': 'DKK',
        'currency_symbol': 'kr',
        'academic_terms': ['Efterårssemester 2024', 'Forårssemester 2025'],
        'flag': '🇩🇰'
    },
    'JP': {
        'name': 'Japan',
        'code': 'jp',
        'locale': 'ja-jp',
        'collegeFile': 'sheerid_jp.json',
        'currency': 'JPY',
        'currency_symbol': '¥',
        'academic_terms': ['Spring 2024', 'Fall 2024'],
        'flag': '🇯🇵'
    },
    'KR': {
        'name': 'South Korea',
        'code': 'kr',
        'locale': 'ko-kr',
        'collegeFile': 'sheerid_kr.json',
        'currency': 'KRW',
        'currency_symbol': '₩',
        'academic_terms': ['Spring 2024', 'Fall 2024'],
        'flag': '🇰🇷'
    },
    'SG': {
        'name': 'Singapore',
        'code': 'sg',
        'locale': 'en-sg',
        'collegeFile': 'sheerid_sg.json',
        'currency': 'SGD',
        'currency_symbol': '$',
        'academic_terms': ['Semester 1 2024', 'Semester 2 2025'],
        'flag': '🇸🇬'
    },
    'NZ': {
        'name': 'New Zealand',
        'code': 'nz',
        'locale': 'en-nz',
        'collegeFile': 'sheerid_nz.json',
        'currency': 'NZD',
        'currency_symbol': '$',
        'academic_terms': ['Semester 1 2024', 'Semester 2 2025'],
        'flag': '🇳🇿'
    },
    'ZA': {
        'name': 'South Africa',
        'code': 'za',
        'locale': 'en-za',
        'collegeFile': 'sheerid_za.json',
        'currency': 'ZAR',
        'currency_symbol': 'R',
        'academic_terms': ['First Semester 2024', 'Second Semester 2025'],
        'flag': '🇿🇦'
    },
    'CN': {
        'name': 'China',
        'code': 'cn',
        'locale': 'zh-cn',
        'collegeFile': 'sheerid_cn.json',
        'currency': 'CNY',
        'currency_symbol': '¥',
        'academic_terms': ['Spring 2024', 'Fall 2024'],
        'flag': '🇨🇳'
    },
    'AE': {
        'name': 'UAE',
        'code': 'ae',
        'locale': 'en-ae',
        'collegeFile': 'sheerid_ae.json',
        'currency': 'AED',
        'currency_symbol': 'د.إ',
        'academic_terms': ['Fall 2024', 'Spring 2025'],
        'flag': '🇦🇪'
    },
    'PH': {
        'name': 'Philippines',
        'code': 'ph',
        'locale': 'en-ph',
        'collegeFile': 'sheerid_ph.json',
        'currency': 'PHP',
        'currency_symbol': '₱',
        'academic_terms': ['First Semester 2024-2025', 'Second Semester 2024-2025', 'Summer 2024'],
        'flag': '🇵🇭'
    }
}

class UnlimitedIDCardGenerator:
    def __init__(self):
        self.receipts_dir = "receipts"
        self.students_file = "students.txt"
        self.selected_country = None
        self.all_colleges = []
        self.colleges_lock = threading.Lock()
        
        self.faker_instances = []
        self.faker_lock = threading.Lock()
        self.faker_index = 0
        self.file_save_lock = threading.Lock()
        
        # ⚡⚡⚡⚡⚡ ULTRA MEGA FAST SETTINGS - 2000+ IDs/MIN
        self.max_workers = 5000  # Increased from 3000
        self.memory_cleanup_interval = 5000  # Reduced cleanup frequency
        
        # ⚡ MEGA BATCH FILE WRITES
        self.student_buffer = []
        self.buffer_size = 1000  # Increased from 500
        
        # Remove photo cache and related functionality
        self.photo_cache = []
        self.photo_cache_lock = threading.Lock()
        self.photo_cache_size = 0
        
        # Remove sessions as they're no longer needed for photo downloads
        self.sessions = []
        
        self.stats = {
            "ids_generated": 0,
            "photos_downloaded": 0,
            "photo_retries": 0,
            "students_saved": 0,
            "start_time": None
        }
        
        self.colors = {
            "blue": "#1e3a8a",
            "light_blue": "#dbeafe",
            "dark_blue": "#1e40af",
            "white": "#ffffff",
            "black": "#000000",
            "gray": "#6b7280",
        }

        # Reuse the same background image that b.py relies on
        self.template_path = Path(__file__).parent / "mentahan.jpg"
        
        # ⚡ CACHE CURRENT YEAR
        self.current_year = datetime.now(timezone.utc).year
        
        # Font configuration to match b.py exactly
        self.font_path = Path(__file__).parent / "PlayfairDisplay-VariableFont_wght.ttf"
        self.font_size = 50
        self.text_color = "#051d40"
        self.center_x = 675  # Same as b.py
        self.pos_y = 200    # Same as b.py
        self.bg_padding_x = 50  # Same as b.py
        self.bg_padding_y = 35  # Same as b.py
        
        # College name position (similar to b.py but for university name)
        self.college_font_size = 40
        self.college_pos_y = 100
        self.college_bg_padding_x = 40
        self.college_bg_padding_y = 25
        
        self.create_directories()
        self.clear_all_data()
        self.fonts = self.load_fonts()

    def create_directories(self):
        os.makedirs(self.receipts_dir, exist_ok=True)

    def clear_all_data(self):
        try:
            if os.path.exists(self.receipts_dir):
                for f in os.listdir(self.receipts_dir):
                    if f.endswith(('.png', '.jpg')):
                        try:
                            os.remove(os.path.join(self.receipts_dir, f))
                        except:
                            pass
            if os.path.exists(self.students_file):
                try:
                    os.remove(self.students_file)
                except:
                    pass
            
            print("🗑️  All data cleared!")
            print(f"✅ EXACT NAMES: Uses JSON college names as-is")
            print(f"✅ ENGLISH NAMES: Only English student names")
            print(f"✅ SHEERID READY: Dates within 90 days")
            print(f"✅ SIMPLE FORMAT: Clean layout like STU36259874.png")
            print(f"✅ FORMAT: STUDENTID_COLLEGEID.png")
            print(f"✅ SAVE: students.txt + receipts/")
            print(f"✅ 24 COUNTRIES: Full global support")
            print(f"⚡⚡⚡⚡⚡ ULTRA MEGA FAST: 5000 workers")
            print(f"⚡⚡⚡⚡⚡ TARGET: 2000+ IDs per minute (10K in 5 min)")
            print("="*70)
        except Exception as e:
            print(f"⚠️  Warning: {e}")

    def load_colleges(self):
        try:
            if not self.selected_country:
                return []
            
            config = COUNTRY_CONFIG[self.selected_country]
            college_file = config['collegeFile']
            
            print(f"\n📚 Loading {college_file}...")
            
            if not os.path.exists(college_file):
                print(f"❌ ERROR: {college_file} not found!")
                return []
            
            with open(college_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            colleges = []
            for c in data:
                if (c.get('name') and c.get('id') and
                    c.get('type') in ['UNIVERSITY', 'COLLEGE', 'HEI', 'POST_SECONDARY']):
                    colleges.append({
                        'name': c['name'],
                        'id': c['id'],
                        'type': c['type']
                    })
            
            if not colleges:
                print(f"❌ No valid colleges!")
                return []
            
            print(f"✅ Loaded {len(colleges)} colleges")
            print(f"✅ Names stored EXACTLY as in JSON (no modifications)")
            print(f"✅ ENGLISH NAMES: Only English student names")
            print(f"✅ UNLIMITED mode: Colleges can be reused")
            
            return colleges
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return []

    def select_country_and_load(self):
        print("\n🌍 COUNTRY SELECTION - 24 COUNTRIES AVAILABLE")
        print("=" * 70)
        print("1 . United States        (US) | 2 . Canada               (CA)")
        print("3 . United Kingdom       (GB) | 4 . India                (IN)")
        print("5 . Indonesia            (ID) | 6 . Australia            (AU)")
        print("7 . Germany              (DE) | 8 . France               (FR)")
        print("9 . Spain                (ES) | 10. Italy                (IT)")
        print("11. Brazil               (BR) | 12. Mexico               (MX)")
        print("13. Netherlands          (NL) | 14. Sweden               (SE)")
        print("15. Norway               (NO) | 16. Denmark              (DK)")
        print("17. Japan                (JP) | 18. South Korea          (KR)")
        print("19. Singapore            (SG) | 20. New Zealand          (NZ)")
        print("21. South Africa         (ZA) | 22. China                (CN)")
        print("23. UAE                  (AE) | 24. Philippines          (PH)")
        print("=" * 70)
        
        country_map = {
            '1': 'US', '2': 'CA', '3': 'GB', '4': 'IN',
            '5': 'ID', '6': 'AU', '7': 'DE', '8': 'FR',
            '9': 'ES', '10': 'IT', '11': 'BR', '12': 'MX',
            '13': 'NL', '14': 'SE', '15': 'NO', '16': 'DK',
            '17': 'JP', '18': 'KR', '19': 'SG', '20': 'NZ',
            '21': 'ZA', '22': 'CN', '23': 'AE', '24': 'PH'
        }
        
        while True:
            choice = input("\nSelect country (1-24): ").strip()
            if choice in country_map:
                self.selected_country = country_map[choice]
                break
            else:
                print("❌ Enter a number between 1 and 24")
        
        config = COUNTRY_CONFIG[self.selected_country]
        print(f"\n✅ Selected: {config['flag']} {config['name']} ({self.selected_country})")
        
        self.all_colleges = self.load_colleges()
        
        if not self.all_colleges:
            print("❌ No colleges!")
            return False
        
        # ALWAYS USE ENGLISH FAKER REGARDLESS OF COUNTRY
        print("✅ Using English names only for all students")
        try:
            self.faker_instances = [Faker('en_US') for _ in range(200)]  # Always English
        except:
            self.faker_instances = [Faker('en_US') for _ in range(200)]  # Fallback
        
        print(f"✅ Generator ready!")
        
        return True

    @lru_cache(maxsize=1)
    def load_fonts(self):
        try:
            if self.font_path.exists():
                return {
                    'title': ImageFont.truetype(str(self.font_path), 64),
                    'header': ImageFont.truetype(str(self.font_path), 50),
                    'name': ImageFont.truetype(str(self.font_path), 54),
                    'normal': ImageFont.truetype(str(self.font_path), 28),
                    'small': ImageFont.truetype(str(self.font_path), 20),
                    'bold': ImageFont.truetype(str(self.font_path), 32),
                }

            if os.name == 'nt':
                return {
                    'title': ImageFont.truetype("arialbd.ttf", 24),
                    'header': ImageFont.truetype("arialbd.ttf", 18),
                    'name': ImageFont.truetype("arialbd.ttf", 20),
                    'normal': ImageFont.truetype("arial.ttf", 14),
                    'small': ImageFont.truetype("arial.ttf", 12),
                    'bold': ImageFont.truetype("arialbd.ttf", 14),
                }

            return {k: ImageFont.load_default() for k in ['title', 'header', 'name', 'normal', 'small', 'bold']}
        except Exception as exc:
            logger.warning("Falling back to default fonts due to: %s", exc)
            return {k: ImageFont.load_default() for k in ['title', 'header', 'name', 'normal', 'small', 'bold']}

    def get_faker(self):
        with self.faker_lock:
            faker = self.faker_instances[self.faker_index]
            self.faker_index = (self.faker_index + 1) % len(self.faker_instances)
            return faker

    def create_simple_photo(self):
        """Create a simple placeholder photo"""
        photo = Image.new("RGB", (120, 150), self.colors["light_blue"])
        draw = ImageDraw.Draw(photo)
        
        # Simple face placeholder
        draw.ellipse([30, 20, 90, 80], outline=self.colors["blue"], width=2)
        draw.ellipse([45, 40, 55, 50], fill=self.colors["blue"])  # Left eye
        draw.ellipse([65, 40, 75, 50], fill=self.colors["blue"])  # Right eye
        draw.arc([45, 55, 75, 70], 0, 180, fill=self.colors["blue"], width=2)
        
        draw.text((60, 110), "STUDENT\nPHOTO", 
                 fill=self.colors["blue"], font=self.fonts['small'], anchor="mm")
        
        return photo

    def select_random_college(self):
        with self.colleges_lock:
            if not self.all_colleges:
                return None
            return random.choice(self.all_colleges)

    def generate_student_data(self, college):
        fake = self.get_faker()
        config = COUNTRY_CONFIG[self.selected_country]

        # ALWAYS GENERATE ENGLISH NAMES REGARDLESS OF COUNTRY
        first_name = fake.first_name()
        last_name = fake.last_name()
        full_name = clean_name(f"{first_name} {last_name}")
        student_id = f"{fake.random_number(digits=8, fix_len=True)}"
        
        programs_by_country = {
            'US': ["Computer Science", "Business Administration", "Engineering", "Nursing", "Psychology"],
            'CA': ["Computer Science", "Business", "Engineering", "Medicine", "Arts"],
            'GB': ["Computer Science", "Business Studies", "Engineering", "Medicine", "Law"],
            'IN': ["B.Tech", "B.E.", "MBBS", "B.Com", "BBA"],
            'ID': ["Teknik Informatika", "Ekonomi", "Kedokteran", "Hukum", "Teknik"],
            'AU': ["Computer Science", "Business", "Engineering", "Medicine", "Law"],
            'DE': ["Informatik", "BWL", "Ingenieurwesen", "Medizin", "Jura"],
            'FR': ["Informatique", "Commerce", "Ingénierie", "Médecine", "Droit"],
            'ES': ["Informática", "Administración", "Ingeniería", "Medicina", "Derecho"],
            'IT': ["Informatica", "Economia", "Ingegneria", "Medicina", "Giurisprudenza"],
            'BR': ["Ciência da Computação", "Administração", "Engenharia", "Medicina"],
            'MX': ["Informática", "Administración", "Ingeniería", "Medicina", "Derecho"],
            'NL': ["Computer Science", "Business", "Engineering", "Medicine", "Law"],
            'SE': ["Datavetenskap", "Ekonomi", "Teknik", "Medicin", "Juridik"],
            'NO': ["Informatikk", "Økonomi", "Ingeniørvitenskap", "Medisin", "Jus"],
            'DK': ["Datalogi", "Økonomi", "Ingeniørvidenskab", "Medicin", "Jura"],
            'JP': ["Computer Science", "Business", "Engineering", "Medicine", "Law"],
            'KR': ["Computer Science", "Business", "Engineering", "Medicine", "Law"],
            'SG': ["Computer Science", "Business", "Engineering", "Medicine", "Law"],
            'NZ': ["Computer Science", "Business", "Engineering", "Medicine", "Law"],
            'ZA': ["Computer Science", "Business", "Engineering", "Medicine", "Law"],
            'CN': ["Computer Science", "Business", "Engineering", "Medicine", "Law"],
            'AE': ["Computer Science", "Business", "Engineering", "Medicine", "Law"],
            'PH': ["BS Computer Science", "BS Business Administration", "BS Engineering", "BS Nursing"]
        }
        
        programs = programs_by_country.get(self.selected_country, ["Computer Science", "Business", "Engineering"])
        
        today = datetime.now(timezone.utc)
        days_ago = random.randint(0, 90)
        doc_date = today - timedelta(days=days_ago)
        exp_date = doc_date + timedelta(days=365*4)  # 4 years validity
        
        # Generate registration and card numbers
        reg_number = f"REG/{self.selected_country}/{fake.random_number(digits=6, fix_len=True)}"
        card_number = f"CARD-{fake.random_number(digits=4, fix_len=True)}-{fake.random_number(digits=4, fix_len=True)}"

        country_label = f"{config['flag']} {config['name']}"
        
        return {
            "full_name": full_name,
            "student_id": student_id,
            "program": random.choice(programs),
            "college": college,
            "doc_date": doc_date,
            "exp_date": exp_date,
            "reg_number": reg_number,
            "card_number": card_number,
            "academic_year": f"{self.current_year}-{self.current_year+1}",
            "country": country_label,
            "country_code": self.selected_country
        }

    def create_simple_id_card(self, student_data):
        """Render a cleaner, more professional ID layout on the template."""
        college = student_data['college']
        college_name = college['name']
        college_id = college['id']
        student_id = student_data['student_id']

        filename = f"{student_id}_{college_id}.png"
        filepath = os.path.join(self.receipts_dir, filename)

        try:
            base = Image.open(self.template_path).convert("RGB")
        except FileNotFoundError:
            logger.warning("Template image %s not found, falling back to plain card", self.template_path)
            base = Image.new("RGB", (1000, 620), self.colors["white"])

        width, height = base.size
        draw = ImageDraw.Draw(base)

        try:
            if not os.path.exists(self.font_path):
                raise FileNotFoundError(f"Font not found: {self.font_path}")

            # Load fonts for different sections
            title_font = ImageFont.truetype(str(self.font_path), self.college_font_size + 6)
            student_font = ImageFont.truetype(str(self.font_path), self.font_size + 8)
            label_font = ImageFont.truetype(str(self.font_path), 24)
            value_font = ImageFont.truetype(str(self.font_path), 30)
            footer_font = ImageFont.truetype(str(self.font_path), 26)

            # Header bar with college branding
            header_height = 130
            draw.rectangle([0, 0, width, header_height], fill=self.colors["dark_blue"])

            college_text_bbox = draw.textbbox((0, 0), college_name, font=title_font)
            college_text_width = college_text_bbox[2] - college_text_bbox[0]
            college_text_height = college_text_bbox[3] - college_text_bbox[1]
            college_x = (width - college_text_width) / 2
            college_y = (header_height - college_text_height) / 2 - 6

            draw.text((college_x, college_y), college_name, font=title_font, fill=self.colors["white"])

            id_label = f"Institution ID: {college_id}"
            id_bbox = draw.textbbox((0, 0), id_label, font=footer_font)
            id_width = id_bbox[2] - id_bbox[0]
            draw.text((width - id_width - 30, header_height - id_bbox[3] - 15), id_label, font=footer_font, fill=self.colors["light_blue"])

            # Content panel for student details
            panel_padding = 40
            panel_top = header_height + 20
            panel_bottom = height - 90
            draw.rounded_rectangle([
                panel_padding,
                panel_top,
                width - panel_padding,
                panel_bottom
            ], radius=24, fill="#f8fafc")

            # Student name headline
            full_name = student_data["full_name"]
            name_bbox = draw.textbbox((0, 0), full_name, font=student_font)
            name_height = name_bbox[3] - name_bbox[1]
            name_x = panel_padding + 32
            name_y = panel_top + 24
            draw.text((name_x, name_y), full_name, font=student_font, fill=self.text_color)

            # Divider line under name
            draw.line([(panel_padding + 24, name_y + name_height + 16), (width - panel_padding - 24, name_y + name_height + 16)],
                      fill=self.colors["light_blue"], width=3)

            info_start_y = name_y + name_height + 38
            left_column_x = panel_padding + 32
            right_column_x = width / 2 + 10
            line_height = 52

            left_fields = [
                ("Student ID", student_id),
                ("Registration", student_data['reg_number']),
                ("Program", student_data['program']),
                ("Academic Year", student_data['academic_year']),
            ]

            right_fields = [
                ("Card Number", student_data['card_number']),
                ("Issued", student_data['doc_date'].strftime('%Y-%m-%d')),
                ("Expires", student_data['exp_date'].strftime('%Y-%m-%d')),
                ("Country", student_data['country']),
            ]

            for idx, (label, value) in enumerate(left_fields):
                y_pos = info_start_y + idx * line_height
                draw.text((left_column_x, y_pos), label, font=label_font, fill=self.colors["gray"])
                draw.text((left_column_x, y_pos + 22), value, font=value_font, fill=self.text_color)

            for idx, (label, value) in enumerate(right_fields):
                y_pos = info_start_y + idx * line_height
                draw.text((right_column_x, y_pos), label, font=label_font, fill=self.colors["gray"])
                draw.text((right_column_x, y_pos + 22), value, font=value_font, fill=self.text_color)

            # Footer bar for quick verification info
            footer_height = 70
            draw.rectangle([0, height - footer_height, width, height], fill=self.colors["dark_blue"])
            footer_text = f"Student ID {student_id}  •  Institution {college_id}  •  {student_data['country']}"
            footer_bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
            footer_width = footer_bbox[2] - footer_bbox[0]
            footer_x = (width - footer_width) / 2
            footer_y = height - footer_height + (footer_height - (footer_bbox[3] - footer_bbox[1])) / 2 - 4
            draw.text((footer_x, footer_y), footer_text, font=footer_font, fill=self.colors["white"])

        except Exception as e:
            logger.warning(f"Using fallback font due to: {e}")
            font = ImageFont.load_default()

            header_height = 100
            draw.rectangle([0, 0, width, header_height], fill=self.colors["dark_blue"])
            draw.text((20, 30), college_name, font=font, fill=self.colors["white"])
            draw.text((20, 55), f"Institution ID: {college_id}", font=font, fill=self.colors["light_blue"])

            body_y = header_height + 20
            draw.text((20, body_y), f"Name: {student_data['full_name']}", font=font, fill=self.text_color)
            draw.text((20, body_y + 18), f"Student ID: {student_id}", font=font, fill=self.text_color)
            draw.text((20, body_y + 36), f"Program: {student_data['program']}", font=font, fill=self.text_color)
            draw.text((20, body_y + 54), f"Academic Year: {student_data['academic_year']}", font=font, fill=self.text_color)
            draw.text((20, body_y + 72), f"Issued: {student_data['doc_date'].strftime('%Y-%m-%d')}", font=font, fill=self.text_color)
            draw.text((20, body_y + 90), f"Expires: {student_data['exp_date'].strftime('%Y-%m-%d')}", font=font, fill=self.text_color)

        base.save(filepath, "PNG", quality=95, optimize=True)
        self.stats["ids_generated"] += 1
        return filepath

    def save_student(self, student_data):
        """⚡⚡⚡⚡⚡ MEGA BATCH SAVE - 1000 at once"""
        with self.file_save_lock:
            try:
                self.student_buffer.append(student_data)
                
                if len(self.student_buffer) >= self.buffer_size:
                    self._flush_buffer()
                
                return True
            except:
                return False

    def _flush_buffer(self):
        if not self.student_buffer:
            return
        
        try:
            with open(self.students_file, 'a', encoding='utf-8', buffering=32768) as f:
                for student_data in self.student_buffer:
                    line = f"{student_data['full_name']}|{student_data['student_id']}|{student_data['college']['id']}|{student_data['college']['name']}|{self.selected_country}|{student_data['doc_date'].strftime('%Y-%m-%d')}|{student_data['exp_date'].strftime('%Y-%m-%d')}\n"
                    f.write(line)
                f.flush()

            self.stats["students_saved"] += len(self.student_buffer)
            self.student_buffer.clear()
        except Exception as e:
            logger.error(f"⚠️ Flush error: {e}")

    def process_one(self, num):
        try:
            college = self.select_random_college()
            if college is None:
                return False
            
            student_data = self.generate_student_data(college)
            self.create_simple_id_card(student_data)
            self.save_student(student_data)
            return True
        except Exception as e:
            logger.error(f"Error processing student {num}: {e}")
            return False

    def generate_bulk(self, quantity):
        config = COUNTRY_CONFIG[self.selected_country]
        logger.info(f"⚡⚡⚡⚡⚡ Generating {quantity} IDs for {config['flag']} {config['name']}")
        logger.info(f"✅ {len(self.all_colleges)} colleges available")
        logger.info("✅ Using EXACT names from JSON (zero modifications)")
        logger.info("✅ ENGLISH NAMES: Only English student names")
        logger.info("✅ Dates within 90 days (SheerID verified)")
        logger.info("✅ SIMPLE FORMAT: Clean layout like STU36259874.png")
        logger.info("⚡⚡⚡⚡⚡ ULTRA MEGA FAST: 5000 workers")
        logger.info("=" * 70)

        start = time.time()
        success = 0
        
        # Process in chunks for better memory management
        chunk_size = 1000
        
        for chunk_start in range(0, quantity, chunk_size):
            chunk_end = min(chunk_start + chunk_size, quantity)
            chunk_qty = chunk_end - chunk_start
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [executor.submit(self.process_one, i+1) for i in range(chunk_start, chunk_end)]
                
                for i, future in enumerate(concurrent.futures.as_completed(futures), chunk_start + 1):
                    if future.result():
                        success += 1
                    
                    if i % 200 == 0 or i == quantity:
                        elapsed = time.time() - start
                        rate = i / elapsed if elapsed > 0 else 0
                        rate_per_min = rate * 60
                        print(f"Progress: {i}/{quantity} ({(i/quantity*100):.1f}%) | Rate: {rate_per_min:.0f} IDs/min")
        
        self._flush_buffer()
        
        duration = time.time() - start
        rate_per_min = (success / duration) * 60 if duration > 0 else 0
        
        print("\n" + "="*70)
        print(f"✅ COMPLETE - {config['flag']} {config['name']}")
        print("="*70)
        print(f"⏱️  Time: {duration:.1f}s ({duration/60:.2f} minutes)")
        print(f"⚡⚡⚡⚡⚡ Speed: {rate_per_min:.0f} IDs/minute")
        print(f"✅ Success: {success}/{quantity}")
        print(f"📁 Folder: {self.receipts_dir}/")
        print(f"📄 Students: {self.students_file}")
        print(f"✅ FORMAT: Same as STU36259874.png")
        print("="*70)

    def interactive(self):
        total = 0
        config = COUNTRY_CONFIG[self.selected_country]
        
        while True:
            print(f"\n{'='*60}")
            print(f"Country: {config['flag']} {config['name']}")
            print(f"Total Generated: {total}")
            print(f"Available Colleges: {len(self.all_colleges)}")
            print(f"Mode: ULTRA MEGA FAST ⚡⚡⚡⚡⚡")
            print(f"Names: ENGLISH ONLY")
            print(f"Format: Simple layout like STU36259874.png")
            print(f"{'='*60}")
            
            user_input = input(f"\nQuantity (0 to exit): ").strip()
            
            if user_input == "0":
                self._flush_buffer()
                break
            
            try:
                quantity = int(user_input)
            except:
                print("❌ Enter a valid number")
                continue
            
            if quantity < 1:
                print("❌ Enter a number greater than 0")
                continue
            
            self.generate_bulk(quantity)
            total = self.stats["ids_generated"]

def main():
    print("\n" + "="*70)
    print("⚡⚡⚡⚡⚡ SHEERID ID - SIMPLE FORMAT GENERATOR")
    print("="*70)
    print("✅ EXACT NAMES: Uses JSON college names as-is")
    print("✅ ENGLISH NAMES: Only English student names")
    print("✅ DATES: Within 90 days (SheerID requirement)")
    print("✅ SIMPLE FORMAT: Clean layout like STU36259874.png")
    print("✅ FORMAT: STUDENTID_COLLEGEID.png")
    print("✅ SAVE: students.txt + receipts/")
    print("✅ 24 COUNTRIES: Full global support")
    print("⚡⚡⚡⚡⚡ ULTRA MEGA FAST: 5000 workers")
    print("="*70)
    
    gen = UnlimitedIDCardGenerator()
    
    if not gen.select_country_and_load():
        return
    
    gen.interactive()
    
    print("\n✅ FINISHED!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")