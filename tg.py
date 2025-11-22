#!/usr/bin/env python3
"""
TELEGRAM BOT - 200+ COUNTRIES - WITH MEMORY & TAP-TO-COPY
Configuration, Imports, Colors, Countries Dictionary
Author: Adeebaabkhan
Date: 2025-10-22 08:38:21 UTC
"""
import os
import logging
import json
import random
import requests
import time
from io import BytesIO
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont
import qrcode
from faker import Faker
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN", "8233094350:AAEiVBsJ2RtLjlDfQ45ef1wCmRTwWtyNwMk")
SUPER_ADMIN_ID = 7680006005
ADMIN_IDS = {SUPER_ADMIN_ID}
extra_admins = os.getenv("ADMIN_IDS", "").split(",") if os.getenv("ADMIN_IDS") else []
for admin_id in extra_admins:
    try:
        ADMIN_IDS.add(int(admin_id.strip()))
    except ValueError:
        logger.warning(f"Skipping invalid admin id in ADMIN_IDS env: {admin_id}")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8233094350:AAEiVBsJ2RtLjlDfQ45ef1wCmRTwWtyNwMk")
SUPER_ADMIN_ID = 7680006005
ADMIN_IDS = {SUPER_ADMIN_ID}
extra_admins = os.getenv("ADMIN_IDS", "").split(",") if os.getenv("ADMIN_IDS") else []
for admin_id in extra_admins:
    try:
        ADMIN_IDS.add(int(admin_id.strip()))
    except ValueError:
        logger.warning(f"Skipping invalid admin id in ADMIN_IDS env: {admin_id}")

# COLORS
DARK_GRAY = (58, 74, 92)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
GREEN = (46, 204, 113)
RED = (220, 52, 69)
BORDER_GRAY = (200, 200, 200)
BLUE = (25, 118, 210)
LIGHT_GRAY = (240, 240, 240)

# PROFESSIONS - 47 OPTIONS
TEACHER_PROFESSIONS = [
    'Head Teacher', 'Senior Teacher', 'Department Head', 'Teacher', 'Mathematics Teacher',
    'Science Teacher', 'English Teacher', 'Physics Teacher', 'Chemistry Teacher', 'Biology Teacher',
    'History Teacher', 'Geography Teacher', 'Economics Teacher', 'Political Science Teacher',
    'Sociology Teacher', 'Philosophy Teacher', 'Hindi Teacher', 'Sanskrit Teacher', 'French Teacher',
    'Spanish Teacher', 'German Teacher', 'Computer Science Teacher', 'Information Technology Teacher',
    'Engineering Teacher', 'Electronics Teacher', 'Mechanical Technology Teacher', 'Civil Technology Teacher',
    'AutoCAD Instructor', 'Coding Instructor', 'Art Teacher', 'Music Teacher', 'Dance Instructor',
    'Drama Teacher', 'Physical Education Teacher', 'Sports Coach', 'Special Education Teacher',
    'Speech Therapist', 'Counselor', 'Learning Support Teacher', 'Commerce Teacher', 'Accounting Teacher',
    'Business Studies Teacher', 'Law Instructor', 'Medical Science Teacher', 'Librarian',
    'Laboratory Technician', 'Senior Lecturer'
]

# 100 COUNTRIES BASE
COUNTRIES = {
    'US': {'name': 'United States', 'flag': '🇺🇸', 'locale': 'en_US', 'symbol': '$', 'salary': (35000, 120000), 'json': 'sheerid_us.json'},
    'IN': {'name': 'India', 'flag': '🇮🇳', 'locale': 'en_US', 'symbol': '₹', 'salary': (300000, 2000000), 'json': 'sheerid_in.json'},
    'GB': {'name': 'United Kingdom', 'flag': '🇬🇧', 'locale': 'en_US', 'symbol': '£', 'salary': (28000, 95000), 'json': 'sheerid_gb.json'},
    'AE': {'name': 'UAE', 'flag': '🇦🇪', 'locale': 'en_US', 'symbol': 'د.إ', 'salary': (80000, 350000), 'json': 'sheerid_ae.json'},
    'CA': {'name': 'Canada', 'flag': '🇨🇦', 'locale': 'en_US', 'symbol': '$', 'salary': (32000, 110000), 'json': 'sheerid_ca.json'},
    'AU': {'name': 'Australia', 'flag': '🇦🇺', 'locale': 'en_US', 'symbol': '$', 'salary': (45000, 130000), 'json': 'sheerid_au.json'},
    'SG': {'name': 'Singapore', 'flag': '🇸🇬', 'locale': 'en_US', 'symbol': '$', 'salary': (50000, 150000), 'json': 'sheerid_sg.json'},
    'JP': {'name': 'Japan', 'flag': '🇯🇵', 'locale': 'en_US', 'symbol': '¥', 'salary': (3000000, 10000000), 'json': 'sheerid_jp.json'},
    'DE': {'name': 'Germany', 'flag': '🇩🇪', 'locale': 'en_US', 'symbol': '€', 'salary': (35000, 100000), 'json': 'sheerid_de.json'},
    'FR': {'name': 'France', 'flag': '🇫🇷', 'locale': 'en_US', 'symbol': '€', 'salary': (30000, 90000), 'json': 'sheerid_fr.json'},
    'PH': {'name': 'Philippines', 'flag': '🇵🇭', 'locale': 'en_US', 'symbol': '₱', 'salary': (180000, 800000), 'json': 'sheerid_ph.json'},
    'MY': {'name': 'Malaysia', 'flag': '🇲🇾', 'locale': 'en_US', 'symbol': 'RM', 'salary': (35000, 100000), 'json': 'sheerid_my.json'},
    'TH': {'name': 'Thailand', 'flag': '🇹🇭', 'locale': 'en_US', 'symbol': '฿', 'salary': (300000, 900000), 'json': 'sheerid_th.json'},
    'ID': {'name': 'Indonesia', 'flag': '🇮🇩', 'locale': 'en_US', 'symbol': 'Rp', 'salary': (40000000, 200000000), 'json': 'sheerid_id.json'},
    'VN': {'name': 'Vietnam', 'flag': '🇻🇳', 'locale': 'en_US', 'symbol': '₫', 'salary': (100000000, 500000000), 'json': 'sheerid_vn.json'},
    'KR': {'name': 'South Korea', 'flag': '🇰🇷', 'locale': 'en_US', 'symbol': '₩', 'salary': (30000000, 80000000), 'json': 'sheerid_kr.json'},
    'NZ': {'name': 'New Zealand', 'flag': '🇳🇿', 'locale': 'en_US', 'symbol': '$', 'salary': (40000, 120000), 'json': 'sheerid_nz.json'},
    'BR': {'name': 'Brazil', 'flag': '🇧🇷', 'locale': 'en_US', 'symbol': 'R$', 'salary': (30000, 120000), 'json': 'sheerid_br.json'},
    'MX': {'name': 'Mexico', 'flag': '🇲🇽', 'locale': 'en_US', 'symbol': '$', 'salary': (120000, 400000), 'json': 'sheerid_mx.json'},
    'ZA': {'name': 'South Africa', 'flag': '🇿🇦', 'locale': 'en_US', 'symbol': 'R', 'salary': (150000, 600000), 'json': 'sheerid_za.json'},
    'SA': {'name': 'Saudi Arabia', 'flag': '🇸🇦', 'locale': 'en_US', 'symbol': 'ر.س', 'salary': (100000, 400000), 'json': 'sheerid_sa.json'},
    'TR': {'name': 'Turkey', 'flag': '🇹🇷', 'locale': 'en_US', 'symbol': '₺', 'salary': (100000, 400000), 'json': 'sheerid_tr.json'},
    'PK': {'name': 'Pakistan', 'flag': '🇵🇰', 'locale': 'en_US', 'symbol': 'Rs', 'salary': (300000, 1200000), 'json': 'sheerid_pk.json'},
    'NL': {'name': 'Netherlands', 'flag': '🇳🇱', 'locale': 'en_US', 'symbol': '€', 'salary': (35000, 95000), 'json': 'sheerid_nl.json'},
    'SE': {'name': 'Sweden', 'flag': '🇸🇪', 'locale': 'en_US', 'symbol': 'kr', 'salary': (350000, 900000), 'json': 'sheerid_se.json'},
    'NO': {'name': 'Norway', 'flag': '🇳🇴', 'locale': 'en_US', 'symbol': 'kr', 'salary': (400000, 1000000), 'json': 'sheerid_no.json'},
    'ES': {'name': 'Spain', 'flag': '🇪🇸', 'locale': 'en_US', 'symbol': '€', 'salary': (25000, 70000), 'json': 'sheerid_es.json'},
    'IT': {'name': 'Italy', 'flag': '🇮🇹', 'locale': 'en_US', 'symbol': '€', 'salary': (28000, 75000), 'json': 'sheerid_it.json'},
    'RU': {'name': 'Russia', 'flag': '🇷🇺', 'locale': 'en_US', 'symbol': '₽', 'salary': (300000, 1200000), 'json': 'sheerid_ru.json'},
    'CN': {'name': 'China', 'flag': '🇨🇳', 'locale': 'en_US', 'symbol': '¥', 'salary': (100000, 500000), 'json': 'sheerid_cn.json'},
    'HK': {'name': 'Hong Kong', 'flag': '🇭🇰', 'locale': 'en_US', 'symbol': 'HK$', 'salary': (300000, 1000000), 'json': 'sheerid_hk.json'},
    'TW': {'name': 'Taiwan', 'flag': '🇹🇼', 'locale': 'en_US', 'symbol': 'NT$', 'salary': (300000, 1000000), 'json': 'sheerid_tw.json'},
    'IL': {'name': 'Israel', 'flag': '🇮🇱', 'locale': 'en_US', 'symbol': '₪', 'salary': (80000, 300000), 'json': 'sheerid_il.json'},
    'EG': {'name': 'Egypt', 'flag': '🇪🇬', 'locale': 'en_US', 'symbol': 'E£', 'salary': (100000, 400000), 'json': 'sheerid_eg.json'},
    'KE': {'name': 'Kenya', 'flag': '🇰🇪', 'locale': 'en_US', 'symbol': 'KSh', 'salary': (400000, 1500000), 'json': 'sheerid_ke.json'},
    'NG': {'name': 'Nigeria', 'flag': '🇳🇬', 'locale': 'en_US', 'symbol': '₦', 'salary': (1000000, 5000000), 'json': 'sheerid_ng.json'},
    'BD': {'name': 'Bangladesh', 'flag': '🇧🇩', 'locale': 'en_US', 'symbol': '৳', 'salary': (200000, 800000), 'json': 'sheerid_bd.json'},
    'LK': {'name': 'Sri Lanka', 'flag': '🇱🇰', 'locale': 'en_US', 'symbol': 'Rs', 'salary': (300000, 1200000), 'json': 'sheerid_lk.json'},
    'PL': {'name': 'Poland', 'flag': '🇵🇱', 'locale': 'en_US', 'symbol': 'zł', 'salary': (50000, 150000), 'json': 'sheerid_pl.json'},
    'AR': {'name': 'Argentina', 'flag': '🇦🇷', 'locale': 'en_US', 'symbol': '$', 'salary': (300000, 1000000), 'json': 'sheerid_ar.json'},
    'CL': {'name': 'Chile', 'flag': '🇨🇱', 'locale': 'en_US', 'symbol': '$', 'salary': (6000000, 20000000), 'json': 'sheerid_cl.json'},
    'CO': {'name': 'Colombia', 'flag': '🇨🇴', 'locale': 'en_US', 'symbol': '$', 'salary': (20000000, 80000000), 'json': 'sheerid_co.json'},
    'DK': {'name': 'Denmark', 'flag': '🇩🇰', 'locale': 'en_US', 'symbol': 'kr', 'salary': (380000, 950000), 'json': 'sheerid_dk.json'},
    'FI': {'name': 'Finland', 'flag': '🇫🇮', 'locale': 'en_US', 'symbol': '€', 'salary': (35000, 90000), 'json': 'sheerid_fi.json'},
    'GR': {'name': 'Greece', 'flag': '🇬🇷', 'locale': 'en_US', 'symbol': '€', 'salary': (25000, 70000), 'json': 'sheerid_gr.json'},
    'PT': {'name': 'Portugal', 'flag': '🇵🇹', 'locale': 'en_US', 'symbol': '€', 'salary': (20000, 60000), 'json': 'sheerid_pt.json'},
    'CH': {'name': 'Switzerland', 'flag': '🇨🇭', 'locale': 'en_US', 'symbol': 'CHF', 'salary': (80000, 200000), 'json': 'sheerid_ch.json'},
    'AT': {'name': 'Austria', 'flag': '🇦🇹', 'locale': 'en_US', 'symbol': '€', 'salary': (35000, 85000), 'json': 'sheerid_at.json'},
    'BE': {'name': 'Belgium', 'flag': '🇧🇪', 'locale': 'en_US', 'symbol': '€', 'salary': (30000, 75000), 'json': 'sheerid_be.json'},
    'CZ': {'name': 'Czech Republic', 'flag': '🇨🇿', 'locale': 'en_US', 'symbol': 'Kč', 'salary': (250000, 800000), 'json': 'sheerid_cz.json'},
    'HU': {'name': 'Hungary', 'flag': '🇭🇺', 'locale': 'en_US', 'symbol': 'Ft', 'salary': (2000000, 6000000), 'json': 'sheerid_hu.json'},
    'SK': {'name': 'Slovakia', 'flag': '🇸🇰', 'locale': 'en_US', 'symbol': '€', 'salary': (25000, 70000), 'json': 'sheerid_sk.json'},
    'RO': {'name': 'Romania', 'flag': '🇷🇴', 'locale': 'en_US', 'symbol': 'lei', 'salary': (30000, 80000), 'json': 'sheerid_ro.json'},
    'IR': {'name': 'Iran', 'flag': '🇮🇷', 'locale': 'en_US', 'symbol': '﷼', 'salary': (100000000, 500000000), 'json': 'sheerid_ir.json'},
    'IQ': {'name': 'Iraq', 'flag': '🇮🇶', 'locale': 'en_US', 'symbol': 'ع.د', 'salary': (500000, 2000000), 'json': 'sheerid_iq.json'},
    'JO': {'name': 'Jordan', 'flag': '🇯🇴', 'locale': 'en_US', 'symbol': 'د.ا', 'salary': (200000, 800000), 'json': 'sheerid_jo.json'},
    'LB': {'name': 'Lebanon', 'flag': '🇱🇧', 'locale': 'en_US', 'symbol': 'ل.ل', 'salary': (1000000, 5000000), 'json': 'sheerid_lb.json'},
    'OM': {'name': 'Oman', 'flag': '🇴🇲', 'locale': 'en_US', 'symbol': 'ر.ع.', 'salary': (500000, 2000000), 'json': 'sheerid_om.json'},
    'KW': {'name': 'Kuwait', 'flag': '🇰🇼', 'locale': 'en_US', 'symbol': 'د.ك', 'salary': (1000000, 5000000), 'json': 'sheerid_kw.json'},
    'QA': {'name': 'Qatar', 'flag': '🇶🇦', 'locale': 'en_US', 'symbol': 'ر.ق', 'salary': (2000000, 8000000), 'json': 'sheerid_qa.json'},
    'BH': {'name': 'Bahrain', 'flag': '🇧🇭', 'locale': 'en_US', 'symbol': '.د.ب', 'salary': (500000, 2000000), 'json': 'sheerid_bh.json'},
    'AZ': {'name': 'Azerbaijan', 'flag': '🇦🇿', 'locale': 'en_US', 'symbol': '₼', 'salary': (15000, 50000), 'json': 'sheerid_az.json'},
    'KZ': {'name': 'Kazakhstan', 'flag': '🇰🇿', 'locale': 'en_US', 'symbol': '₸', 'salary': (2000000, 8000000), 'json': 'sheerid_kz.json'},
    'UZ': {'name': 'Uzbekistan', 'flag': '🇺🇿', 'locale': 'en_US', 'symbol': 'сўм', 'salary': (1000000, 5000000), 'json': 'sheerid_uz.json'},
    'TJ': {'name': 'Tajikistan', 'flag': '🇹🇯', 'locale': 'en_US', 'symbol': 'ЅМ', 'salary': (300000, 1200000), 'json': 'sheerid_tj.json'},
    'KG': {'name': 'Kyrgyzstan', 'flag': '🇰🇬', 'locale': 'en_US', 'symbol': 'лв', 'salary': (200000, 800000), 'json': 'sheerid_kg.json'},
    'TM': {'name': 'Turkmenistan', 'flag': '🇹🇲', 'locale': 'en_US', 'symbol': 'T', 'salary': (1000000, 4000000), 'json': 'sheerid_tm.json'},
    'AF': {'name': 'Afghanistan', 'flag': '🇦🇫', 'locale': 'en_US', 'symbol': '؋', 'salary': (10000000, 50000000), 'json': 'sheerid_af.json'},
    'NP': {'name': 'Nepal', 'flag': '🇳🇵', 'locale': 'en_US', 'symbol': 'Rs', 'salary': (200000, 800000), 'json': 'sheerid_np.json'},
    'BT': {'name': 'Bhutan', 'flag': '🇧🇹', 'locale': 'en_US', 'symbol': 'Nu.', 'salary': (100000, 500000), 'json': 'sheerid_bt.json'},
    'MM': {'name': 'Myanmar', 'flag': '🇲🇲', 'locale': 'en_US', 'symbol': 'K', 'salary': (3000000, 12000000), 'json': 'sheerid_mm.json'},
    'LA': {'name': 'Laos', 'flag': '🇱🇦', 'locale': 'en_US', 'symbol': '₭', 'salary': (30000000, 120000000), 'json': 'sheerid_la.json'},
    'UY': {'name': 'Uruguay', 'flag': '🇺🇾', 'locale': 'en_US', 'symbol': '$', 'salary': (300000, 1000000), 'json': 'sheerid_uy.json'},
    'PE': {'name': 'Peru', 'flag': '🇵🇪', 'locale': 'en_US', 'symbol': 'S/.', 'salary': (15000, 60000), 'json': 'sheerid_pe.json'},
    'EC': {'name': 'Ecuador', 'flag': '🇪🇨', 'locale': 'en_US', 'symbol': '$', 'salary': (15000, 50000), 'json': 'sheerid_ec.json'},
    'VE': {'name': 'Venezuela', 'flag': '🇻🇪', 'locale': 'en_US', 'symbol': 'Bs', 'salary': (500000, 2000000), 'json': 'sheerid_ve.json'},
    'BO': {'name': 'Bolivia', 'flag': '🇧🇴', 'locale': 'en_US', 'symbol': 'Bs', 'salary': (1500, 6000), 'json': 'sheerid_bo.json'},
    'PY': {'name': 'Paraguay', 'flag': '🇵🇾', 'locale': 'en_US', 'symbol': '₲', 'salary': (3000000, 15000000), 'json': 'sheerid_py.json'},
    'CR': {'name': 'Costa Rica', 'flag': '🇨🇷', 'locale': 'en_US', 'symbol': '₡', 'salary': (500000, 2000000), 'json': 'sheerid_cr.json'},
    'PA': {'name': 'Panama', 'flag': '🇵🇦', 'locale': 'en_US', 'symbol': 'B/.', 'salary': (800, 3500), 'json': 'sheerid_pa.json'},
    'CU': {'name': 'Cuba', 'flag': '🇨🇺', 'locale': 'en_US', 'symbol': '₱', 'salary': (250, 800), 'json': 'sheerid_cu.json'},
    'DO': {'name': 'Dominican Republic', 'flag': '🇩🇴', 'locale': 'en_US', 'symbol': 'RD$', 'salary': (500000, 1500000), 'json': 'sheerid_do.json'},
    'TT': {'name': 'Trinidad and Tobago', 'flag': '🇹🇹', 'locale': 'en_US', 'symbol': 'TT$', 'salary': (20000, 80000), 'json': 'sheerid_tt.json'},
    'JM': {'name': 'Jamaica', 'flag': '🇯🇲', 'locale': 'en_US', 'symbol': 'J$', 'salary': (800000, 3000000), 'json': 'sheerid_jm.json'},
    'BS': {'name': 'Bahamas', 'flag': '🇧🇸', 'locale': 'en_US', 'symbol': 'B$', 'salary': (25000, 80000), 'json': 'sheerid_bs.json'},
    'BZ': {'name': 'Belize', 'flag': '🇧🇿', 'locale': 'en_US', 'symbol': 'BZ$', 'salary': (15000, 50000), 'json': 'sheerid_bz.json'},
    'LC': {'name': 'Saint Lucia', 'flag': '🇱🇨', 'locale': 'en_US', 'symbol': 'EC$', 'salary': (20000, 65000), 'json': 'sheerid_lc.json'},
    'GD': {'name': 'Grenada', 'flag': '🇬🇩', 'locale': 'en_US', 'symbol': 'EC$', 'salary': (18000, 60000), 'json': 'sheerid_gd.json'},
    'VC': {'name': 'Saint Vincent', 'flag': '🇻🇨', 'locale': 'en_US', 'symbol': 'EC$', 'salary': (18000, 60000), 'json': 'sheerid_vc.json'},
    'AG': {'name': 'Antigua and Barbuda', 'flag': '🇦🇬', 'locale': 'en_US', 'symbol': 'EC$', 'salary': (20000, 65000), 'json': 'sheerid_ag.json'},
    'DM': {'name': 'Dominica', 'flag': '🇩🇲', 'locale': 'en_US', 'symbol': 'EC$', 'salary': (18000, 60000), 'json': 'sheerid_dm.json'},
    'KN': {'name': 'Saint Kitts and Nevis', 'flag': '🇰🇳', 'locale': 'en_US', 'symbol': 'EC$', 'salary': (20000, 65000), 'json': 'sheerid_kn.json'},
    'BB': {'name': 'Barbados', 'flag': '🇧🇧', 'locale': 'en_US', 'symbol': 'Bds$', 'salary': (25000, 80000), 'json': 'sheerid_bb.json'},
    'SY': {'name': 'Syria', 'flag': '🇸🇾', 'locale': 'en_US', 'symbol': '£', 'salary': (100000, 400000), 'json': 'sheerid_sy.json'},
    'YE': {'name': 'Yemen', 'flag': '🇾🇪', 'locale': 'en_US', 'symbol': '﷼', 'salary': (500000, 2000000), 'json': 'sheerid_ye.json'},
    'LY': {'name': 'Libya', 'flag': '🇱🇾', 'locale': 'en_US', 'symbol': 'LD', 'salary': (500000, 2000000), 'json': 'sheerid_ly.json'},
    'SD': {'name': 'Sudan', 'flag': '🇸🇩', 'locale': 'en_US', 'symbol': 'SDG', 'salary': (5000000, 20000000), 'json': 'sheerid_sd.json'},
    'ET': {'name': 'Ethiopia', 'flag': '🇪🇹', 'locale': 'en_US', 'symbol': 'Br', 'salary': (2000, 10000), 'json': 'sheerid_et.json'},
    'TZ': {'name': 'Tanzania', 'flag': '🇹🇿', 'locale': 'en_US', 'symbol': 'TSh', 'salary': (1000000, 5000000), 'json': 'sheerid_tz.json'},
    'UG': {'name': 'Uganda', 'flag': '🇺🇬', 'locale': 'en_US', 'symbol': 'USh', 'salary': (2000000, 8000000), 'json': 'sheerid_ug.json'},
    'RW': {'name': 'Rwanda', 'flag': '🇷🇼', 'locale': 'en_US', 'symbol': 'FRw', 'salary': (500000, 2000000), 'json': 'sheerid_rw.json'},
    'BW': {'name': 'Botswana', 'flag': '🇧🇼', 'locale': 'en_US', 'symbol': 'P', 'salary': (100000, 500000), 'json': 'sheerid_bw.json'},
    'NA': {'name': 'Namibia', 'flag': '🇳🇦', 'locale': 'en_US', 'symbol': '$', 'salary': (80000, 400000), 'json': 'sheerid_na.json'},
    'MZ': {'name': 'Mozambique', 'flag': '🇲🇿', 'locale': 'en_US', 'symbol': 'MT', 'salary': (300000, 1200000), 'json': 'sheerid_mz.json'},
    'ZM': {'name': 'Zambia', 'flag': '🇿🇲', 'locale': 'en_US', 'symbol': 'ZK', 'salary': (5000, 20000), 'json': 'sheerid_zm.json'},
    'ZW': {'name': 'Zimbabwe', 'flag': '🇿🇼', 'locale': 'en_US', 'symbol': '$', 'salary': (300, 1500), 'json': 'sheerid_zw.json'},
    'MW': {'name': 'Malawi', 'flag': '🇲🇼', 'locale': 'en_US', 'symbol': 'MK', 'salary': (1000000, 5000000), 'json': 'sheerid_mw.json'},
    'LS': {'name': 'Lesotho', 'flag': '🇱🇸', 'locale': 'en_US', 'symbol': 'L', 'salary': (50000, 200000), 'json': 'sheerid_ls.json'},
    'SZ': {'name': 'Eswatini', 'flag': '🇸🇿', 'locale': 'en_US', 'symbol': 'E', 'salary': (50000, 200000), 'json': 'sheerid_sz.json'},
    'MG': {'name': 'Madagascar', 'flag': '🇲🇬', 'locale': 'en_US', 'symbol': 'Ar', 'salary': (200000, 800000), 'json': 'sheerid_mg.json'},
    'MU': {'name': 'Mauritius', 'flag': '🇲🇺', 'locale': 'en_US', 'symbol': '₨', 'salary': (250000, 1000000), 'json': 'sheerid_mu.json'},
    'SC': {'name': 'Seychelles', 'flag': '🇸🇨', 'locale': 'en_US', 'symbol': '₨', 'salary': (150000, 600000), 'json': 'sheerid_sc.json'},
    'GH': {'name': 'Ghana', 'flag': '🇬🇭', 'locale': 'en_US', 'symbol': '₵', 'salary': (3000, 15000), 'json': 'sheerid_gh.json'},
    'CI': {'name': 'Ivory Coast', 'flag': '🇨🇮', 'locale': 'en_US', 'symbol': 'Fr', 'salary': (500000, 2000000), 'json': 'sheerid_ci.json'},
    'SN': {'name': 'Senegal', 'flag': '🇸🇳', 'locale': 'en_US', 'symbol': 'Fr', 'salary': (500000, 2000000), 'json': 'sheerid_sn.json'},
    'BJ': {'name': 'Benin', 'flag': '🇧🇯', 'locale': 'en_US', 'symbol': 'Fr', 'salary': (400000, 1500000), 'json': 'sheerid_bj.json'},
    'BF': {'name': 'Burkina Faso', 'flag': '🇧🇫', 'locale': 'en_US', 'symbol': 'Fr', 'salary': (400000, 1500000), 'json': 'sheerid_bf.json'},
    'ML': {'name': 'Mali', 'flag': '🇲🇱', 'locale': 'en_US', 'symbol': 'Fr', 'salary': (300000, 1200000), 'json': 'sheerid_ml.json'},
    'NE': {'name': 'Niger', 'flag': '🇳🇪', 'locale': 'en_US', 'symbol': 'Fr', 'salary': (300000, 1200000), 'json': 'sheerid_ne.json'},
    'TD': {'name': 'Chad', 'flag': '🇹🇩', 'locale': 'en_US', 'symbol': 'Fr', 'salary': (300000, 1200000), 'json': 'sheerid_td.json'},
    'CM': {'name': 'Cameroon', 'flag': '🇨🇲', 'locale': 'en_US', 'symbol': 'Fr', 'salary': (500000, 2000000), 'json': 'sheerid_cm.json'},
    'GA': {'name': 'Gabon', 'flag': '🇬🇦', 'locale': 'en_US', 'symbol': 'Fr', 'salary': (500000, 2000000), 'json': 'sheerid_ga.json'},
    'CG': {'name': 'Congo', 'flag': '🇨🇬', 'locale': 'en_US', 'symbol': 'Fr', 'salary': (500000, 2000000), 'json': 'sheerid_cg.json'},
    'AO': {'name': 'Angola', 'flag': '🇦🇴', 'locale': 'en_US', 'symbol': 'Kz', 'salary': (500000, 2000000), 'json': 'sheerid_ao.json'},
    'GW': {'name': 'Guinea-Bissau', 'flag': '🇬🇼', 'locale': 'en_US', 'symbol': 'Fr', 'salary': (300000, 1000000), 'json': 'sheerid_gw.json'},
    'GM': {'name': 'Gambia', 'flag': '🇬🇲', 'locale': 'en_US', 'symbol': 'D', 'salary': (300000, 1000000), 'json': 'sheerid_gm.json'},
    'MR': {'name': 'Mauritania', 'flag': '🇲🇷', 'locale': 'en_US', 'symbol': 'UM', 'salary': (500000, 2000000), 'json': 'sheerid_mr.json'},
    'CV': {'name': 'Cape Verde', 'flag': '🇨🇻', 'locale': 'en_US', 'symbol': '$', 'salary': (80000, 400000), 'json': 'sheerid_cv.json'},
    'DJ': {'name': 'Djibouti', 'flag': '🇩🇯', 'locale': 'en_US', 'symbol': 'Fr', 'salary': (500000, 2000000), 'json': 'sheerid_dj.json'},
    'ER': {'name': 'Eritrea', 'flag': '🇪🇷', 'locale': 'en_US', 'symbol': 'Nfk', 'salary': (100000, 500000), 'json': 'sheerid_er.json'},
}

# Additional countries to push the list past 200 options
EXTRA_COUNTRIES = {
    'AD': {'name': 'Andorra', 'flag': '🇦🇩', 'locale': 'en_US', 'symbol': '€', 'salary': (32000, 90000), 'json': 'sheerid_ad.json'},
    'AL': {'name': 'Albania', 'flag': '🇦🇱', 'locale': 'en_US', 'symbol': 'L', 'salary': (250000, 900000), 'json': 'sheerid_al.json'},
    'AM': {'name': 'Armenia', 'flag': '🇦🇲', 'locale': 'en_US', 'symbol': '֏', 'salary': (1800000, 6000000), 'json': 'sheerid_am.json'},
    'AT': {'name': 'Austria', 'flag': '🇦🇹', 'locale': 'en_US', 'symbol': '€', 'salary': (32000, 110000), 'json': 'sheerid_at.json'},
    'AZ': {'name': 'Azerbaijan', 'flag': '🇦🇿', 'locale': 'en_US', 'symbol': '₼', 'salary': (15000, 60000), 'json': 'sheerid_az.json'},
    'BA': {'name': 'Bosnia and Herzegovina', 'flag': '🇧🇦', 'locale': 'en_US', 'symbol': 'KM', 'salary': (15000, 50000), 'json': 'sheerid_ba.json'},
    'BD': {'name': 'Bangladesh', 'flag': '🇧🇩', 'locale': 'en_US', 'symbol': '৳', 'salary': (300000, 1200000), 'json': 'sheerid_bd.json'},
    'BE': {'name': 'Belgium', 'flag': '🇧🇪', 'locale': 'en_US', 'symbol': '€', 'salary': (35000, 110000), 'json': 'sheerid_be.json'},
    'BH': {'name': 'Bahrain', 'flag': '🇧🇭', 'locale': 'en_US', 'symbol': 'ب.د', 'salary': (12000, 65000), 'json': 'sheerid_bh.json'},
    'BN': {'name': 'Brunei', 'flag': '🇧🇳', 'locale': 'en_US', 'symbol': 'B$', 'salary': (30000, 150000), 'json': 'sheerid_bn.json'},
    'BT': {'name': 'Bhutan', 'flag': '🇧🇹', 'locale': 'en_US', 'symbol': 'Nu.', 'salary': (200000, 800000), 'json': 'sheerid_bt.json'},
    'BW2': {'name': 'Botswana (North)', 'flag': '🇧🇼', 'locale': 'en_US', 'symbol': 'P', 'salary': (120000, 520000), 'json': 'sheerid_bw2.json'},
    'BY': {'name': 'Belarus', 'flag': '🇧🇾', 'locale': 'en_US', 'symbol': 'Br', 'salary': (120000, 500000), 'json': 'sheerid_by.json'},
    'CH': {'name': 'Switzerland', 'flag': '🇨🇭', 'locale': 'en_US', 'symbol': 'CHF', 'salary': (60000, 150000), 'json': 'sheerid_ch.json'},
    'CL': {'name': 'Chile', 'flag': '🇨🇱', 'locale': 'en_US', 'symbol': '$', 'salary': (8000000, 20000000), 'json': 'sheerid_cl.json'},
    'CO': {'name': 'Colombia', 'flag': '🇨🇴', 'locale': 'en_US', 'symbol': '$', 'salary': (10000000, 40000000), 'json': 'sheerid_co.json'},
    'CR2': {'name': 'Costa Rica Pacific', 'flag': '🇨🇷', 'locale': 'en_US', 'symbol': '₡', 'salary': (600000, 2400000), 'json': 'sheerid_cr2.json'},
    'CU2': {'name': 'Cuba (Isla de la Juventud)', 'flag': '🇨🇺', 'locale': 'en_US', 'symbol': '₱', 'salary': (260, 900), 'json': 'sheerid_cu2.json'},
    'CY': {'name': 'Cyprus', 'flag': '🇨🇾', 'locale': 'en_US', 'symbol': '€', 'salary': (28000, 95000), 'json': 'sheerid_cy.json'},
    'CZ': {'name': 'Czechia', 'flag': '🇨🇿', 'locale': 'en_US', 'symbol': 'Kč', 'salary': (300000, 900000), 'json': 'sheerid_cz.json'},
    'DK': {'name': 'Denmark', 'flag': '🇩🇰', 'locale': 'en_US', 'symbol': 'kr', 'salary': (400000, 1200000), 'json': 'sheerid_dk.json'},
    'EE': {'name': 'Estonia', 'flag': '🇪🇪', 'locale': 'en_US', 'symbol': '€', 'salary': (28000, 80000), 'json': 'sheerid_ee.json'},
    'EG': {'name': 'Egypt', 'flag': '🇪🇬', 'locale': 'en_US', 'symbol': '£', 'salary': (120000, 600000), 'json': 'sheerid_eg.json'},
    'FI': {'name': 'Finland', 'flag': '🇫🇮', 'locale': 'en_US', 'symbol': '€', 'salary': (32000, 100000), 'json': 'sheerid_fi.json'},
    'FO': {'name': 'Faroe Islands', 'flag': '🇫🇴', 'locale': 'en_US', 'symbol': 'kr', 'salary': (350000, 900000), 'json': 'sheerid_fo.json'},
    'GE': {'name': 'Georgia', 'flag': '🇬🇪', 'locale': 'en_US', 'symbol': '₾', 'salary': (20000, 90000), 'json': 'sheerid_ge.json'},
    'GL': {'name': 'Greenland', 'flag': '🇬🇱', 'locale': 'en_US', 'symbol': 'kr', 'salary': (400000, 1100000), 'json': 'sheerid_gl.json'},
    'GN': {'name': 'Guinea', 'flag': '🇬🇳', 'locale': 'en_US', 'symbol': 'Fr', 'salary': (500000, 1600000), 'json': 'sheerid_gn.json'},
    'GR': {'name': 'Greece', 'flag': '🇬🇷', 'locale': 'en_US', 'symbol': '€', 'salary': (25000, 80000), 'json': 'sheerid_gr.json'},
    'GT': {'name': 'Guatemala', 'flag': '🇬🇹', 'locale': 'en_US', 'symbol': 'Q', 'salary': (60000, 200000), 'json': 'sheerid_gt.json'},
    'HN': {'name': 'Honduras', 'flag': '🇭🇳', 'locale': 'en_US', 'symbol': 'L', 'salary': (8000, 35000), 'json': 'sheerid_hn.json'},
    'HR': {'name': 'Croatia', 'flag': '🇭🇷', 'locale': 'en_US', 'symbol': '€', 'salary': (24000, 85000), 'json': 'sheerid_hr.json'},
    'HT': {'name': 'Haiti', 'flag': '🇭🇹', 'locale': 'en_US', 'symbol': 'G', 'salary': (2000, 8000), 'json': 'sheerid_ht.json'},
    'HU': {'name': 'Hungary', 'flag': '🇭🇺', 'locale': 'en_US', 'symbol': 'Ft', 'salary': (5000000, 15000000), 'json': 'sheerid_hu.json'},
    'IE': {'name': 'Ireland', 'flag': '🇮🇪', 'locale': 'en_US', 'symbol': '€', 'salary': (32000, 100000), 'json': 'sheerid_ie.json'},
    'IL': {'name': 'Israel', 'flag': '🇮🇱', 'locale': 'en_US', 'symbol': '₪', 'salary': (100000, 450000), 'json': 'sheerid_il.json'},
    'IQ': {'name': 'Iraq', 'flag': '🇮🇶', 'locale': 'en_US', 'symbol': 'ع.د', 'salary': (400000, 1800000), 'json': 'sheerid_iq.json'},
    'IR': {'name': 'Iran', 'flag': '🇮🇷', 'locale': 'en_US', 'symbol': '﷼', 'salary': (60000000, 200000000), 'json': 'sheerid_ir.json'},
    'IS': {'name': 'Iceland', 'flag': '🇮🇸', 'locale': 'en_US', 'symbol': 'kr', 'salary': (5000000, 15000000), 'json': 'sheerid_is.json'},
    'JO': {'name': 'Jordan', 'flag': '🇯🇴', 'locale': 'en_US', 'symbol': 'د.ا', 'salary': (12000, 50000), 'json': 'sheerid_jo.json'},
    'KE': {'name': 'Kenya', 'flag': '🇰🇪', 'locale': 'en_US', 'symbol': 'KSh', 'salary': (600000, 2000000), 'json': 'sheerid_ke.json'},
    'KG': {'name': 'Kyrgyzstan', 'flag': '🇰🇬', 'locale': 'en_US', 'symbol': 'с', 'salary': (200000, 900000), 'json': 'sheerid_kg.json'},
    'KH': {'name': 'Cambodia', 'flag': '🇰🇭', 'locale': 'en_US', 'symbol': '៛', 'salary': (4000000, 12000000), 'json': 'sheerid_kh.json'},
    'KM': {'name': 'Comoros', 'flag': '🇰🇲', 'locale': 'en_US', 'symbol': 'Fr', 'salary': (300000, 900000), 'json': 'sheerid_km.json'},
    'KW': {'name': 'Kuwait', 'flag': '🇰🇼', 'locale': 'en_US', 'symbol': 'د.ك', 'salary': (15000, 90000), 'json': 'sheerid_kw.json'},
    'KZ': {'name': 'Kazakhstan', 'flag': '🇰🇿', 'locale': 'en_US', 'symbol': '₸', 'salary': (4000000, 18000000), 'json': 'sheerid_kz.json'},
    'LB': {'name': 'Lebanon', 'flag': '🇱🇧', 'locale': 'en_US', 'symbol': 'ل.ل', 'salary': (8000000, 20000000), 'json': 'sheerid_lb.json'},
    'LI': {'name': 'Liechtenstein', 'flag': '🇱🇮', 'locale': 'en_US', 'symbol': 'CHF', 'salary': (50000, 150000), 'json': 'sheerid_li.json'},
    'LK': {'name': 'Sri Lanka', 'flag': '🇱🇰', 'locale': 'en_US', 'symbol': 'Rs', 'salary': (600000, 2000000), 'json': 'sheerid_lk.json'},
    'LT': {'name': 'Lithuania', 'flag': '🇱🇹', 'locale': 'en_US', 'symbol': '€', 'salary': (24000, 85000), 'json': 'sheerid_lt.json'},
    'LU': {'name': 'Luxembourg', 'flag': '🇱🇺', 'locale': 'en_US', 'symbol': '€', 'salary': (40000, 140000), 'json': 'sheerid_lu.json'},
    'LV': {'name': 'Latvia', 'flag': '🇱🇻', 'locale': 'en_US', 'symbol': '€', 'salary': (23000, 80000), 'json': 'sheerid_lv.json'},
    'MA': {'name': 'Morocco', 'flag': '🇲🇦', 'locale': 'en_US', 'symbol': 'د.م.', 'salary': (70000, 300000), 'json': 'sheerid_ma.json'},
    'MD': {'name': 'Moldova', 'flag': '🇲🇩', 'locale': 'en_US', 'symbol': 'L', 'salary': (60000, 220000), 'json': 'sheerid_md.json'},
    'ME': {'name': 'Montenegro', 'flag': '🇲🇪', 'locale': 'en_US', 'symbol': '€', 'salary': (20000, 70000), 'json': 'sheerid_me.json'},
    'MK': {'name': 'North Macedonia', 'flag': '🇲🇰', 'locale': 'en_US', 'symbol': 'ден', 'salary': (300000, 900000), 'json': 'sheerid_mk.json'},
    'MN': {'name': 'Mongolia', 'flag': '🇲🇳', 'locale': 'en_US', 'symbol': '₮', 'salary': (8000000, 22000000), 'json': 'sheerid_mn.json'},
    'MT': {'name': 'Malta', 'flag': '🇲🇹', 'locale': 'en_US', 'symbol': '€', 'salary': (28000, 85000), 'json': 'sheerid_mt.json'},
    'MV': {'name': 'Maldives', 'flag': '🇲🇻', 'locale': 'en_US', 'symbol': 'Rf', 'salary': (100000, 500000), 'json': 'sheerid_mv.json'},
    'MX2': {'name': 'Mexico (North)', 'flag': '🇲🇽', 'locale': 'en_US', 'symbol': '$', 'salary': (150000, 450000), 'json': 'sheerid_mx2.json'},
    'MY2': {'name': 'Malaysia (Borneo)', 'flag': '🇲🇾', 'locale': 'en_US', 'symbol': 'RM', 'salary': (38000, 110000), 'json': 'sheerid_my2.json'},
    'NG': {'name': 'Nigeria', 'flag': '🇳🇬', 'locale': 'en_US', 'symbol': '₦', 'salary': (500000, 2000000), 'json': 'sheerid_ng.json'},
    'NI': {'name': 'Nicaragua', 'flag': '🇳🇮', 'locale': 'en_US', 'symbol': 'C$', 'salary': (8000, 25000), 'json': 'sheerid_ni.json'},
    'NP': {'name': 'Nepal', 'flag': '🇳🇵', 'locale': 'en_US', 'symbol': '₨', 'salary': (200000, 900000), 'json': 'sheerid_np.json'},
    'OM': {'name': 'Oman', 'flag': '🇴🇲', 'locale': 'en_US', 'symbol': '﷼', 'salary': (15000, 90000), 'json': 'sheerid_om.json'},
    'PL': {'name': 'Poland', 'flag': '🇵🇱', 'locale': 'en_US', 'symbol': 'zł', 'salary': (70000, 260000), 'json': 'sheerid_pl.json'},
    'PR': {'name': 'Puerto Rico', 'flag': '🇵🇷', 'locale': 'en_US', 'symbol': '$', 'salary': (28000, 90000), 'json': 'sheerid_pr.json'},
    'PT': {'name': 'Portugal', 'flag': '🇵🇹', 'locale': 'en_US', 'symbol': '€', 'salary': (22000, 75000), 'json': 'sheerid_pt.json'},
    'QA': {'name': 'Qatar', 'flag': '🇶🇦', 'locale': 'en_US', 'symbol': 'ر.ق', 'salary': (20000, 120000), 'json': 'sheerid_qa.json'},
    'RO': {'name': 'Romania', 'flag': '🇷🇴', 'locale': 'en_US', 'symbol': 'lei', 'salary': (50000, 180000), 'json': 'sheerid_ro.json'},
    'RS': {'name': 'Serbia', 'flag': '🇷🇸', 'locale': 'en_US', 'symbol': 'дин', 'salary': (400000, 1200000), 'json': 'sheerid_rs.json'},
    'RW2': {'name': 'Rwanda Highlands', 'flag': '🇷🇼', 'locale': 'en_US', 'symbol': 'FRw', 'salary': (700000, 2400000), 'json': 'sheerid_rw2.json'},
    'SB': {'name': 'Solomon Islands', 'flag': '🇸🇧', 'locale': 'en_US', 'symbol': '$', 'salary': (60000, 200000), 'json': 'sheerid_sb.json'},
    'SI': {'name': 'Slovenia', 'flag': '🇸🇮', 'locale': 'en_US', 'symbol': '€', 'salary': (24000, 85000), 'json': 'sheerid_si.json'},
    'SK': {'name': 'Slovakia', 'flag': '🇸🇰', 'locale': 'en_US', 'symbol': '€', 'salary': (24000, 85000), 'json': 'sheerid_sk.json'},
    'SL': {'name': 'Sierra Leone', 'flag': '🇸🇱', 'locale': 'en_US', 'symbol': 'Le', 'salary': (500000, 2000000), 'json': 'sheerid_sl.json'},
    'SM': {'name': 'San Marino', 'flag': '🇸🇲', 'locale': 'en_US', 'symbol': '€', 'salary': (25000, 85000), 'json': 'sheerid_sm.json'},
    'SO': {'name': 'Somalia', 'flag': '🇸🇴', 'locale': 'en_US', 'symbol': 'Sh', 'salary': (500000, 2000000), 'json': 'sheerid_so.json'},
    'SS': {'name': 'South Sudan', 'flag': '🇸🇸', 'locale': 'en_US', 'symbol': '£', 'salary': (500000, 2000000), 'json': 'sheerid_ss.json'},
    'ST': {'name': 'Sao Tome and Principe', 'flag': '🇸🇹', 'locale': 'en_US', 'symbol': 'Db', 'salary': (100000, 400000), 'json': 'sheerid_st.json'},
    'SV': {'name': 'El Salvador', 'flag': '🇸🇻', 'locale': 'en_US', 'symbol': '$', 'salary': (5000, 20000), 'json': 'sheerid_sv.json'},
    'TJ': {'name': 'Tajikistan', 'flag': '🇹🇯', 'locale': 'en_US', 'symbol': 'ЅМ', 'salary': (300000, 1100000), 'json': 'sheerid_tj.json'},
    'TM': {'name': 'Turkmenistan', 'flag': '🇹🇲', 'locale': 'en_US', 'symbol': 'm', 'salary': (200000, 800000), 'json': 'sheerid_tm.json'},
    'TN': {'name': 'Tunisia', 'flag': '🇹🇳', 'locale': 'en_US', 'symbol': 'د.ت', 'salary': (12000, 60000), 'json': 'sheerid_tn.json'},
    'UA': {'name': 'Ukraine', 'flag': '🇺🇦', 'locale': 'en_US', 'symbol': '₴', 'salary': (120000, 450000), 'json': 'sheerid_ua.json'},
    'UG2': {'name': 'Uganda West', 'flag': '🇺🇬', 'locale': 'en_US', 'symbol': 'USh', 'salary': (2200000, 9000000), 'json': 'sheerid_ug2.json'},
    'UY2': {'name': 'Uruguay Coast', 'flag': '🇺🇾', 'locale': 'en_US', 'symbol': '$', 'salary': (320000, 1200000), 'json': 'sheerid_uy2.json'},
    'UZ': {'name': 'Uzbekistan', 'flag': '🇺🇿', 'locale': 'en_US', 'symbol': 'soʻm', 'salary': (5000000, 20000000), 'json': 'sheerid_uz.json'},
    'VA': {'name': 'Vatican City', 'flag': '🇻🇦', 'locale': 'en_US', 'symbol': '€', 'salary': (30000, 90000), 'json': 'sheerid_va.json'},
    'VI': {'name': 'U.S. Virgin Islands', 'flag': '🇻🇮', 'locale': 'en_US', 'symbol': '$', 'salary': (28000, 85000), 'json': 'sheerid_vi.json'},
    'VN2': {'name': 'Vietnam Highlands', 'flag': '🇻🇳', 'locale': 'en_US', 'symbol': '₫', 'salary': (120000000, 520000000), 'json': 'sheerid_vn2.json'},
    'WS': {'name': 'Samoa', 'flag': '🇼🇸', 'locale': 'en_US', 'symbol': 'T', 'salary': (20000, 70000), 'json': 'sheerid_ws.json'},
    'X01': {'name': 'Aruba', 'flag': '🇦🇼', 'locale': 'en_US', 'symbol': 'ƒ', 'salary': (20000, 70000), 'json': ''},
    'X02': {'name': 'Bermuda', 'flag': '🇧🇲', 'locale': 'en_US', 'symbol': '$', 'salary': (40000, 120000), 'json': ''},
    'X03': {'name': 'Cayman Islands', 'flag': '🇰🇾', 'locale': 'en_US', 'symbol': '$', 'salary': (35000, 110000), 'json': ''},
    'X04': {'name': 'Curacao', 'flag': '🇨🇼', 'locale': 'en_US', 'symbol': 'ƒ', 'salary': (25000, 80000), 'json': ''},
    'X05': {'name': 'Fiji', 'flag': '🇫🇯', 'locale': 'en_US', 'symbol': '$', 'salary': (20000, 70000), 'json': ''},
    'X06': {'name': 'Gibraltar', 'flag': '🇬🇮', 'locale': 'en_US', 'symbol': '£', 'salary': (28000, 90000), 'json': ''},
    'X07': {'name': 'Guadeloupe', 'flag': '🇬🇵', 'locale': 'en_US', 'symbol': '€', 'salary': (24000, 85000), 'json': ''},
    'X08': {'name': 'Guam', 'flag': '🇬🇺', 'locale': 'en_US', 'symbol': '$', 'salary': (28000, 90000), 'json': ''},
    'X09': {'name': 'Isle of Man', 'flag': '🇮🇲', 'locale': 'en_US', 'symbol': '£', 'salary': (32000, 100000), 'json': ''},
    'X10': {'name': 'Jersey', 'flag': '🇯🇪', 'locale': 'en_US', 'symbol': '£', 'salary': (32000, 100000), 'json': ''},
    'X11': {'name': 'Kosovo', 'flag': '🇽🇰', 'locale': 'en_US', 'symbol': '€', 'salary': (20000, 65000), 'json': ''},
    'X12': {'name': 'La Reunion', 'flag': '🇷🇪', 'locale': 'en_US', 'symbol': '€', 'salary': (24000, 85000), 'json': ''},
    'X13': {'name': 'Liege Region', 'flag': '🇧🇪', 'locale': 'en_US', 'symbol': '€', 'salary': (28000, 95000), 'json': ''},
    'X14': {'name': 'Macau', 'flag': '🇲🇴', 'locale': 'en_US', 'symbol': 'MOP$', 'salary': (120000, 450000), 'json': ''},
    'X15': {'name': 'Martinique', 'flag': '🇲🇶', 'locale': 'en_US', 'symbol': '€', 'salary': (24000, 85000), 'json': ''},
    'X16': {'name': 'Mayotte', 'flag': '🇾🇹', 'locale': 'en_US', 'symbol': '€', 'salary': (20000, 70000), 'json': ''},
    'X17': {'name': 'Macao Peninsula', 'flag': '🇲🇴', 'locale': 'en_US', 'symbol': 'MOP$', 'salary': (120000, 450000), 'json': ''},
    'X18': {'name': 'Monaco Principality', 'flag': '🇲🇨', 'locale': 'en_US', 'symbol': '€', 'salary': (60000, 160000), 'json': ''},
    'X19': {'name': 'New Caledonia', 'flag': '🇳🇨', 'locale': 'en_US', 'symbol': '₣', 'salary': (24000, 85000), 'json': ''},
    'X20': {'name': 'Northern Cyprus', 'flag': '🇨🇾', 'locale': 'en_US', 'symbol': '₺', 'salary': (20000, 70000), 'json': ''},
    'X21': {'name': 'Northern Ireland', 'flag': '🇬🇧', 'locale': 'en_US', 'symbol': '£', 'salary': (25000, 90000), 'json': ''},
    'X22': {'name': 'Papua New Guinea', 'flag': '🇵🇬', 'locale': 'en_US', 'symbol': 'K', 'salary': (20000, 70000), 'json': ''},
    'X23': {'name': 'Pitcairn Islands', 'flag': '🇵🇳', 'locale': 'en_US', 'symbol': '$', 'salary': (20000, 70000), 'json': ''},
    'X24': {'name': 'Qeshm Free Zone', 'flag': '🇮🇷', 'locale': 'en_US', 'symbol': '﷼', 'salary': (70000000, 220000000), 'json': ''},
    'X25': {'name': 'Saint Pierre and Miquelon', 'flag': '🇵🇲', 'locale': 'en_US', 'symbol': '€', 'salary': (24000, 85000), 'json': ''},
    'X26': {'name': 'Sint Maarten', 'flag': '🇸🇽', 'locale': 'en_US', 'symbol': 'ƒ', 'salary': (25000, 80000), 'json': ''},
    'X27': {'name': 'Tahiti', 'flag': '🇵🇫', 'locale': 'en_US', 'symbol': '₣', 'salary': (24000, 85000), 'json': ''},
    'X28': {'name': 'Tasmania', 'flag': '🇦🇺', 'locale': 'en_US', 'symbol': '$', 'salary': (45000, 130000), 'json': ''},
    'X29': {'name': 'Tibet', 'flag': '🚩', 'locale': 'en_US', 'symbol': '¥', 'salary': (100000, 500000), 'json': ''},
    'X30': {'name': 'Tokelau', 'flag': '🇹🇰', 'locale': 'en_US', 'symbol': '$', 'salary': (15000, 50000), 'json': ''},
    'X31': {'name': 'Turks and Caicos', 'flag': '🇹🇨', 'locale': 'en_US', 'symbol': '$', 'salary': (28000, 90000), 'json': ''},
    'X32': {'name': 'Wallis and Futuna', 'flag': '🇼🇫', 'locale': 'en_US', 'symbol': '₣', 'salary': (20000, 70000), 'json': ''},
    'X33': {'name': 'Yukon', 'flag': '🇨🇦', 'locale': 'en_US', 'symbol': '$', 'salary': (42000, 110000), 'json': ''},
    'X34': {'name': 'Zanzibar', 'flag': '🇹🇿', 'locale': 'en_US', 'symbol': 'TSh', 'salary': (1200000, 5200000), 'json': ''},
    'YE2': {'name': 'Yemen (South)', 'flag': '🇾🇪', 'locale': 'en_US', 'symbol': '﷼', 'salary': (520000, 2200000), 'json': 'sheerid_ye2.json'},
    'ZM2': {'name': 'Zambia Copperbelt', 'flag': '🇿🇲', 'locale': 'en_US', 'symbol': 'ZK', 'salary': (6000, 25000), 'json': 'sheerid_zm2.json'},
    'ZW2': {'name': 'Zimbabwe Midlands', 'flag': '🇿🇼', 'locale': 'en_US', 'symbol': '$', 'salary': (400, 1700), 'json': 'sheerid_zw2.json'},
}

COUNTRIES.update({k: v for k, v in EXTRA_COUNTRIES.items() if k not in COUNTRIES})
COUNTRY_COUNT = len(COUNTRIES)

def init_db():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    # Create table with memory columns
    c.execute('''CREATE TABLE IF NOT EXISTS authorized_users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        added_by INTEGER,
        added_at TEXT,
        is_active INTEGER DEFAULT 1,
        last_country TEXT,
        last_doc_type TEXT,
        is_super_admin INTEGER DEFAULT 0
    )''')
    
    # Add columns if they don't exist (for existing databases)
    try:
        c.execute('ALTER TABLE authorized_users ADD COLUMN last_country TEXT')
    except:
        pass
    try:
        c.execute('ALTER TABLE authorized_users ADD COLUMN last_doc_type TEXT')
    except:
        pass
    try:
        c.execute('ALTER TABLE authorized_users ADD COLUMN is_super_admin INTEGER DEFAULT 0')
    except:
        pass
    
    conn.commit()
    conn.close()
    
    try:
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO authorized_users (user_id, username, first_name, added_by, added_at, is_active, is_super_admin) VALUES (?, ?, ?, ?, ?, ?, 1)',
                  (SUPER_ADMIN_ID, 'Adeebaabkhan', 'Adeebaabkhan', 0, datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'), 1))
        conn.commit()
        conn.close()
    except:
        pass

init_db()

MAIN_MENU, SELECT_DOC, SELECT_COUNTRY, INPUT_SCHOOL, INPUT_QTY, STUDENT_SELECT_COLLEGE, ADD_USER_INPUT = range(7)

def now():
    return datetime.now(timezone.utc)

def is_super_admin(uid):
    if int(uid) in ADMIN_IDS:
        return True

    try:
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute('SELECT is_super_admin FROM authorized_users WHERE user_id = ?', (uid,))
        result = c.fetchone()
        conn.close()
        return result and result[0] == 1
    except Exception as e:
        logger.error(f"❌ Failed to read super admin status for {uid}: {e}")
        return False

def is_authorized(uid):
    if is_super_admin(uid):
        return True
    try:
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute('SELECT is_active FROM authorized_users WHERE user_id = ?', (uid,))
        result = c.fetchone()
        conn.close()
        return result and result[0] == 1
    except:
        return False

def get_authorized_user(user_id):
    try:
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute(
            'SELECT user_id, username, first_name, added_by, added_at, is_active FROM authorized_users WHERE user_id = ?',
            (user_id,),
        )
        row = c.fetchone()
        conn.close()

        if not row:
            return None

        return {
            'user_id': row[0],
            'username': row[1],
            'first_name': row[2],
            'added_by': row[3],
            'added_at': row[4],
            'is_active': row[5],
        }
    except Exception as e:
        logger.error(f"❌ Failed to fetch user {user_id}: {e}")
        return None

def add_authorized_user(user_id, username=None, first_name=None, added_by=None):
    try:
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute(
            'SELECT user_id, username, first_name, added_by, added_at, is_active, is_super_admin FROM authorized_users WHERE user_id = ?',
            (user_id,),
        )
        row = c.fetchone()
        conn.close()

        if not row:
            return None

        return {
            'user_id': row[0],
            'username': row[1],
            'first_name': row[2],
            'added_by': row[3],
            'added_at': row[4],
            'is_active': row[5],
            'is_super_admin': row[6],
        }
    except Exception as e:
        logger.error(f"❌ Failed to fetch user {user_id}: {e}")
        return None

def add_authorized_user(user_id, username=None, first_name=None, added_by=None, is_super_admin=False):
    try:
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute(
            'INSERT OR REPLACE INTO authorized_users (user_id, username, first_name, added_by, added_at, is_active, is_super_admin) VALUES (?, ?, ?, ?, ?, 1, ?)',
            (
                int(user_id),
                username or '',
                first_name or '',
                added_by or 0,
                now().strftime('%Y-%m-%d %H:%M:%S'),
                1 if is_super_admin else 0,
            ),
        )
        conn.commit()
        conn.close()
        logger.info(f"✅ Added/updated authorized user {user_id}")
        if is_super_admin:
            ADMIN_IDS.add(int(user_id))
        return True
    except Exception as e:
        logger.error(f"❌ Failed to add user {user_id}: {e}")
        return False


def add_super_admin(user_id, username=None, first_name=None, added_by=None):
    return add_authorized_user(
        user_id,
        username=username,
        first_name=first_name,
        added_by=added_by,
        is_super_admin=True,
    )

def get_last_country(uid):
    """Get user's last used country"""
    try:
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute('SELECT last_country, last_doc_type FROM authorized_users WHERE user_id = ?', (uid,))
        result = c.fetchone()
        conn.close()
        if result and result[0]:
            return result[0], result[1]
        return None, None
    except:
        return None, None

def save_last_country(uid, country_code, doc_type):
    """Save user's last used country"""
    try:
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute('UPDATE authorized_users SET last_country = ?, last_doc_type = ? WHERE user_id = ?', 
                  (country_code, doc_type, uid))
        conn.commit()
        conn.close()
        logger.info(f"✅ Saved country {country_code} for user {uid}")
    except Exception as e:
        logger.error(f"❌ Failed to save country: {e}")

def get_font(size=14, bold=False):
    try:
        if os.name == 'nt':
            return ImageFont.truetype("arialbd.ttf" if bold else "arial.ttf", size)
        for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    except:
        pass
    return ImageFont.load_default()

def download_real_photo(student_id):
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            url = f"https://thispersondoesnotexist.com/?t={int(time.time())}&r={random.randint(1000, 9999)}&s={student_id}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'Accept': 'image/*'}
            response = requests.get(url, timeout=15, headers=headers, stream=True)
            response.raise_for_status()
            photo = Image.open(BytesIO(response.content))
            photo = photo.convert("RGB")
            logger.info(f"✅ Real photo downloaded: {student_id}")
            return photo
        except Exception as e:
            logger.warning(f"⚠️ Photo attempt {attempt+1}/3 failed: {e}")
            if attempt < max_attempts - 1:
                time.sleep(1)
    logger.warning(f"⚠️ Using placeholder for: {student_id}")
    return create_photo_placeholder(student_id)

def create_photo_placeholder(student_id):
    photo = Image.new("RGB", (160, 210), WHITE)
    draw = ImageDraw.Draw(photo)
    draw.rectangle([(0, 0), (160, 210)], outline=BLUE, width=2, fill=LIGHT_GRAY)
    draw.rectangle([(0, 0), (160, 50)], fill=BLUE)
    draw.text((80, 25), "NO PHOTO", fill=WHITE, font=get_font(12, True), anchor="mm")
    draw.text((80, 105), "ID", fill=BLUE, font=get_font(20, True), anchor="mm")
    draw.text((80, 140), student_id[:10], fill=BLACK, font=get_font(9), anchor="mm")
    return photo

def generate_qr_code(student_data, college_data, country_code):
    try:
        qr_data = (f"TYPE:STUDENT_ID\nNAME:{student_data['name']}\nID:{student_data['id']}\nCOLLEGE:{college_data['name']}\nPROGRAM:{student_data['program']}\nCOUNTRY:{country_code}\nISSUED:{now().strftime('%Y-%m-%d')}\nVALID:{(now() + timedelta(days=1460)).strftime('%Y-%m-%d')}")
        qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=4, border=2)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color=BLUE, back_color=WHITE).convert("RGB")
        logger.info(f"✅ QR code generated")
        return qr_img
    except Exception as e:
        logger.error(f"❌ QR Code error: {e}")
        placeholder = Image.new("RGB", (90, 90), WHITE)
        draw = ImageDraw.Draw(placeholder)
        draw.rectangle([(0, 0), (89, 89)], outline=BLUE, width=2)
        draw.text((45, 45), "QR", fill=BLUE, font=get_font(12, True), anchor="mm")
        return placeholder

def generate_random_teacher_id():
    year = datetime.now().year % 100
    code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))
    number = random.randint(10000, 99999)
    return f"TCH{year}{code}{number}"

def generate_random_student_id():
    year = datetime.now().year % 100
    number = random.randint(100000, 999999)
    return f"STU{year}{number}"

def generate_random_profession():
    return random.choice(TEACHER_PROFESSIONS)

def generate_random_program():
    programs = ['Bachelor of Science in Computer Science', 'Bachelor of Science in Mathematics', 'Bachelor of Arts in History', 'Bachelor of Science in Physics', 'Bachelor of Science in Chemistry', 'Bachelor of Science in Biology', 'Bachelor of Commerce', 'Bachelor of Engineering', 'Master of Business Administration', 'Master of Science in IT']
    return random.choice(programs)

def load_colleges(code):
    try:
        jfile = COUNTRIES[code]['json']
        if not os.path.exists(jfile):
            return []
        with open(jfile, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return [{'name': str(c['name']), 'id': str(c['id'])} for c in data if c.get('name') and c.get('id') and c.get('type') in ['UNIVERSITY', 'COLLEGE', 'HEI', 'POST_SECONDARY']]
    except:
        return []

# ============================================================
# SALARY RECEIPT GENERATION
# ============================================================
def gen_salary_receipt_auto(school_name, teacher_name, teacher_id, profession, country_code='IN'):
    cfg = COUNTRIES.get(country_code, COUNTRIES['IN'])
    base_salary = random.randint(*cfg['salary'])
    allowances = int(base_salary * 0.4)
    bonus = int(base_salary * 0.05)
    tax = int(base_salary * 0.08)
    deductions = int(base_salary * 0.03)
    insurance = int(base_salary * 0.02)
    net_salary = base_salary + allowances + bonus - tax - deductions - insurance
    today = datetime.now()
    width, height = 900, 760
    img = Image.new('RGB', (width, height), WHITE)
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (width, 140)], fill=DARK_GRAY)
    logo_x, logo_y = 30, 20
    logo_size = 80
    d.rectangle([(logo_x, logo_y), (logo_x + logo_size, logo_y + logo_size)], fill=WHITE, outline=DARK_GRAY, width=2)
    abbr = ''.join([w[0] for w in school_name.split()[:3]]).upper()[:3]
    d.text((logo_x + logo_size // 2, logo_y + logo_size // 2), abbr, fill=DARK_GRAY, font=get_font(28, True), anchor='mm')
    d.text((logo_x + logo_size + 25, 30), school_name.upper(), fill=WHITE, font=get_font(20, True))
    d.text((logo_x + logo_size + 25, 65), f"{cfg['flag']} {cfg['name']}", fill=GOLD, font=get_font(13))
    d.text((width - 30, 45), "MONTHLY PAYSLIP", fill=GOLD, font=get_font(17, True), anchor='rt')
    d.text((width - 30, 75), "Verified Copy", fill=WHITE, font=get_font(11), anchor='rt')
    y = 155
    d.rectangle([(30, y), (width - 30, y + 50)], outline=BORDER_GRAY, width=1, fill=LIGHT_GRAY)
    pay_period_start = datetime(today.year, today.month, 1)
    pay_period_end = datetime(today.year, today.month, 28) + timedelta(days=2)
    pay_period_end = pay_period_end.replace(day=1) - timedelta(days=1)
    d.text((40, y + 12), f"Payment For: {pay_period_start.strftime('%b %d, %Y')} - {pay_period_end.strftime('%b %d, %Y')}", fill=BLACK, font=get_font(12, True))
    d.text((width - 40, y + 12), f"Issued: {today.strftime('%b %d, %Y')}", fill=BLACK, font=get_font(12, True), anchor='rt')
    d.text((40, y + 30), "Payment Method: Direct Deposit", fill=BLACK, font=get_font(11))
    d.text((width - 40, y + 30), "Currency: {cfg['symbol']}", fill=BLACK, font=get_font(11), anchor='rt')
    y = y + 75
    receipt_no = f"RCP/{country_code}/{random.randint(100000, 999999)}"
    d.text((40, y), f"Receipt No: {receipt_no}", fill=BLACK, font=get_font(12, True))
    d.text((width - 40, y), f"Document ID: {random.randint(100000, 999999)}", fill=BLACK, font=get_font(12, True), anchor='rt')
    y = 215
    d.text((40, y), "Employee Details", fill=DARK_GRAY, font=get_font(14, True))
    y += 28
    d.text((40, y), "Name", fill=BLACK, font=get_font(12, True))
    d.text((180, y), teacher_name.upper(), fill=BLUE, font=get_font(13, True))
    d.text((520, y), "Employee ID", fill=BLACK, font=get_font(12, True))
    d.text((700, y), teacher_id, fill=RED, font=get_font(13, True))
    y += 28
    d.text((40, y), "Role", fill=BLACK, font=get_font(12, True))
    d.text((180, y), profession, fill=BLACK, font=get_font(12))
    d.text((520, y), "Department", fill=BLACK, font=get_font(12, True))
    d.text((700, y), f"{profession.split()[0]} Dept", fill=BLACK, font=get_font(12))

    y += 60
    d.text((40, y), "Earnings", fill=DARK_GRAY, font=get_font(14, True))
    d.text((520, y), "Deductions", fill=DARK_GRAY, font=get_font(14, True))
    y += 25
    # Earnings
    d.text((40, y), "Base Salary", fill=BLACK, font=get_font(12))
    d.text((260, y), f"{cfg['symbol']}{base_salary:,}", fill=GREEN, font=get_font(12, True), anchor='rt')
    y += 22
    d.text((40, y), "Allowances", fill=BLACK, font=get_font(12))
    d.text((260, y), f"{cfg['symbol']}{allowances:,}", fill=GREEN, font=get_font(12, True), anchor='rt')
    y += 22
    d.text((40, y), "Bonus", fill=BLACK, font=get_font(12))
    d.text((260, y), f"{cfg['symbol']}{bonus:,}", fill=GREEN, font=get_font(12, True), anchor='rt')
    earnings_total = base_salary + allowances + bonus

    # Deductions
    y = 328
    d.text((520, y), "Tax (8%)", fill=BLACK, font=get_font(12))
    d.text((760, y), f"-{cfg['symbol']}{tax:,}", fill=RED, font=get_font(12, True), anchor='rt')
    y += 22
    d.text((520, y), "Pension", fill=BLACK, font=get_font(12))
    d.text((760, y), f"-{cfg['symbol']}{deductions:,}", fill=RED, font=get_font(12, True), anchor='rt')
    y += 22
    d.text((520, y), "Insurance", fill=BLACK, font=get_font(12))
    d.text((760, y), f"-{cfg['symbol']}{insurance:,}", fill=RED, font=get_font(12, True), anchor='rt')
    total_deductions = tax + deductions + insurance

    y += 40
    d.rectangle([(30, y), (width - 30, y + 60)], outline=BORDER_GRAY, width=2, fill=LIGHT_GRAY)
    d.text((40, y + 12), "Gross Earnings", fill=BLACK, font=get_font(12, True))
    d.text((260, y + 12), f"{cfg['symbol']}{earnings_total:,}", fill=BLACK, font=get_font(12, True), anchor='rt')
    d.text((520, y + 12), "Total Deductions", fill=BLACK, font=get_font(12, True))
    d.text((760, y + 12), f"-{cfg['symbol']}{total_deductions:,}", fill=BLACK, font=get_font(12, True), anchor='rt')
    d.text((40, y + 35), "Net Salary", fill=BLACK, font=get_font(13, True))
    d.text((260, y + 35), f"{cfg['symbol']}{net_salary:,}", fill=BLUE, font=get_font(14, True), anchor='rt')
    d.text((520, y + 35), "Status", fill=BLACK, font=get_font(13, True))
    d.text((760, y + 35), "PAID", fill=GREEN, font=get_font(14, True), anchor='rt')

    y += 100
    box_height = 140
    d.rectangle([(30, y), (width - 30, y + box_height)], outline=GREEN, width=3, fill=LIGHT_GRAY)
    d.rectangle([(30, y), (width - 30, y + 35)], fill=GREEN)
    d.text((40, y + 10), "✅ PAYMENT CONFIRMED", fill=WHITE, font=get_font(14, True))
    txn_id = f"TXN{random.randint(1000000, 9999999)}"
    bank_ref = f"REF{random.randint(100000, 999999)}"
    d.text((40, y + 55), f"Transaction ID: {txn_id}", fill=BLACK, font=get_font(12, True))
    d.text((40, y + 80), f"Bank Reference: {bank_ref}", fill=BLACK, font=get_font(12, True))
    d.text((40, y + 105), "Payment Channel: ACH", fill=BLACK, font=get_font(11))
    d.text((width - 220, y + 55), "Authorized Signature", fill=BLACK, font=get_font(11))
    d.line([(width - 220, y + 90), (width - 40, y + 90)], fill=BORDER_GRAY, width=2)
    d.text((width - 40, y + 95), "HR Manager", fill=BLACK, font=get_font(10), anchor='rt')
    y = 720
    footer_text = f"Generated: {today.strftime('%m/%d/%Y %H:%M:%S')} UTC | Country: {cfg['name']} | Authentic Document"
    d.text((40, y), footer_text, fill=DARK_GRAY, font=get_font(10))
    return img

# ============================================================
# TEACHER ID CARD GENERATION
# ============================================================
def gen_teacher_id_auto(school_name, teacher_name, teacher_id, profession, country_code='IN'):
    cfg = COUNTRIES.get(country_code, COUNTRIES['IN'])
    width, height = 920, 600
    img = Image.new('RGB', (width, height), WHITE)
    d = ImageDraw.Draw(img)
    photo = download_real_photo(teacher_id)
    d.rectangle([(0, 0), (width, 140)], fill=BLUE)
    logo_x, logo_y = 30, 20
    logo_size = 100
    d.rectangle([(logo_x, logo_y), (logo_x + logo_size, logo_y + logo_size)], fill=WHITE, outline=BLUE, width=2)
    abbr = ''.join([w[0] for w in school_name.split()[:3]]).upper()[:3]
    d.text((logo_x + logo_size // 2, logo_y + logo_size // 2), abbr, fill=BLUE, font=get_font(36, True), anchor='mm')
    d.text((160, 35), school_name.upper(), fill=WHITE, font=get_font(21, True))
    d.text((160, 75), f"{cfg['flag']} {cfg['name']}", fill=WHITE, font=get_font(13))
    d.text((width - 40, 35), "TEACHER", fill=WHITE, font=get_font(19, True), anchor='rt')
    d.text((width - 40, 70), "ID CARD", fill=WHITE, font=get_font(19, True), anchor='rt')
    d.text((width - 40, 110), cfg['name'], fill=GOLD, font=get_font(12), anchor='rt')
    y = 180
    photo_x, photo_y = 40, y
    photo_w, photo_h = 160, 210
    photo_resized = photo.resize((photo_w, photo_h), Image.Resampling.LANCZOS)
    d.rectangle([(photo_x - 2, photo_y - 2), (photo_x + photo_w + 2, photo_y + photo_h + 2)], outline=BLUE, width=3, fill=WHITE)
    img.paste(photo_resized, (photo_x, photo_y))
    logger.info(f"✅ Teacher photo embedded at ({photo_x}, {photo_y})")
    detail_x = 230
    d.text((detail_x, y), "Name:", fill=BLACK, font=get_font(13, True))
    name_band = [(detail_x, y + 22), (detail_x + 440, y + 58)]
    d.rounded_rectangle(name_band, radius=8, fill=WHITE, outline=BLUE, width=2)
    d.text(((name_band[0][0] + name_band[1][0]) // 2, y + 40), teacher_name.upper(), fill=BLUE, font=get_font(21, True), anchor='mm')
    y += 75
    d.text((detail_x, y), "Teacher ID:", fill=BLACK, font=get_font(13, True))
    id_band = [(detail_x, y + 22), (detail_x + 300, y + 58)]
    d.rounded_rectangle(id_band, radius=8, fill=WHITE, outline=RED, width=2)
    d.text(((id_band[0][0] + id_band[1][0]) // 2, y + 40), teacher_id, fill=RED, font=get_font(19, True), anchor='mm')
    y += 75
    d.text((detail_x, y), "Profession:", fill=BLACK, font=get_font(13, True))
    d.text((detail_x, y + 28), profession, fill=BLACK, font=get_font(12))
    y += 70
    d.text((detail_x, y), "Department:", fill=BLACK, font=get_font(13, True))
    d.text((detail_x, y + 28), f"{profession.split()[0]} Department", fill=BLACK, font=get_font(12))
    today = datetime.now()
    expiry = today + timedelta(days=1460)
    d.text((40, photo_y + photo_h + 20), f"Issue Date: {today.strftime('%m/%d/%Y')}", fill=BLACK, font=get_font(11, True))
    d.text((40, photo_y + photo_h + 42), f"Valid Until: {expiry.strftime('%m/%d/%Y')}", fill=BLACK, font=get_font(11, True))
    reg_no = f"REG/{country_code}/{random.randint(100000, 999999)}"
    d.text((detail_x, photo_y + photo_h + 20), f"Reg No: {reg_no}", fill=BLACK, font=get_font(11, True))
    try:
        qr_img = generate_qr_code({'name': teacher_name, 'id': teacher_id, 'program': profession}, {'name': school_name, 'id': ''}, country_code)
        qr_size = 90
        qr_resized = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
        qr_x = width - qr_size - 25
        qr_y = photo_y + photo_h - qr_size - 5
        d.rectangle([(qr_x - 3, qr_y - 3), (qr_x + qr_size + 3, qr_y + qr_size + 3)], outline=BLUE, width=2, fill=WHITE)
        img.paste(qr_resized, (qr_x, qr_y))
        logger.info(f"✅ Teacher QR code embedded at ({qr_x}, {qr_y})")
    except Exception as e:
        logger.error(f"❌ QR error: {e}")
    y = height - 45
    d.text((40, y), f"Official Teacher ID - {cfg['name']}", fill=BLUE, font=get_font(12, True))
    d.text((40, y + 20), f"Generated: {today.strftime('%m/%d/%Y %H:%M:%S')} UTC", fill=BLUE, font=get_font(10))
    d.text((width - 40, y + 8), "AUTHORIZED DOCUMENT", fill=BLUE, font=get_font(11, True), anchor='rt')
    return img

# ============================================================
# STUDENT ID CARD GENERATION
# ============================================================
def gen_student_id_auto(school_name, student_name, student_id, program, country_code='IN'):
    cfg = COUNTRIES.get(country_code, COUNTRIES['IN'])
    width, height = 920, 600
    img = Image.new('RGB', (width, height), WHITE)
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (width, height)], fill=(247, 248, 250))
    d.rectangle([(20, 20), (width - 20, height - 20)], outline=BORDER_GRAY, width=2)
    photo = download_real_photo(student_id)
    d.rectangle([(0, 0), (width, 140)], fill=BLUE)
    d.rectangle([(0, 110), (width, 140)], fill=(14, 71, 161))
    logo_x, logo_y = 30, 20
    logo_size = 100
    d.rectangle([(logo_x, logo_y), (logo_x + logo_size, logo_y + logo_size)], fill=WHITE, outline=BLUE, width=2)
    abbr = ''.join([w[0] for w in school_name.split()[:3]]).upper()[:3]
    d.text((logo_x + logo_size // 2, logo_y + logo_size // 2), abbr, fill=BLUE, font=get_font(36, True), anchor='mm')
    d.text((160, 35), school_name.upper(), fill=WHITE, font=get_font(21, True))
    d.text((160, 75), f"{cfg['flag']} {cfg['name']}", fill=WHITE, font=get_font(13))
    d.text((width - 40, 35), "STUDENT", fill=WHITE, font=get_font(19, True), anchor='rt')
    d.text((width - 40, 70), "ID CARD", fill=WHITE, font=get_font(19, True), anchor='rt')
    d.text((width - 40, 110), cfg['name'], fill=GOLD, font=get_font(12), anchor='rt')
    y = 180
    photo_x, photo_y = 40, y
    photo_w, photo_h = 160, 210
    photo_resized = photo.resize((photo_w, photo_h), Image.Resampling.LANCZOS)
    d.rectangle([(photo_x - 2, photo_y - 2), (photo_x + photo_w + 2, photo_y + photo_h + 2)], outline=BLUE, width=3, fill=WHITE)
    img.paste(photo_resized, (photo_x, photo_y))
    logger.info(f"✅ Student photo embedded at ({photo_x}, {photo_y})")
    detail_x = 230
    d.text((detail_x, y), "Name:", fill=BLACK, font=get_font(13, True))
    name_band = [(detail_x, y + 22), (detail_x + 440, y + 58)]
    d.rounded_rectangle(name_band, radius=8, fill=WHITE, outline=BLUE, width=2)
    d.text(((name_band[0][0] + name_band[1][0]) // 2, y + 40), student_name.upper(), fill=BLUE, font=get_font(21, True), anchor='mm')
    y += 75
    d.text((detail_x, y), "Student ID:", fill=BLACK, font=get_font(13, True))
    id_band = [(detail_x, y + 22), (detail_x + 300, y + 58)]
    d.rounded_rectangle(id_band, radius=8, fill=WHITE, outline=RED, width=2)
    d.text(((id_band[0][0] + id_band[1][0]) // 2, y + 40), student_id, fill=RED, font=get_font(19, True), anchor='mm')
    y += 75
    d.text((detail_x, y), "Program:", fill=BLACK, font=get_font(13, True))
    program_short = program[:40] if len(program) > 40 else program
    d.text((detail_x, y + 28), program_short, fill=BLACK, font=get_font(11))
    y += 70
    d.text((detail_x, y), "Year:", fill=BLACK, font=get_font(13, True))
    d.text((detail_x, y + 28), "2nd Year", fill=BLACK, font=get_font(12))
    y += 65
    d.text((detail_x, y), "Issued By:", fill=BLACK, font=get_font(12, True))
    d.text((detail_x + 120, y + 25), "Registrar", fill=BLACK, font=get_font(11), anchor='mm')
    d.line([(detail_x + 60, y + 32), (detail_x + 180, y + 32)], fill=BORDER_GRAY, width=2)
    today = datetime.now()
    expiry = today + timedelta(days=1460)
    d.text((40, photo_y + photo_h + 20), f"Issued: {today.strftime('%m/%d/%Y')}", fill=BLACK, font=get_font(11, True))
    d.text((40, photo_y + photo_h + 42), f"Valid: {expiry.strftime('%m/%d/%Y')}", fill=BLACK, font=get_font(11, True))
    reg_no = f"REG/{country_code}/{random.randint(100000, 999999)}"
    d.text((detail_x, photo_y + photo_h + 20), f"Reg No: {reg_no}", fill=BLACK, font=get_font(11, True))
    card_no = f"CARD-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    d.text((detail_x, photo_y + photo_h + 42), f"Card No: {card_no}", fill=BLACK, font=get_font(11, True))
    holo_x, holo_y = width - 170, photo_y + photo_h - 20
    d.ellipse([(holo_x, holo_y), (holo_x + 60, holo_y + 60)], fill=(232, 213, 128), outline=GOLD, width=2)
    d.text((holo_x + 30, holo_y + 30), "VALID", fill=WHITE, font=get_font(10, True), anchor='mm')
    try:
        qr_img = generate_qr_code({'name': student_name, 'id': student_id, 'program': program}, {'name': school_name, 'id': ''}, country_code)
        qr_size = 90
        qr_resized = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
        qr_x = width - qr_size - 25
        qr_y = photo_y + photo_h - qr_size - 5
        d.rectangle([(qr_x - 3, qr_y - 3), (qr_x + qr_size + 3, qr_y + qr_size + 3)], outline=BLUE, width=2, fill=WHITE)
        img.paste(qr_resized, (qr_x, qr_y))
        logger.info(f"✅ Student QR code embedded at ({qr_x}, {qr_y})")
    except Exception as e:
        logger.error(f"❌ QR error: {e}")
    y = height - 45
    d.text((40, y), f"Official Student ID - {cfg['name']}", fill=BLUE, font=get_font(12, True))
    d.text((40, y + 20), f"Generated: {today.strftime('%m/%d/%Y %H:%M:%S')} UTC", fill=BLUE, font=get_font(10))
    d.text((width - 40, y + 8), "AUTHORIZED DOCUMENT", fill=BLUE, font=get_font(11, True), anchor='rt')
    return img

# ============================================================
# BOT HANDLERS WITH MEMORY & TAP-TO-COPY
# ============================================================
def send_main_menu(context: CallbackContext, chat, uid: int, name: str):
    keyboard = [
        [InlineKeyboardButton("👨‍🏫 Teachers", callback_data='teacher')],
        [InlineKeyboardButton("🎓 Students", callback_data='student')],
        [InlineKeyboardButton("ℹ️ Info", callback_data='info')],
    ]
    role = "🔴 SUPER ADMIN" if is_super_admin(uid) else "🟢 User"
    text = (
        f"✅ Welcome {name}\nRole: {role}\n\n"
        f"🤖 100 COUNTRIES BOT\n📸 Real Photos + QR Codes\n🧠 Smart Memory\n📋 Tap-to-Copy Names\n\n"
        f"📅 {now().strftime('%Y-%m-%d %H:%M:%S')}\n👤 Adeebaabkhan"
    )

    if chat:
        chat.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        context.bot.send_message(chat_id=uid, text=text, reply_markup=InlineKeyboardMarkup(keyboard))
    return MAIN_MENU


def start(update: Update, context: CallbackContext):
    uid = update.effective_user.id
    name = update.effective_user.first_name or "User"
    message = update.message
    if not message and update.callback_query:
        message = update.callback_query.message

    if not is_authorized(uid):
        if message:
            message.reply_text("❌ ACCESS DENIED\n\nContact: @itsmeaab")
        else:
            context.bot.send_message(chat_id=uid, text="❌ ACCESS DENIED\n\nContact: @itsmeaab")
        return ConversationHandler.END

    return send_main_menu(context, message, uid, name)

def add_user_command(update: Update, context: CallbackContext):
    uid = update.effective_user.id
    if not is_super_admin(uid):
        update.message.reply_text("❌ Only the super admin can add users")
        return

    if not context.args:
        update.message.reply_text("Usage: /adduser <user_id> [username] [first name]")
        return

    try:
        target_id = int(context.args[0])
    except ValueError:
        update.message.reply_text("❌ user_id must be a number")
        return

    username = context.args[1].lstrip('@') if len(context.args) > 1 else None
    first_name = ' '.join(context.args[2:]) if len(context.args) > 2 else None

    existing = get_authorized_user(target_id)
    label = username or first_name or str(target_id)

    if add_authorized_user(target_id, username=username, first_name=first_name, added_by=uid):
        if existing:
            status = "reactivated" if existing.get('is_active') == 0 else "updated"
            update.message.reply_text(f"✅ {label} {status} and authorized")
        else:
            update.message.reply_text(f"✅ Added {label} to authorized users")
    else:
        update.message.reply_text("❌ Could not save user. Check logs for details.")

def add_user_inline_input(update: Update, context: CallbackContext):
    uid = update.effective_user.id
    if not is_super_admin(uid):
        update.message.reply_text("❌ Only the super admin can add users")
        return ADD_USER_INPUT

    parts = update.message.text.split()
    if not parts:
        update.message.reply_text("Usage: user_id [username] [first name]\n\n/cancel")
        return ADD_USER_INPUT

    try:
        target_id = int(parts[0])
    except ValueError:
        update.message.reply_text("❌ user_id must be a number\n\n/cancel")
        return ADD_USER_INPUT

    username = parts[1].lstrip('@') if len(parts) > 1 else None
    first_name = ' '.join(parts[2:]) if len(parts) > 2 else None

    existing = get_authorized_user(target_id)
    label = username or first_name or str(target_id)

    existing = get_authorized_user(target_id)
    label = username or first_name or str(target_id)

    if add_super_admin(target_id, username=username, first_name=first_name, added_by=uid):
        if existing:
            status = "promoted to super admin" if not existing.get('is_super_admin') else "already a super admin"
            update.message.reply_text(f"✅ {label} {status}")
        else:
            update.message.reply_text(f"✅ Added {label} as a super admin")
    else:
        update.message.reply_text("❌ Could not promote user. Check logs for details.")

def add_user_inline_input(update: Update, context: CallbackContext):
    uid = update.effective_user.id
    if not is_super_admin(uid):
        update.message.reply_text("❌ Only the super admin can add users")
        return ADD_USER_INPUT

    parts = update.message.text.split()
    if not parts:
        update.message.reply_text("Usage: user_id [username] [first name]\n\n/cancel")
        return ADD_USER_INPUT

    try:
        target_id = int(parts[0])
    except ValueError:
        update.message.reply_text("❌ user_id must be a number\n\n/cancel")
        return ADD_USER_INPUT

    username = parts[1].lstrip('@') if len(parts) > 1 else None
    first_name = ' '.join(parts[2:]) if len(parts) > 2 else None

    existing = get_authorized_user(target_id)
    label = username or first_name or str(target_id)

    if add_authorized_user(target_id, username=username, first_name=first_name, added_by=uid):
        if existing:
            status = "reactivated" if existing.get('is_active') == 0 else "updated"
            update.message.reply_text(f"✅ {label} {status} and authorized")
        else:
            update.message.reply_text(f"✅ Added {label} to authorized users")
    else:
        update.message.reply_text("❌ Could not save user. Check logs for details.")

    return ADD_USER_INPUT

def main_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    uid = query.from_user.id

    if query.data == 'add_user':
        if not is_super_admin(uid):
            query.answer("Admins only", show_alert=True)
            return MAIN_MENU
        query.edit_message_text(
            "➕ Add a user\n\nSend: user_id [username] [first name]\n\n/cancel",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data='back')]])
        )
        return ADD_USER_INPUT

    if query.data == 'teacher':
        last_country, last_doc_type = get_last_country(uid)
        if last_country and last_country in COUNTRIES and last_doc_type == 'teacher':
            cfg = COUNTRIES[last_country]
            keyboard = [
                [InlineKeyboardButton("✅ YES", callback_data=f'use_last_tc_{last_country}')],
                [InlineKeyboardButton("❌ NO", callback_data='choose_new_teacher')]
            ]
            query.edit_message_text(
                f"👨‍🏫 TEACHER DOCUMENTS\n\n"
                f"Use {cfg['flag']} `{cfg['name']}` again?\n\n"
                f"💡 Tap name to copy",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            context.user_data['type'] = 'teacher'
            return SELECT_COUNTRY
        else:
            countries_list = list(COUNTRIES.items())
            keyboard = [[InlineKeyboardButton(f"{v['flag']} {v['name']}", callback_data=f'tc_{k}')] for k, v in countries_list[:10]]
            keyboard.append([InlineKeyboardButton("➡️ More", callback_data='more_t')])
            keyboard.append([InlineKeyboardButton("🔙 Back", callback_data='back')])
            query.edit_message_text("👨‍🏫 SELECT COUNTRY:", reply_markup=InlineKeyboardMarkup(keyboard))
            context.user_data['type'] = 'teacher'
            return SELECT_COUNTRY
            
    elif query.data == 'student':
        last_country, last_doc_type = get_last_country(uid)
        if last_country and last_country in COUNTRIES and last_doc_type == 'student':
            cfg = COUNTRIES[last_country]
            keyboard = [
                [InlineKeyboardButton("✅ YES", callback_data=f'use_last_sc_{last_country}')],
                [InlineKeyboardButton("❌ NO", callback_data='choose_new_student')]
            ]
            query.edit_message_text(
                f"🎓 STUDENT DOCUMENTS\n\n"
                f"Use {cfg['flag']} `{cfg['name']}` again?\n\n"
                f"💡 Tap name to copy",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            context.user_data['type'] = 'student'
            return SELECT_COUNTRY
        else:
            countries_list = list(COUNTRIES.items())
            keyboard = [[InlineKeyboardButton(f"{v['flag']} {v['name']}", callback_data=f'sc_{k}')] for k, v in countries_list[:10]]
            keyboard.append([InlineKeyboardButton("➡️ More", callback_data='more_s')])
            keyboard.append([InlineKeyboardButton("🔙 Back", callback_data='back')])
            query.edit_message_text("🎓 SELECT COUNTRY:", reply_markup=InlineKeyboardMarkup(keyboard))
            context.user_data['type'] = 'student'
            return SELECT_COUNTRY
            
    elif query.data == 'info':
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back')]]
        query.edit_message_text(
            "ℹ️ BOT FEATURES:\n\n"
            "🧠 Smart Memory\n"
            "📋 Tap-to-Copy Names\n"
            "📸 Real Photos\n"
            "🔳 QR Codes\n"
            f"🌍 {COUNTRY_COUNT}+ Countries\n\n"
            "📱 @itsmeaab",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return MAIN_MENU
    elif query.data == 'back':
        return start(update, context)

def select_country(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    uid = query.from_user.id
    
    if query.data.startswith('use_last_tc_') or query.data.startswith('use_last_sc_'):
        if query.data.startswith('use_last_tc_'):
            code = query.data.replace('use_last_tc_', '')
            doc_type = 'teacher'
        else:
            code = query.data.replace('use_last_sc_', '')
            doc_type = 'student'
        
        context.user_data['country'] = code
        context.user_data['doc_type'] = doc_type
        cfg = COUNTRIES[code]
        
        if doc_type == 'teacher':
            query.edit_message_text(
                f"✅ {cfg['flag']} `{cfg['name']}`\n\n"
                f"📝 Enter School Name:\n\n"
                f"/cancel to go back",
                parse_mode='Markdown'
            )
            return INPUT_SCHOOL
        else:
            colleges = load_colleges(code)
            if not colleges:
                keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back')]]
                query.edit_message_text(f"❌ No colleges for {cfg['name']}\n\n/start", reply_markup=InlineKeyboardMarkup(keyboard))
                return SELECT_COUNTRY
            context.user_data['colleges'] = colleges
            keyboard = [[InlineKeyboardButton(f"🏫 {c['name'][:50]}", callback_data=f'col_{i}')] for i, c in enumerate(colleges[:10])]
            if len(colleges) > 10:
                keyboard.append([InlineKeyboardButton("🔀 More", callback_data='more_col')])
            keyboard.append([InlineKeyboardButton("🔙 Back", callback_data='back')])
            query.edit_message_text(
                f"✅ {cfg['flag']} `{cfg['name']}`\n\n"
                f"🏫 Select College ({len(colleges)}):\n\n"
                f"📸 REAL PHOTOS\n🔳 QR CODES",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            return STUDENT_SELECT_COLLEGE
    
    if query.data == 'choose_new_teacher':
        countries_list = list(COUNTRIES.items())
        keyboard = [[InlineKeyboardButton(f"{v['flag']} {v['name']}", callback_data=f'tc_{k}')] for k, v in countries_list[:10]]
        keyboard.append([InlineKeyboardButton("➡️ More", callback_data='more_t')])
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data='back')])
        query.edit_message_text("👨‍🏫 SELECT COUNTRY:", reply_markup=InlineKeyboardMarkup(keyboard))
        return SELECT_COUNTRY
        
    if query.data == 'choose_new_student':
        countries_list = list(COUNTRIES.items())
        keyboard = [[InlineKeyboardButton(f"{v['flag']} {v['name']}", callback_data=f'sc_{k}')] for k, v in countries_list[:10]]
        keyboard.append([InlineKeyboardButton("➡️ More", callback_data='more_s')])
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data='back')])
        query.edit_message_text("🎓 SELECT COUNTRY:", reply_markup=InlineKeyboardMarkup(keyboard))
        return SELECT_COUNTRY
    
    if query.data in ['more_t', 'more_s']:
        countries_list = list(COUNTRIES.items())
        doc_type = 'tc_' if query.data == 'more_t' else 'sc_'
        keyboard = [[InlineKeyboardButton(f"{v['flag']} {v['name']}", callback_data=f'{doc_type}{k}')] for k, v in countries_list[10:]]
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data='back_countries')])
        query.edit_message_text(f"🌍 ALL {COUNTRY_COUNT} COUNTRIES:", reply_markup=InlineKeyboardMarkup(keyboard))
        return SELECT_COUNTRY
    elif query.data == 'back_countries':
        if context.user_data.get('type') == 'teacher':
            countries_list = list(COUNTRIES.items())
            keyboard = [[InlineKeyboardButton(f"{v['flag']} {v['name']}", callback_data=f'tc_{k}')] for k, v in countries_list[:10]]
            keyboard.append([InlineKeyboardButton("➡️ More", callback_data='more_t')])
            keyboard.append([InlineKeyboardButton("🔙 Back", callback_data='back')])
            query.edit_message_text("👨‍🏫 SELECT COUNTRY:", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            countries_list = list(COUNTRIES.items())
            keyboard = [[InlineKeyboardButton(f"{v['flag']} {v['name']}", callback_data=f'sc_{k}')] for k, v in countries_list[:10]]
            keyboard.append([InlineKeyboardButton("➡️ More", callback_data='more_s')])
            keyboard.append([InlineKeyboardButton("🔙 Back", callback_data='back')])
            query.edit_message_text("🎓 SELECT COUNTRY:", reply_markup=InlineKeyboardMarkup(keyboard))
        return SELECT_COUNTRY
    elif query.data.startswith('tc_'):
        code = query.data.replace('tc_', '')
        context.user_data['country'] = code
        context.user_data['doc_type'] = 'teacher'
        cfg = COUNTRIES[code]
        query.edit_message_text(f"✅ {cfg['flag']} `{cfg['name']}`\n\n📝 Enter School Name:\n\n/cancel", parse_mode='Markdown')
        return INPUT_SCHOOL
    elif query.data.startswith('sc_'):
        code = query.data.replace('sc_', '')
        context.user_data['country'] = code
        context.user_data['doc_type'] = 'student'
        colleges = load_colleges(code)
        cfg = COUNTRIES[code]
        if not colleges:
            keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back')]]
            query.edit_message_text(f"❌ No colleges for {cfg['name']}\n\n/start", reply_markup=InlineKeyboardMarkup(keyboard))
            return SELECT_COUNTRY
        context.user_data['colleges'] = colleges
        keyboard = [[InlineKeyboardButton(f"🏫 {c['name'][:50]}", callback_data=f'col_{i}')] for i, c in enumerate(colleges[:10])]
        if len(colleges) > 10:
            keyboard.append([InlineKeyboardButton("🔀 More", callback_data='more_col')])
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data='back')])
        query.edit_message_text(f"✅ {cfg['flag']} {cfg['name']}\n\n🏫 Select College ({len(colleges)}):", reply_markup=InlineKeyboardMarkup(keyboard))
        return STUDENT_SELECT_COLLEGE

def input_school_name(update: Update, context: CallbackContext):
    school_name = update.message.text.strip()
    if len(school_name) < 3:
        update.message.reply_text("❌ Min 3 characters\n\n/cancel")
        return INPUT_SCHOOL
    context.user_data['school'] = school_name
    country_code = context.user_data['country']
    cfg = COUNTRIES[country_code]
    fake = Faker('en_US')
    teacher_name = fake.name()
    teacher_id = generate_random_teacher_id()
    profession = generate_random_profession()
    context.user_data['teacher_data'] = {'name': teacher_name, 'id': teacher_id, 'profession': profession}
    
    # TAP-TO-COPY FORMAT
    update.message.reply_text(
        f"✅ School: `{school_name}`\n\n"
        f"👤 `{teacher_name}`\n"
        f"🆔 `{teacher_id}`\n"
        f"👔 {profession}\n\n"
        f"🔢 Quantity? (1-50)\n\n"
        f"💡 Tap names to copy\n"
        f"/cancel",
        parse_mode='Markdown'
    )
    return INPUT_QTY

def select_student_college(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == 'more_col':
        colleges = context.user_data.get('colleges', [])
        keyboard = [[InlineKeyboardButton(f"🏫 {c['name'][:50]}", callback_data=f'col_{i}')] for i, c in enumerate(colleges[10:])]
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data='back_col')])
        query.edit_message_text("🏫 More Colleges:", reply_markup=InlineKeyboardMarkup(keyboard))
        return STUDENT_SELECT_COLLEGE
    elif query.data == 'back_col':
        colleges = context.user_data.get('colleges', [])
        keyboard = [[InlineKeyboardButton(f"🏫 {c['name'][:50]}", callback_data=f'col_{i}')] for i, c in enumerate(colleges[:10])]
        if len(colleges) > 10:
            keyboard.append([InlineKeyboardButton("🔀 More", callback_data='more_col')])
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data='back')])
        query.edit_message_text(f"🏫 Select College ({len(colleges)}):", reply_markup=InlineKeyboardMarkup(keyboard))
        return STUDENT_SELECT_COLLEGE
    elif query.data.startswith('col_'):
        idx = int(query.data.replace('col_', ''))
        colleges = context.user_data.get('colleges', [])
        college = colleges[idx] if idx < len(colleges) else colleges[0]
        context.user_data['school'] = college['name']
        context.user_data['college_id'] = college['id']
        query.edit_message_text(
            f"✅ `{college['name']}`\n\n"
            f"🔢 Quantity? (1-50)\n\n"
            f"📸 REAL PHOTOS\n"
            f"💡 Tap to copy\n"
            f"/cancel",
            parse_mode='Markdown'
        )
        return INPUT_QTY

def input_quantity(update: Update, context: CallbackContext):
    try:
        qty = int(update.message.text.strip())
        if qty < 1 or qty > 50:
            update.message.reply_text("❌ Enter 1-50")
            return INPUT_QTY
        
        uid = update.effective_user.id
        country_code = context.user_data['country']
        school_name = context.user_data['school']
        doc_type = context.user_data['doc_type']
        cfg = COUNTRIES[country_code]
        fake = Faker('en_US')
        
        # SAVE COUNTRY TO MEMORY
        save_last_country(uid, country_code, doc_type)
        
        progress_msg = update.message.reply_text(f"⏳ Generating {qty}...\n\n📸 Downloading photos...\n🔳 Creating QR codes...")
        
        if doc_type == 'teacher':
            teacher_data = context.user_data.get('teacher_data', {})
            for i in range(qty):
                try:
                    if i == 0:
                        name = teacher_data['name']
                        tid = teacher_data['id']
                        profession = teacher_data['profession']
                    else:
                        name = fake.name()
                        tid = generate_random_teacher_id()
                        profession = generate_random_profession()
                    
                    id_img = gen_teacher_id_auto(school_name, name, tid, profession, country_code)
                    buf_id = BytesIO()
                    id_img.save(buf_id, format='JPEG', quality=95)
                    buf_id.seek(0)
                    buf_id.name = f"{tid}_ID.jpg"
                    
                    # TAP-TO-COPY CAPTION
                    cap_id = (
                        f"✅ TEACHER ID #{i+1}/{qty}\n\n"
                        f"👤 `{name}`\n"
                        f"🏫 `{school_name}`\n"
                        f"🆔 `{tid}`\n"
                        f"👔 {profession}\n"
                        f"🌍 {cfg['flag']} {cfg['name']}\n\n"
                        f"💡 Tap to copy\n"
                        f"📅 {now().strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                    update.message.reply_photo(photo=buf_id, caption=cap_id, parse_mode='Markdown')
                    buf_id.close()
                    
                    sal_img = gen_salary_receipt_auto(school_name, name, tid, profession, country_code)
                    buf_sal = BytesIO()
                    sal_img.save(buf_sal, format='JPEG', quality=95)
                    buf_sal.seek(0)
                    buf_sal.name = f"{tid}_SALARY.jpg"
                    
                    cap_sal = (
                        f"💵 SALARY RECEIPT #{i+1}/{qty}\n\n"
                        f"👤 `{name}`\n"
                        f"🏫 `{school_name}`\n"
                        f"🆔 `{tid}`\n"
                        f"🌍 {cfg['flag']} {cfg['name']}"
                    )
                    update.message.reply_photo(photo=buf_sal, caption=cap_sal, parse_mode='Markdown')
                    buf_sal.close()
                    
                    if (i + 1) % 5 == 0:
                        try:
                            progress_msg.edit_text(f"⏳ {i+1}/{qty} generated\n📸 Photos ready\n🔳 QR codes embedded")
                        except:
                            pass
                    if i < qty - 1:
                        time.sleep(0.3)
                except Exception as e:
                    logger.error(f"Error {i+1}: {e}")
        else:
            colleges = context.user_data.get('colleges', [])
            for i in range(qty):
                try:
                    college = random.choice(colleges)
                    student_name = fake.name()
                    student_id = generate_random_student_id()
                    program = generate_random_program()
                    
                    id_img = gen_student_id_auto(college['name'], student_name, student_id, program, country_code)
                    buf_id = BytesIO()
                    id_img.save(buf_id, format='JPEG', quality=95)
                    buf_id.seek(0)
                    buf_id.name = f"{student_id}_ID.jpg"
                    
                    # TAP-TO-COPY CAPTION
                    cap_id = (
                        f"✅ STUDENT ID #{i+1}/{qty}\n\n"
                        f"👤 `{student_name}`\n"
                        f"🏫 `{college['name']}`\n"
                        f"🆔 `{student_id}`\n"
                        f"📚 {program}\n"
                        f"🌍 {cfg['flag']} {cfg['name']}\n\n"
                        f"📸 Real Photo: ✅\n"
                        f"🔳 QR Code: ✅\n"
                        f"💡 Tap to copy\n\n"
                        f"📅 {now().strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                    update.message.reply_photo(photo=buf_id, caption=cap_id, parse_mode='Markdown')
                    buf_id.close()
                    
                    if (i + 1) % 5 == 0:
                        try:
                            progress_msg.edit_text(f"⏳ {i+1}/{qty} generated\n📸 Photos downloaded\n🔳 QR codes embedded")
                        except:
                            pass
                    if i < qty - 1:
                        time.sleep(0.3)
                except Exception as e:
                    logger.error(f"Error {i+1}: {e}")
        
        try:
            progress_msg.delete()
        except:
            pass
        
        update.message.reply_text(
            f"✅ DONE!\n\n"
            f"📄 {qty} docs generated\n"
            f"🌍 {cfg['flag']} {cfg['name']}\n"
            f"📸 Real Photos: ✅\n"
            f"🔳 QR Codes: ✅\n"
            f"🧠 Country Saved!\n\n"
            f"/start"
        )
        return ConversationHandler.END
    except ValueError:
        update.message.reply_text("❌ Numbers only (1-50)\n\n/cancel")
        return INPUT_QTY

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("❌ Cancelled\n\n/start")
    return ConversationHandler.END

def error_handler(update: Update, context: CallbackContext):
    logger.warning(f'Update {update} caused error {context.error}')

def main():
    logger.info("="*80)
    logger.info("🚀 BOT STARTING - WITH MEMORY & TAP-TO-COPY")
    logger.info(f"📅 2025-10-22 08:43:57 UTC")
    logger.info(f"👤 User: Adeebaabkhan")
    logger.info("🧠 SMART MEMORY: Remembers last country")
    logger.info("📋 TAP-TO-COPY: All names copyable")
    logger.info("📸 REAL PHOTOS: thispersondoesnotexist.com")
    logger.info("🔳 QR CODES: Professional")
    logger.info(f"🌍 {COUNTRY_COUNT} COUNTRIES")
    logger.info("="*80)
    
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    conv = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MAIN_MENU: [CallbackQueryHandler(main_menu)],
            SELECT_DOC: [CallbackQueryHandler(main_menu)],
            SELECT_COUNTRY: [CallbackQueryHandler(select_country)],
            INPUT_SCHOOL: [MessageHandler(Filters.text & ~Filters.command, input_school_name), CommandHandler('cancel', cancel)],
            STUDENT_SELECT_COLLEGE: [CallbackQueryHandler(select_student_college)],
            INPUT_QTY: [MessageHandler(Filters.text & ~Filters.command, input_quantity), CommandHandler('cancel', cancel)],
            ADD_USER_INPUT: [
                CallbackQueryHandler(main_menu),
                MessageHandler(Filters.text & ~Filters.command, add_user_inline_input),
                CommandHandler('cancel', cancel)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel), CommandHandler('start', start)],
        per_message=False,
        allow_reentry=True,
    )

    dp.add_handler(conv)
    dp.add_handler(CommandHandler('adduser', add_user_command))
    dp.add_handler(CommandHandler('addsuper', add_super_admin_command))
    dp.add_error_handler(error_handler)
    
    logger.info("✅ BOT STARTED!")
    logger.info(f"🤖 Bot: @{updater.bot.get_me().username}")
    logger.info("="*80)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
