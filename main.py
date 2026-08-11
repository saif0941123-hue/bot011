# -*- coding: utf-8 -*-
import threading
import jwt
import random
from threading import Thread
import json
import requests 
import google.protobuf
from protobuf_decoder.protobuf_decoder import Parser
import json
import datetime
from datetime import datetime
from google.protobuf.json_format import MessageToJson
import my_message_pb2
import data_pb2
import base64
import logging
import socket
from google.protobuf.timestamp_pb2 import Timestamp
import jwt_generator_pb2
import os
from code_command import handle_code_command
import binascii
import sys
import psutil
from AlliFF import*
import MajorLoginRes_pb2
from time import sleep
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time
import urllib3
from important_zitado import*
from byte import*  
import asyncio
import re

# ==================== المتغيرات العامة ====================
threads = []
senthi = False
sent_inv = False
tempid = None
start_par = False
pleaseaccept = False
statusinfo = False
leaveee = False
isroom = False
isroom2 = False
g_token = None

# ==================== دوال مساعدة ====================
def add_player(uid, hours=4):
    try:
        if not uid or not uid.isdigit():
            return {"status": "error", "message": "يجب إرسال UID صحيح"}
        return {
            "status": "success",
            "message": "تم إضافة اللاعب بنجاح",
            "data": {
                "uid": uid,
                "name": uid,
                "expiry": int(time.time()) + (hours * 3600),
                "duration_hours": hours
            }
        }
    except Exception as e:
        return {"status": "error", "message": f"حدث خطأ: {str(e)}"}

def remove_player(uid):
    try:
        if not uid or not uid.isdigit():
            return {"status": "error", "message": "يجب إرسال UID صحيح"}
        return {
            "status": "success",
            "message": "تم حذف اللاعب بنجاح",
            "data": {
                "uid": uid,
                "name": uid
            }
        }
    except Exception as e:
        return {"status": "error", "message": f"حدث خطأ: {str(e)}"}

def get_user_remaining_time(uid):
    return "⏳ وقتك غير محدود"

def Get_Player_Name(uid):
    try:
        global g_token
        data = bytes.fromhex(EnC_AEs(f"08{EnC_Uid(uid, Tp='Uid')}1007"))
        url = "https://clientbp.ggpolarbear.com/GetPlayerPersonalShow"
        headers = {
            'X-Unity-Version': '2018.4.11f1',
            'ReleaseVersion': 'OB54',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-GA': 'v1 1',
            'Authorization': f'Bearer {g_token}',
            'Content-Length': '16',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
            'Host': 'clientbp.ggpolarbear',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'}
        
        response = requests.post(url, headers=headers, data=data, verify=False)
        
        if response.status_code in [200, 201]:
            packet = binascii.hexlify(response.content).decode('utf-8')
            DaTa_Pb2 = json.loads(DeCode_PackEt(packet))
            return DaTa_Pb2.get("1", {}).get("data", {}).get("3", {}).get("data", uid)
        return uid
    except:
        return uid

def encrypt_packet(plain_text, key, iv):
    plain_text = bytes.fromhex(plain_text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()
    
def gethashteam(hexxx):
    a = zitado_get_proto(hexxx)
    if not a:
        raise ValueError("Invalid hex format or empty response from zitado_get_proto")
    data = json.loads(a)
    return data['5']['7']

def getownteam(hexxx):
    a = zitado_get_proto(hexxx)
    if not a:
        raise ValueError("Invalid hex format or empty response from zitado_get_proto")
    data = json.loads(a)
    return data['5']['1']

def get_player_status(packet):
    json_result = get_available_room(packet)
    parsed_data = json.loads(json_result)

    if "5" not in parsed_data or "data" not in parsed_data["5"]:
        return "OFFLINE"

    json_data = parsed_data["5"]["data"]

    if "1" not in json_data or "data" not in json_data["1"]:
        return "OFFLINE"

    data = json_data["1"]["data"]

    if "3" not in data:
        return "OFFLINE"

    status_data = data["3"]

    if "data" not in status_data:
        return "OFFLINE"

    status = status_data["data"]

    if status == 1:
        return "SOLO"
    
    if status == 2:
        if "9" in data and "data" in data["9"]:
            group_count = data["9"]["data"]
            countmax1 = data["10"]["data"]
            countmax = countmax1 + 1
            return f"INSQUAD ({group_count}/{countmax})"

        return "INSQUAD"
    
    if status in [3, 5]:
        return "INGAME"
    if status == 4:
        return "IN ROOM"
    
    if status in [6, 7]:
        return "IN SOCIAL ISLAND MODE .."

    return "NOTFOUND"

def get_idroom_by_idplayer(packet):
    json_result = get_available_room(packet)
    parsed_data = json.loads(json_result)
    json_data = parsed_data["5"]["data"]
    data = json_data["1"]["data"]
    idroom = data['15']["data"]
    return idroom

def get_leader(packet):
    json_result = get_available_room(packet)
    parsed_data = json.loads(json_result)
    json_data = parsed_data["5"]["data"]
    data = json_data["1"]["data"]
    leader = data['8']["data"]
    return leader

def generate_random_color():
    color_list = [
        "[00FF00]", "[FFDD00]", "[3813F3]", "[FF0000]",
        "[0000FF]", "[FFA500]", "[DF07F8]", "[11EAFD]",
        "[DCE775]", "[A8E6CF]", "[7CB342]", "[FFB300]",
        "[90EE90]", "[32CD32]", "[00BFFF]", "[00FA9A]",
        "[FF4500]", "[FF6347]", "[FF69B4]", "[FF8C00]",
        "[FFD700]", "[FFDAB9]", "[F0F0F0]", "[F0E68C]",
        "[D3D3D3]", "[A9A9A9]", "[D2691E]", "[CD853F]",
        "[BC8F8F]", "[6A5ACD]", "[483D8B]", "[4682B4]",
        "[9370DB]", "[C71585]", "[FFA07A]", "[87CEEB]",
        "[8A2BE2]", "[DC143C]", "[00CED1]", "[9400D3]"
    ]
    return random.choice(color_list)

def fix_num(num):
    fixed = ""
    count = 0
    num_str = str(num)

    for char in num_str:
        if char.isdigit():
            count += 1
        fixed += char
        if count == 3:
            fixed += "[c]"
            count = 0  
    return fixed

def rrrrrrrrrrrrrr(number):
    if isinstance(number, str) and '***' in number:
        return number.replace('***', '106')
    return number
                
def Encrypt(number):
    number = int(number)
    encoded_bytes = []

    while True:
        byte = number & 0x7F
        number >>= 7  
        if number:
            byte |= 0x80

        encoded_bytes.append(byte)
        if not number:
            break

    return bytes(encoded_bytes).hex()

def get_random_avatar():
    avatar_list = [
        '902000061', '902000060', '902000064', '902000065', '902000066', 
        '902000074', '902000075', '902000077', '902000078', '902000084', 
        '902000085', '902000087', '902000091', '902000094', '902000306', 
        '902000208', '902000209', '902000210', '902000211', '902047016', 
        '902000347', '902000305', '902000003', '902000016', '902000017', 
        '902000019', '902000020', '902000021', '902000023', '902000070', 
        '902000108', '902000011', '902049020', '902049018', '902049017', 
        '902049016', '902049015', '902049003', '902033016', '902033017', 
        '902033018', '902048018'
    ]
    random_avatar = random.choice(avatar_list)
    return random_avatar

def get_player_info(uid):
    try:
        response = requests.get(f"https://api-info-alliff-d5m.vercel.app/info={uid}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            basic_info = data.get("basicInfo", {})
            social_info = data.get("socialInfo", {})
            
            a3 = basic_info.get("nickname", uid)
            a1 = uid
            a2 = basic_info.get("liked", 0)
            llll = basic_info.get("level", 0)
            ssss = basic_info.get("region", "Unknown")
            
            bbbb = social_info.get("signature", "لا يوجد بايو")
            
            created_time = basic_info.get("createAt", 0)
            if created_time and int(created_time) > 0:
                try:
                    account_date = datetime.fromtimestamp(int(created_time)).strftime("%I:%M %p - %d/%m/%y")
                except:
                    account_date = "غير معروف"
            else:
                account_date = "غير معروف"
            
            last_login_time = basic_info.get("lastLoginAt", 0)
            if last_login_time and int(last_login_time) > 0:
                try:
                    last_login = datetime.fromtimestamp(int(last_login_time)).strftime("%I:%M %p - %d/%m/%y")
                except:
                    last_login = "غير معروف"
            else:
                last_login = "غير معروف"
            
            result = f"""{generate_random_color()}[c][b]الاسم !
{generate_random_color()}{a3}
{generate_random_color()}الايدي !
{generate_random_color()}{fix_num(a1)}
{generate_random_color()}الإعجابات !
{generate_random_color()}{fix_num(a2)}
{generate_random_color()}المستوى !
{generate_random_color()}{fix_num(llll)}
{generate_random_color()}البايو !
{generate_random_color()}{bbbb}
{generate_random_color()}السيرفر !
{generate_random_color()}{ssss}
{generate_random_color()}تاريخ الإنشاء !
{generate_random_color()}{account_date}
{generate_random_color()}آخر تسجيل دخول !
{generate_random_color()}{last_login}"""
            
            return result
        else:
            return f"{generate_random_color()}❌ لم يتم العثور على اللاعب {uid}"
            
    except requests.exceptions.ConnectionError:
        return f"{generate_random_color()}❌ API غير متصل!"
    except requests.exceptions.Timeout:
        return f"{generate_random_color()}❌ انتهى وقت الاتصال بالـ API"
    except Exception as e:
        print(f"Error in get_player_info: {e}")
        return f"{generate_random_color()}❌ حدث خطأ في جلب معلومات اللاعب: {str(e)}"

def get_player_bio(uid):
    try:
        response = requests.get(f"https://api-info-alliff-d5m.vercel.app/info={uid}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            social_info = data.get("socialInfo", {})
            bbbb = social_info.get("signature", "لا يوجد بايو")
            
            return f"{generate_random_color()}📝 بايو اللاعب {fix_num(uid)}:\n{generate_random_color()}{bbbb}"
        else:
            return f"{generate_random_color()}❌ لم يتم العثور على اللاعب {uid}"
            
    except requests.exceptions.ConnectionError:
        return f"{generate_random_color()}❌ API غير متصل!"
    except requests.exceptions.Timeout:
        return f"{generate_random_color()}❌ انتهى وقت الاتصال بالـ API"
    except Exception as e:
        print(f"Error in get_player_bio: {e}")
        return f"{generate_random_color()}❌ حدث خطأ في جلب بايو اللاعب: {str(e)}"
        
def get_player_likes(uid):
    try:
        likes_api_response = requests.get(f"http://51.83.6.5:20099/proxy/8102/like?uid={uid}", timeout=30)

        if likes_api_response.status_code == 200:
            api_data = likes_api_response.json()

            if api_data.get("status") == 1:
                return {
                    "status": "ok",
                    "message": (
                        f"[C][B][00FF00]________\n"
                        f" ✅ تم إضافة {api_data.get('LikesGivenByAPI', 0)} إعجاب\n"
                        f" الاسم: {api_data.get('PlayerNickname', uid)}\n"
                        f" الإعجابات السابقة: {api_data.get('LikesBefore', 0)}\n"
                        f" الإعجابات الجديدة: {api_data.get('LikesAfter', 0)}\n"
                        f"________"
                    )
                }
            elif api_data.get("status") == 2:
                return {
                    "status": "failed",
                    "message": (
                        f"[C][B][FF0000]________\n"
                        f" ❌ الحد اليومي لإرسال الإعجابات!\n"
                        f" حاول مرة أخرى بعد 24 ساعة\n"
                        f"________"
                    )
                }
            else:
                return {
                    "status": "failed",
                    "message": (
                        f"[C][B][FF0000]________\n"
                        f" ❌ خطأ غير معروف!\n"
                        f"________"
                    )
                }

        else:
            return {
                "status": "failed",
                "message": (
                    f"[C][B][FF0000]________\n"
                    f" ❌ خطأ في الإرسال!\n"
                    f" تأكد من صحة ال ID\n"
                    f"________"
                )
            }

    except Exception as e:
        return {
            "status": "failed",
            "message": (
                f"[C][B][FF0000]________\n"
                f" ⚠️ حدث خطأ أثناء محاولة الإرسال!\n"
                f" التفاصيل: {str(e)}\n"
                f"________"
            )
        }
        
def send_visits(uid):
    try:
        response = requests.get(f"http://alliff5-api-visit.hf.space/visit?uid={uid}", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("status") == "success":
                return f"{generate_random_color()}✅ تم ارسال 300 زيارة للاعب بنجاح !"
            else:
                return f"{generate_random_color()}❌ فشل إرسال الزيارات للاعب"
        else:
            return f"{generate_random_color()}❌ API غير متصل!"
            
    except requests.exceptions.ConnectionError:
        return f"{generate_random_color()}❌ API غير متصل!"
    except requests.exceptions.Timeout:
        return f"{generate_random_color()}❌ انتهى وقت الاتصال بالـ API"
    except Exception as e:
        print(f"Error in send_visits: {e}")
        return f"{generate_random_color()}❌ حدث خطأ في إرسال الزيارات: {str(e)}"

def get_available_room(input_text):
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_objects = parsed_results
        parsed_results_dict = parse_results(parsed_results_objects)
        json_data = json.dumps(parsed_results_dict)
        return json_data
    except Exception as e:
        print(f"error {e}")
        return None

def parse_results(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data["wire_type"] = result.wire_type
        if result.wire_type == "varint":
            field_data["data"] = result.data
        if result.wire_type == "string":
            field_data["data"] = result.data
        if result.wire_type == "bytes":
            field_data["data"] = result.data
        elif result.wire_type == "length_delimited":
            field_data["data"] = parse_results(result.data.results)
        result_dict[result.field] = field_data
    return result_dict

def dec_to_hex(ask):
    ask_result = hex(ask)
    final_result = str(ask_result)[2:]
    if len(final_result) == 1:
        final_result = "0" + final_result
    return final_result

def encrypt_message(plaintext):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(plaintext, AES.block_size)
    encrypted_message = cipher.encrypt(padded_message)
    return binascii.hexlify(encrypted_message).decode('utf-8')

def encrypt_api(plain_text):
    plain_text = bytes.fromhex(plain_text)
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()

def extract_jwt_from_hex(hex):
    byte_data = binascii.unhexlify(hex)
    message = jwt_generator_pb2.Garena_420()
    message.ParseFromString(byte_data)
    json_output = MessageToJson(message)
    token_data = json.loads(json_output)
    return token_data

def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def check_banned_status(player_id):
    try:
        ban_url = f"https://ff.garena.com/api/antihack/check_banned?lang=en&uid={player_id}"
        ban_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
            "referer": "https://ff.garena.com/en/support/",
            "x-requested-with": "B6FksShzIgjfrYImLpTsadjS86sddhFH"
        }
        
        ban_response = requests.get(ban_url, headers=ban_headers, timeout=10)
        
        if ban_response.status_code == 200:
            data = ban_response.json().get("data", {})
            is_banned = data.get("is_banned", 0)
            period = data.get("period", 0)
            
            ban_status = "❌ مبند" if is_banned == 1 else "✅ غير مبند"
            
            return {
                "success": True,
                "is_banned": ban_status,
                "ban_period": period,
                "player_id": player_id
            }
        else:
            return {
                "success": False,
                "message": f"❌ فشل فحص الباند. HTTP {ban_response.status_code}"
            }
            
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "message": "❌ انتهى وقت الاتصال"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ خطأ: {str(e)}"
        }

def EnC_AEs(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(data, AES.block_size))
    return cipher_text.hex()

def EnC_Uid(uid, Tp='Uid'):
    if Tp == 'Uid':
        number = int(uid)
        result = []
        while number > 0:
            byte = number & 0x7F
            number >>= 7
            if number > 0:
                byte |= 0x80
            result.append(byte)
        return ''.join(f'{b:02x}' for b in result)
    return uid

def DeCode_PackEt(data):
    try:
        parsed_results = Parser().parse(data)
        return json.dumps(parse_results(parsed_results))
    except:
        return "{}"

def decode_data(data):
    try:
        return data.decode('utf-8', errors='ignore')
    except:
        return str(data)

# ==================== Class FF_CLIENT ====================
class FF_CLIENT(threading.Thread):
    def __init__(self, id, password):
        super().__init__()
        self.id = id
        self.password = password
        self.key = None
        self.iv = None
        self.AutH_ToKen = None
        self.whisper_ip = None
        self.whisper_port = None
        self.online_ip = None
        self.online_port = None
        self.admin_chat_state = {}
        self.running = True
        self.get_tok()

    def parse_my_message(self, serialized_data):
        MajorLogRes = MajorLoginRes_pb2.MajorLoginRes()
        MajorLogRes.ParseFromString(serialized_data)
        
        timestamp = MajorLogRes.kts
        key = MajorLogRes.ak
        iv = MajorLogRes.aiv
        BASE64_TOKEN = MajorLogRes.token
        timestamp_obj = Timestamp()
        timestamp_obj.FromNanoseconds(timestamp)
        timestamp_seconds = timestamp_obj.seconds
        timestamp_nanos = timestamp_obj.nanos
        combined_timestamp = timestamp_seconds * 1_000_000_000 + timestamp_nanos
        return combined_timestamp, key, iv, BASE64_TOKEN

    def GET_PAYLOAD_BY_DATA(self,JWT_TOKEN , NEW_ACCESS_TOKEN,date):
        token_payload_base64 = JWT_TOKEN.split('.')[1]
        token_payload_base64 += '=' * ((4 - len(token_payload_base64) % 4) % 4)
        decoded_payload = base64.urlsafe_b64decode(token_payload_base64).decode('utf-8')
        decoded_payload = json.loads(decoded_payload)
        NEW_EXTERNAL_ID = decoded_payload['external_id']
        SIGNATURE_MD5 = decoded_payload['signature_md5']
        now = datetime.now()
        now =str(now)[:len(str(now))-7]
        formatted_time = date
        payload = bytes.fromhex("1a13323032362d30362d32392031333a34323a3531220966726565206669726528013a07322e3132362e36423a416e64726f6964204f532039202f204150492d32382028505133422e3139303830312e30333235303930332f47393635305a48553241524336294a0848616e6468656c6452074d6f62696e696c5a045749464960c00c68840772033234307a287838362d3634205353453320535345342e3120535345342e3220415658207c2032383635207c20368001c32e8a010f416472656e6f2028544d29203634309201104f70656e474c20455320332e312076319a012b476f6f676c657c38656162393736322d633065612d343064382d623634662d663135326263313265303362a2010d3139372e3230322e35352e3330aa01026172b201206465633265383233613766303737306338383765663163613464303131633063ba010134c2010848616e6468656c64ca01115869616f6d69203233303446504e364447d201024d45ea014066383830663031383933666337383264663063393538366562656232326134633663393464613632636334353365303166333465363538613830393561663730f00101ca02074d6f62696e696cd2020457494649ca03203161633462383065636630343738613434323033626638666163363132306635e003c88a03e803c1f002f003d713f803de058004d0ba01880484d0019004ff81039804c88a03c80403d204402f646174612f6170702f636f6d2e6474732e66726565666972656d61782d716a7a583456364a6d654d744d656865766f6c6856513d3d2f6c69622f61726d3634e00402ea046064353038353336623261336331366266326265626264323432333365393239337c2f646174612f6170702f636f6d2e6474732e66726565666972656d61782d716a7a583456364a6d654d744d656865766f6c6856513d3d2f626173652e61706bf00402f804028a050236349a050a32303139313138303435a80503b205094f70656e474c455333b805ff1fc00504e005a73dea050b616e64726f69645f6d6178f2055c4b717348542b64772f4f504d523676524b7352545a55486a727272635779346333477974374b3649794157586665307238513943696261414231364b3538674244514d57314b6939626372382b78696f4b3278776453396a7330413df805e7e4068206257b226375725f72617465223a6e756c6c2c22737570706f72745f65746332223a747275657d8806019006019a060134a2060134b20600")
        payload = payload.replace(b"2025-07-30 11:02:51", str(now).encode())
        payload = payload.replace(b"f880f01893fc782df0c9586ebeb22a4c6c94da62cc453e01f34e658a8095af70", NEW_ACCESS_TOKEN.encode("UTF-8"))
        payload = payload.replace(b"dec2e823a7f0770c887ef1ca4d011c0c", NEW_EXTERNAL_ID.encode("UTF-8"))
        payload = payload.replace(b"7428b253defc164018c604a1ebbfebdf", SIGNATURE_MD5.encode("UTF-8"))
        PAYLOAD = payload.hex()
        PAYLOAD = encrypt_api(PAYLOAD)
        PAYLOAD = bytes.fromhex(PAYLOAD)
        whisper_ip, whisper_port, online_ip, online_port = self.GET_LOGIN_DATA(JWT_TOKEN , PAYLOAD)
        return whisper_ip, whisper_port, online_ip, online_port
    
    def dec_to_hex(ask):
        ask_result = hex(ask)
        final_result = str(ask_result)[2:]
        if len(final_result) == 1:
            final_result = "0" + final_result
            return final_result
        else:
            return final_result
    
    def convert_to_hex(PAYLOAD):
        hex_payload = ''.join([f'{byte:02x}' for byte in PAYLOAD])
        return hex_payload
    
    def convert_to_bytes(PAYLOAD):
        payload = bytes.fromhex(PAYLOAD)
        return payload
    
    def GET_LOGIN_DATA(self, JWT_TOKEN, PAYLOAD):
        url = "https://clientbp.ggpolarbear.com/GetLoginData"
        headers = {
            'Expect': '100-continue',
            'Authorization': f'Bearer {JWT_TOKEN}',
            'X-Unity-Version': '2018.4.11f1',
            'X-GA': 'v1 1',
            'ReleaseVersion': 'OB54',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)',
            'Host': 'clientbp.ggpolarbear',
            'Connection': 'close',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        
        max_retries = 3
        attempt = 0

        while attempt < max_retries:
            try:
                response = requests.post(url, headers=headers, data=PAYLOAD,verify=False)
                response.raise_for_status()
                x = response.content.hex()
                json_result = get_available_room(x)
                parsed_data = json.loads(json_result)
                print(parsed_data)
                
                whisper_address = parsed_data['32']['data']
                online_address = parsed_data['14']['data']
                online_ip = online_address[:len(online_address) - 6]
                whisper_ip = whisper_address[:len(whisper_address) - 6]
                online_port = int(online_address[len(online_address) - 5:])
                whisper_port = int(whisper_address[len(whisper_address) - 5:])
                return whisper_ip, whisper_port, online_ip, online_port
            
            except requests.RequestException as e:
                print(f"Request failed: {e}. Attempt {attempt + 1} of {max_retries}. Retrying...")
                attempt += 1
                time.sleep(2)

        print("Failed to get login data after multiple attempts.")
        return None, None, None, None

    def guest_token(self, uid, password):
        url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        headers = {
            "Host": "100067.connect.garena.com",
            "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 10;en;EN;)",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "close",
        }
        data = {
            "uid": f"{uid}",
            "password": f"{password}",
            "response_type": "token",
            "client_type": "2",
            "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
            "client_id": "100067",
        }
        try:
            response = requests.post(url, headers=headers, data=data, timeout=10)
            response_data = response.json()
            
            if 'access_token' not in response_data:
                print(f"❌ فشل تسجيل الدخول للحساب {uid}")
                print(f"الرد: {response_data}")
                return None
            
            NEW_ACCESS_TOKEN = response_data['access_token']
            NEW_OPEN_ID = response_data['open_id']
            OLD_ACCESS_TOKEN = "f880f01893fc782df0c9586ebeb22a4c6c94da62cc453e01f34e658a8095af70"
            OLD_OPEN_ID = "dec2e823a7f0770c887ef1ca4d011c0c"
            time.sleep(0.2)
            result = self.TOKEN_MAKER(OLD_ACCESS_TOKEN, NEW_ACCESS_TOKEN, OLD_OPEN_ID, NEW_OPEN_ID, uid)
            return result
        except Exception as e:
            print(f"❌ خطأ في تسجيل الدخول للحساب {uid}: {e}")
            return None
        
    def TOKEN_MAKER(self,OLD_ACCESS_TOKEN , NEW_ACCESS_TOKEN , OLD_OPEN_ID , NEW_OPEN_ID,id):
        headers = {
            'X-Unity-Version': '2018.4.11f1',
            'ReleaseVersion': 'OB54',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-GA': 'v1 1',
            'Content-Length': '928',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
            'Host': 'loginbp.ggpolarbear.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }
        data = bytes.fromhex('1a13323032362d30362d32392031333a34323a3531220966726565206669726528013a07322e3132362e36423a416e64726f6964204f532039202f204150492d32382028505133422e3139303830312e30333235303930332f47393635305a48553241524336294a0848616e6468656c6452074d6f62696e696c5a045749464960c00c68840772033234307a287838362d3634205353453320535345342e3120535345342e3220415658207c2032383635207c20368001c32e8a010f416472656e6f2028544d29203634309201104f70656e474c20455320332e312076319a012b476f6f676c657c38656162393736322d633065612d343064382d623634662d663135326263313265303362a2010d3139372e3230322e35352e3330aa01026172b201206465633265383233613766303737306338383765663163613464303131633063ba010134c2010848616e6468656c64ca01115869616f6d69203233303446504e364447d201024d45ea014066383830663031383933666337383264663063393538366562656232326134633663393464613632636334353365303166333465363538613830393561663730f00101ca02074d6f62696e696cd2020457494649ca03203161633462383065636630343738613434323033626638666163363132306635e003c88a03e803c1f002f003d713f803de058004d0ba01880484d0019004ff81039804c88a03c80403d204402f646174612f6170702f636f6d2e6474732e66726565666972656d61782d716a7a583456364a6d654d744d656865766f6c6856513d3d2f6c69622f61726d3634e00402ea046064353038353336623261336331366266326265626264323432333365393239337c2f646174612f6170702f636f6d2e6474732e66726565666972656d61782d716a7a583456364a6d654d744d656865766f6c6856513d3d2f626173652e61706bf00402f804028a050236349a050a32303139313138303435a80503b205094f70656e474c455333b805ff1fc00504e005a73dea050b616e64726f69645f6d6178f2055c4b717348542b64772f4f504d523676524b7352545a55486a727272635779346333477974374b3649794157586665307238513943696261414231364b3538674244514d57314b6939626372382b78696f4b3278776453396a7330413df805e7e4068206257b226375725f72617465223a6e756c6c2c22737570706f72745f65746332223a747275657d8806019006019a060134a2060134b20600')
        data = data.replace(OLD_OPEN_ID.encode(),NEW_OPEN_ID.encode())
        data = data.replace(OLD_ACCESS_TOKEN.encode() , NEW_ACCESS_TOKEN.encode())
        hex = data.hex()
        d = encrypt_api(data.hex())
        Final_Payload = bytes.fromhex(d)
        URL = "https://loginbp.ggpolarbear.com/MajorLogin"

        RESPONSE = requests.post(URL, headers=headers, data=Final_Payload,verify=False)
        
        combined_timestamp, key, iv, BASE64_TOKEN = self.parse_my_message(RESPONSE.content)
        if RESPONSE.status_code == 200:
            if len(RESPONSE.text) < 10:
                return False
            whisper_ip, whisper_port, online_ip, online_port = self.GET_PAYLOAD_BY_DATA(BASE64_TOKEN,NEW_ACCESS_TOKEN,1)
            self.key = key
            self.iv = iv
            self.whisper_ip = whisper_ip
            self.whisper_port = whisper_port
            self.online_ip = online_ip
            self.online_port = online_port
            print(key, iv)
            return(BASE64_TOKEN, key, iv, combined_timestamp, whisper_ip, whisper_port, online_ip, online_port)
        else:
            return False
    
    def time_to_seconds(hours, minutes, seconds):
        return (hours * 3600) + (minutes * 60) + seconds

    def seconds_to_hex(seconds):
        return format(seconds, '04x')
    
    def extract_time_from_timestamp(timestamp):
        dt = datetime.fromtimestamp(timestamp)
        h = dt.hour
        m = dt.minute
        s = dt.second
        return h, m, s
    
    def get_tok(self):
        global g_token
        max_retries = 10
        for attempt in range(max_retries):
            try:
                result = self.guest_token(self.id, self.password)
                if result:
                    token, key, iv, Timestamp, whisper_ip, whisper_port, online_ip, online_port = result
                    g_token = token
                    self.whisper_ip = whisper_ip
                    self.whisper_port = whisper_port
                    self.online_ip = online_ip
                    self.online_port = online_port
                    self.key = key
                    self.iv = iv
                    print(whisper_ip, whisper_port)
                    try:
                        decoded = jwt.decode(token, options={"verify_signature": False})
                        account_id = decoded.get('account_id')
                        encoded_acc = hex(account_id)[2:]
                        hex_value = dec_to_hex(Timestamp)
                        time_hex = hex_value
                        BASE64_TOKEN_ = token.encode().hex()
                        print(f"Token decoded and processed. Account ID: {account_id}")
                    except Exception as e:
                        print(f"Error processing token: {e}")
                        continue

                    try:
                        head = hex(len(encrypt_packet(BASE64_TOKEN_, key, iv)) // 2)[2:]
                        length = len(encoded_acc)
                        zeros = '00000000'

                        if length == 9:
                            zeros = '0000000'
                        elif length == 8:
                            zeros = '00000000'
                        elif length == 10:
                            zeros = '000000'
                        elif length == 7:
                            zeros = '000000000'
                        else:
                            print('Unexpected length encountered')
                        head = f'0115{zeros}{encoded_acc}{time_hex}00000{head}'
                        final_token = head + encrypt_packet(BASE64_TOKEN_, key, iv)
                        self.AutH_ToKen = final_token
                        print("Final token constructed successfully.")
                    except Exception as e:
                        print(f"Error constructing final token: {e}")
                        continue
                    token = final_token
                    self.connect(token, 'anything', key, iv, whisper_ip, whisper_port, online_ip, online_port)
                    return token, key, iv
                else:
                    print(f"❌ Attempt {attempt+1}/{max_retries} failed for account {self.id}, retrying in 5 seconds...")
                    time.sleep(5)
            except Exception as e:
                print(f"❌ Error in get_tok: {e}, retrying in 5 seconds...")
                time.sleep(5)
        print(f"❌ All attempts failed for account {self.id}, stopping...")
        return None, None, None

    def nmnmmmmn(self, data):
        key, iv = self.key, self.iv
        try:
            key = key if isinstance(key, bytes) else bytes.fromhex(key)
            iv = iv if isinstance(iv, bytes) else bytes.fromhex(iv)
            data = bytes.fromhex(data)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            cipher_text = cipher.encrypt(pad(data, AES.block_size))
            return cipher_text.hex()
        except Exception as e:
            print(f"Error in nmnmmmmn: {e}")

    def send_emote(self, target_id, emote_id, owner_id):
        fields = {
            1: 21,
            2: {
                1: int(owner_id),
                2: 909000002,
                5: {
                    1: int(target_id),
                    3: int(emote_id),
                }
            }
        }
        packet = create_protobuf_packet(fields).hex()
        header_lenth = len(encrypt_packet(packet, self.key, self.iv)) // 2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        else:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)    
        
    def spam_room(self, idroom, idplayer):
        fields = {
        1: 78,
        2: {
            1: int(idroom),
            2: "[C][B]AlliFF[FF0000]BOT",
            4: 330,
            5: 6000,
            6: 201,
            10: int(get_random_avatar()),
            11: int(idplayer),
            12: 1
        }
        }
        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, self.key, self.iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0E15000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "0E1500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "0E150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0E15000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)

    def send_squad(self, idplayer):
        fields = {
            1: 33,
            2: {
                1: int(idplayer),
                2: "ME",
                3: 1,
                4: 1,
                7: 330,
                8: 19459,
                9: 100,
                12: 1,
                16: 1,
                17: {
                2: 94,
                6: 11,
                8: "1.109.5",
                9: 3,
                10: 2
                },
                18: 201,
                23: {
                2: 1,
                3: 1
                },
                24: int(get_random_avatar()),
                26: {},
                28: {}
            }
        }
        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, self.key, self.iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
        
    def request_join_squad(self, idplayer):
        import random
        same_value = random.choice([4096, 16384, 8192])
        fields = {
        1: 33,
        2: {
            1: int(idplayer),
            2: "ME",
            3: 1,
            4: 1,
            5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
            6: "AlliFF:[C][B][FF0000] @knatri77",
            7: 330,
            8: 1000,
            10: "ME",
            11: bytes([49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56,
            97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49, 50, 48, 102, 53]),
            12: 1,
            13: int(idplayer),
            14: {
            1: 2203434355,
            2: 8,
            3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            },
            16: 1,
            17: 1,
            18: 312,
            19: 46,
            23: bytes([16, 1, 24, 1]),
            24: int(get_random_avatar()),
            26: "",
            28: "",
            31: {
            1: 1,
            2: same_value
            },
            32: same_value,
            34: {
            1: int(idplayer),
            2: 8,
            3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
            }
        },
        10: "en",
        13: {
            2: 1,
            3: 1
        }
        }
        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, self.key, self.iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)

    def start_autooo(self):
        fields = {
        1: 9,
        2: {
            1: 11371687918
        }
        }
        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, self.key, self.iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)

    def invite_skwad(self, idplayer):
        fields = {
        1: 2,
        2: {
            1: int(idplayer),
            2: "ME",
            4: 1
        }
        }
        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, self.key, self.iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
        
    def request_skwad(self, idplayer):
        fields = {
        1: 33,
        2: {
            1: int(idplayer),
            2: "ME",
            3: 1,
            4: 1,
            7: 330,
            8: 19459,
            9: 100,
            12: 1,
            16: 1,
            17: {
            2: 94,
            6: 11,
            8: "1.109.5",
            9: 3,
            10: 2
            },
            18: 201,
            23: {
            2: 1,
            3: 1
            },
            24: int(get_random_avatar()),
            26: {},
            28: {}
        }
        }
        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, self.key, self.iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)

    def skwad_maker(self):
        fields = {
        1: 1,
        2: {
            2: '\u0001',
            3: 1,
            4: 3,
            5: 'ar',
            8: {
                1: 'IDC4',
                2: 145,
                3: 'ME'
            },
            9: 1,
            10: '01030407090a0b12191a201d2729',
            11: 1,
            13: 1,
            14: {
                1: {
                    6: 56
                },
                2: 731,
                3: '745d59541601024c01015f02020d0905030304570608570d57060d53540402025f5707545301060613050645775945454c18021c051e1a0306491a4760785c53477d735a53486073421b5d5841075642426f5c63610914084e1f005e721f6001467e0c51634263771f5f554642434556660104040f13050445636e74634379505365047256665e405459657766510f615a5250420d11084858416a0d7a470c720065655c5f5a0370584559584a457f43675f460c16024e477a4258430c6050417a45545c47786456597a7a7163545907714109160849667377607d0b4a07657c5c45045f5d784f5b5665096464065875620411050d4d7f7444766661406a6205545d5b5f74507e0b0b535c67580877607d0a1a0148761e795678487f7871465874697177534971666d5a7574677075550d17034503781a675e60787f4d406d7a625d57797d441b47057b026d1a685a0d1102044b0d60040d706067756547767d66777b7f46007346667e43065e5c780813074c5606764057727546596364037054674d590161467f73416209077108',
                4: 'w]ZP',
                6: 11,
                7: '140b7d71715b751011',
                8: '1.126.8',
                9: 3,
                10: 2,
                11: '0362625351363559382b505637416456324b796f566c6364724541566d46795954394b384445494d7a4b646d4b4231562f2b5a727577754a307847426c36712b38683863796b56447967524f4e3676493259347a646974684371364b73464d33724e534a4c4274594f3256565a5465786235484c324c39544a7652514c55374a525663696154544d46776e594e4b4c35353150336c5831475150635668615a77396251674b4d30395a4b6a2f4d675a38656d66757a6e4b356f5a6734367841626a7761363273366235636469637867386a6d4e4944594c383638686e756c3044316a4e445636444a4a69614758456154782b5450696c6f69476f58333638497234563266697a63783934436f5562735039765855683438356a626233356a717a5577504365554c55776374534574456d68426c3957453943524873422b76504a39704863323479517a70446c74644779536f6a6a4f573166433343413733374e617255546d734a70355431686b35635853307134557a6f7a6b75684b6d42423067354f4563634b627a68506c585943712f666a59767531624174504d766437486f4e6e39696e53767679796c6156386e315837636b7978384575626b5868414734565069425961556a75667a2b75675a474164356872324c3156615434613143485745702f6b446142364849434b756f705770706c703151373265463252744f62544957487775305a6753474659514266396f6e48744e7a5035336e72457072366f6c5349455354393839414f494858313471384d4a5763546d514267486d6c3456454c617354426d6f2b36764149525752783664617256692f345147566f4c785944593359477a366e513d3d'
            },
            19: 329,
            21: '374f5219',
            24: {
                1: 21
            }
        }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, self.key, self.iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)

    def changes(self, num):
        fields = {
        1: 17,
        2: {
            1: 11371687918,
            2: 1,
            3: int(num),
            4: 62,
            5: "\u001a",
            8: 5,
            13: 329
        }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, self.key, self.iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)

    def leave_s(self):
        fields = {
        1: 7,
        2: {
            1: 11371687918
        }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, self.key, self.iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)

    def leave_room(self, idroom):
        fields = {
        1: 6,
        2: {
            1: int(idroom)
        }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, self.key, self.iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0E15000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "0E1500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "0E150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0E15000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)

    def stauts_infoo(self, idd):
        fields = {
        1: 7,
        2: {
            1: 11371687918
        }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, self.key, self.iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)

    def GenResponsMsg(self, Msg, Enc_Id):
        fields = {
            1: 1,
            2: {
                1: 12947146032,
                2: Enc_Id,
                3: 2,
                4: str(Msg),
                5: int(datetime.now().timestamp()),
                7: 2,
                9: {
                    1: "BANECIPHER",
                    2: int(get_random_avatar()),
                    3: 901049014,
                    4: 330,
                    5: 710037095,
                    8: "Friend",
                    10: 1,
                    11: 1,
                    13: {
                        1: 2,
                        2: 1,
                    },
                    14: {
                        1: 11017917409,
                        2: 8,
                        3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
                    }
                },
                10: "IND",
                13: {
                    1: "https://graph.facebook.com/v9.0/253082355523299/picture?width=160&height=160",
                    2: 1,
                    3: 1
                },
                14: {
                    1: {
                        1: random.choice([1, 4]),
                        2: 1,
                        3: random.randint(1, 180),
                        4: 1,
                        5: int(datetime.now().timestamp()),
                        6: "IND"
                    }
                }
            }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, self.key, self.iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "1215000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "121500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "12150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "1215000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)

    def createpacketinfo(self, idddd):
        ida = Encrypt(idddd)
        packet = f"080112090A05{ida}1005"
        header_lenth = len(encrypt_packet(packet, self.key, self.iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0F15000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "0F1500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "0F150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0F15000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)

    def accept_sq(self, hashteam, idplayer, ownerr):
        fields = {
        1: 4,
        2: {
            1: int(ownerr),
            3: int(idplayer),
            4: "\u0001\u0007\t\n\u0012\u0019\u001a ",
            8: 1,
            9: {
            2: 1393,
            4: "AlliFF_BOT",
            6: 11,
            8: "1.109.5",
            9: 3,
            10: 2
            },
            10: hashteam,
            12: 1,
            13: "en",
            16: "OR"
        }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, self.key, self.iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)

    def info_room(self, idrooom):
        fields = {
        1: 1,
        2: {
            1: int(idrooom),
            3: {},
            4: 1,
            6: "en"
        }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, self.key, self.iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0E15000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "0E1500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "0E150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0E15000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)

    def reconnect(self, tok, online_ip, online_port, packet, key, iv):
        """محاولة إعادة الاتصال عند الانقطاع"""
        global socket_client
        try:
            socket_client.close()
        except:
            pass
        try:
            socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_client.connect((online_ip, int(online_port)))
            socket_client.send(bytes.fromhex(tok))
            print(f"✅ Reconnected successfully to {online_ip}:{online_port}")
            return True
        except Exception as e:
            print(f"❌ Reconnection failed: {e}")
            return False

    def sockf1(self, tok, online_ip, online_port, packet, key, iv):
        global socket_client
        global sent_inv
        global tempid
        global start_par
        global clients
        global pleaseaccept
        global tempdata1
        global nameinv
        global idinv
        global senthi
        global statusinfo
        global tempdata
        global data22
        global leaveee
        global isroom
        global isroom2
        
        max_reconnect_attempts = 10
        reconnect_attempt = 0
        
        while True:
            try:
                if reconnect_attempt == 0:
                    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    online_port = int(online_port)
                    socket_client.connect((online_ip, online_port))
                    print(f" Con port {online_port} Host {online_ip} ")
                    print(tok)
                    socket_client.send(bytes.fromhex(tok))
                
                while True:
                    data2 = socket_client.recv(9999)
                    if data2 == b"":
                        print("Connection closed by remote host, attempting to reconnect...")
                        reconnect_attempt += 1
                        if reconnect_attempt <= max_reconnect_attempts:
                            print(f"Reconnect attempt {reconnect_attempt}/{max_reconnect_attempts}")
                            time.sleep(5)
                            if self.reconnect(tok, online_ip, online_port, packet, key, iv):
                                reconnect_attempt = 0
                                continue
                        else:
                            print("Max reconnect attempts reached, waiting 60 seconds...")
                            time.sleep(60)
                            reconnect_attempt = 0
                        break
                    
                    print(data2)
                    if "0500" in data2.hex()[0:4]:
                        accept_packet = f'08{data2.hex().split("08", 1)[1]}'
                        kk = get_available_room(accept_packet)
                        parsed_data = json.loads(kk)
                        fark = parsed_data.get("4", {}).get("data", None)
                        if fark is not None:
                            print(f"haaaaaaaaaaaaaaaaaaaaaaho {fark}")
                            if fark == 18:
                                if sent_inv:
                                    accept_packet = f'08{data2.hex().split("08", 1)[1]}'
                                    print(accept_packet)
                                    print(tempid)
                                    aa = gethashteam(accept_packet)
                                    ownerid = getownteam(accept_packet)
                                    print(ownerid)
                                    print(aa)
                                    ss = self.accept_sq(aa, tempid, int(ownerid))
                                    socket_client.send(ss)
                                    sleep(1)
                                    startauto = self.start_autooo()
                                    socket_client.send(startauto)
                                    start_par = False
                                    sent_inv = False
                            if fark == 6:
                                leaveee = True
                                print("kaynaaaaaaaaaaaaaaaa")
                            if fark == 50:
                                pleaseaccept = True
                        print(data2.hex())

                    if "0600" in data2.hex()[0:4] and len(data2.hex()) > 700:
                            accept_packet = f'08{data2.hex().split("08", 1)[1]}'
                            kk = get_available_room(accept_packet)
                            parsed_data = json.loads(kk)
                            print(parsed_data)
                            idinv = parsed_data["5"]["data"]["1"]["data"]
                            nameinv = parsed_data["5"]["data"]["3"]["data"]
                            senthi = True
                    if "0f00" in data2.hex()[0:4]:
                        packett = f'08{data2.hex().split("08", 1)[1]}'
                        print(packett)
                        kk = get_available_room(packett)
                        parsed_data = json.loads(kk)
                        
                        asdj = parsed_data["2"]["data"]
                        tempdata = get_player_status(packett)
                        if asdj == 15:
                            if tempdata == "OFFLINE":
                                tempdata = f"The id is {tempdata}"
                            else:
                                idplayer = parsed_data["5"]["data"]["1"]["data"]["1"]["data"]
                                idplayer1 = fix_num(idplayer)
                                if tempdata == "IN ROOM":
                                    idrooom = get_idroom_by_idplayer(packett)
                                    idrooom1 = fix_num(idrooom)
                                    
                                    tempdata = f"id : {idplayer1}\nstatus : {tempdata}\nid room : {idrooom1}"
                                    data22 = packett
                                    print(data22)
                                    
                                if "INSQUAD" in tempdata:
                                    idleader = get_leader(packett)
                                    idleader1 = fix_num(idleador)
                                    tempdata = f"id : {idplayer1}\nstatus : {tempdata}\nleader id : {idleador1}"
                                else:
                                    tempdata = f"id : {idplayer1}\nstatus : {tempdata}"
                            statusinfo = True 

                            print(data2.hex())
                            print(tempdata)
                        
                        

                        else:
                            pass
                    if "0e00" in data2.hex()[0:4]:
                        packett = f'08{data2.hex().split("08", 1)[1]}'
                        print(packett)
                        kk = get_available_room(packett)
                        parsed_data = json.loads(kk)
                        idplayer1 = fix_num(idplayer)
                        asdj = parsed_data["2"]["data"]
                        tempdata1 = get_player_status(packett)
                        if asdj == 14:
                            nameroom = parsed_data["5"]["data"]["1"]["data"]["2"]["data"]
                            
                            maxplayer = parsed_data["5"]["data"]["1"]["data"]["7"]["data"]
                            maxplayer1 = fix_num(maxplayer)
                            nowplayer = parsed_data["5"]["data"]["1"]["data"]["6"]["data"]
                            nowplayer1 = fix_num(nowplayer)
                            tempdata1 = f"{tempdata}\nRoom name : {nameroom}\nMax player : {maxplayer1}\nLive player : {nowplayer1}"
                            print(tempdata1)
                            
            except Exception as e:
                print(f"Error in sockf1: {e}, reconnecting...")
                reconnect_attempt += 1
                if reconnect_attempt <= max_reconnect_attempts:
                    time.sleep(5)
                else:
                    time.sleep(60)
                    reconnect_attempt = 0
    
    def connect(self, tok, packet, key, iv, whisper_ip, whisper_port, online_ip, online_port):
        global clients
        global socket_client
        global sent_inv
        global tempid
        global leaveee
        global start_par
        global nameinv
        global idinv
        global senthi
        global statusinfo
        global tempdata
        global pleaseaccept
        global tempdata1
        global data22
        
        max_reconnect_attempts = 10
        reconnect_attempt = 0
        
        while True:
            try:
                if reconnect_attempt == 0:
                    clients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    clients.connect((whisper_ip, whisper_port))
                    clients.send(bytes.fromhex(tok))
                
                thread = threading.Thread(
                    target=self.sockf1, args=(tok, online_ip, online_port, "anything", key, iv)
                )
                threads.append(thread)
                thread.start()

                while True:
                    data = clients.recv(9999)

                    if data == b"":
                        print("Connection closed by remote host, reconnecting...")
                        reconnect_attempt += 1
                        if reconnect_attempt <= max_reconnect_attempts:
                            print(f"Reconnect attempt {reconnect_attempt}/{max_reconnect_attempts}")
                            time.sleep(5)
                            try:
                                clients.close()
                            except:
                                pass
                            try:
                                clients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                clients.connect((whisper_ip, whisper_port))
                                clients.send(bytes.fromhex(tok))
                                reconnect_attempt = 0
                                continue
                            except:
                                continue
                        else:
                            print("Max reconnect attempts reached, waiting 60 seconds...")
                            time.sleep(60)
                            reconnect_attempt = 0
                        break

                    if senthi == True:
                        clients.send(
                                self.GenResponsMsg(
                                    f"""{generate_random_color()}╔══════════════════════════╗
{generate_random_color()}مرحبًا! شكرًا لإضافتي.
{generate_random_color()}لمعرفة الأوامر المتاحة،
{generate_random_color()}أرسل أي رسالة أو إيموجي.
{generate_random_color()}╠══════════════════════════╣
{generate_random_color()}هل أنت مهتم بشراء البوت
{generate_random_color()}تواصل مع المطور:
{generate_random_color()}تيليجرام: @knatri77
{generate_random_color()}╚══════════════════════════╝""", idinv
                                )
                        )
                        senthi = False
                    
                    if "1200" in data.hex()[0:4]:
                        json_result = get_available_room(data.hex()[10:])
                        print(data.hex())
                        parsed_data = json.loads(json_result)
                        try:
                            uid = parsed_data["5"]["data"]["1"]["data"]
                        except KeyError:
                            print("Warning: '1' key is missing in parsed_data, skipping...")
                            uid = None
                        if "8" in parsed_data["5"]["data"] and "data" in parsed_data["5"]["data"]["8"]:
                            uexmojiii = parsed_data["5"]["data"]["8"]["data"]
                            if uexmojiii == "DefaultMessageWithKey":
                                pass
                            else:
                                clients.send(
                                    self.GenResponsMsg(
                                    f"""[b][c]{generate_random_color()}VIP BOT FF

{generate_random_color()}Bot made for hacㅤking players

{generate_random_color()}To see commands send
{generate_random_color()}@help
ㅤㅤ
{generate_random_color()}Bot Makers
{generate_random_color()}⬇️⬇️⬇️⬇️⬇️

[b][c]{generate_random_color()}To renew bot duration
[b][c]{generate_random_color()}Telegram
{generate_random_color()}@knatri77

{generate_random_color()} VERSION 1""",uid
                                    )
                                )
                        else:
                            pass  

                    # ==================== الأوامر الأساسية ====================
                    
                    # أمر المساعدة
                    if "1200" in data.hex()[0:4] and b"@help" in data:
                        try:
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            user_name = parsed_data['5']['data']['9']['data']['1']['data']
                            uid = parsed_data["5"]["data"]["1"]["data"]
                            user_uid = str(uid)
                            if "***" in str(uid):
                                uid = rrrrrrrrrrrrrr(uid)
                            
                            time_msg = get_user_remaining_time(user_uid)
                            
                            print(f"\nUser With ID : {uid}\nName : {user_name}\nStarted Help\n")

                            clients.send(
                                self.GenResponsMsg(
                                    f"""
[b][c]{generate_random_color()}{time_msg}
""", uid
                                )
                            )
                            
                            time.sleep(0.5)
                            
                            clients.send(
                                self.GenResponsMsg(
                                    f"""
[b][c]{generate_random_color()}فتح سكواد 3 لاعبين
[b][c]{generate_random_color()}@3

[b][c]{generate_random_color()}فتح سكواد 5 لاعبين
[b][c]{generate_random_color()}@5

[b][c]{generate_random_color()}فتح سكواد 6 لاعبين
[b][c]{generate_random_color()}@6

[b][c]{generate_random_color()}فتح سكواد 3 لاعبين لصديقك
[b][c]{generate_random_color()}@3 [id]

[b][c]{generate_random_color()}فتح سكواد 5 لاعبين لصديقك
[b][c]{generate_random_color()}@5 [id]

[b][c]{generate_random_color()}فتح سكواد 6 لاعبين لصديقك
[b][c]{generate_random_color()}@6 [id]

[b][c]{generate_random_color()}دعوة لاعب معك للفريق
[b][c]{generate_random_color()}@inv [id]

""", uid

                                )
                            )
                            
                            time.sleep(0.5)
                            
                            clients.send(
                                self.GenResponsMsg(
                                    f"""
[b][c]{generate_random_color()}حالة اللاعب
[b][c]{generate_random_color()}@status [id]

[b][c]{generate_random_color()}سبام روم للاعب
[b][c]{generate_random_color()}@room [id]

[b][c]{generate_random_color()}فحص حالة الباند
[b][c]{generate_random_color()}@check [id]

[b][c]{generate_random_color()}شبح للفريق
[b][c]{generate_random_color()}@ghost [team] [name]

[b][c]{generate_random_color()}معلومات اللاعب
[b][c]{generate_random_color()}@info [id]

[b][c]{generate_random_color()}بايو اللاعب
[b][c]{generate_random_color()}@bio [id]

[b][c]{generate_random_color()}إرسال إعجابات للاعب
[b][c]{generate_random_color()}@like [id]

[b][c]{generate_random_color()}إرسال زيارات للاعب
[b][c]{generate_random_color()}@visit [id]

""", uid

                                )
                            )
                            
                            time.sleep(0.3)
                            
                            clients.send(
                                self.GenResponsMsg(
                                    f"""

[b][c]{generate_random_color()}سبام طلبات انضمام
[b][c]{generate_random_color()}@sp [id]

[b][c]{generate_random_color()}الخروج من السكواد
[b][c]{generate_random_color()}@exit

[b][c]{generate_random_color()}الانضمام للفريق
[b][c]{generate_random_color()}@join [team]

[b][c]{generate_random_color()}رسائل ملونة بالخاص
[b][c]{generate_random_color()}@mc [msg]

[b][c]{generate_random_color()}إرسال رقصات للاعبين
[b][c]{generate_random_color()}@emote [team] [emote_number] [uid1] [uid2] [uid3]

""", uid
                                )
                            )
                            
                            time.sleep(0.3)
                            
                            clients.send(
                                self.GenResponsMsg(
                                    f"""
[b][c]{generate_random_color()} للإدارة التواصل مع المطور
""", uid
                                )
                            )
                            
                        except Exception as e:
                            print(f"Error in @help: {e}")

                    # أوامر تغيير حجم الفريق
                    if "1200" in data.hex()[0:4] and b"@3" in data:
                        try:
                            data_str = str(data)
                            parts = data_str.split("@3")
                            if len(parts) > 1:
                                uid_part = parts[1].split("(\\x")[0] if "(\\x" in parts[1] else parts[1].split()[0] if parts[1].strip() else ""
                            else:
                                uid_part = ""
                            
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]

                            packetmaker = self.skwad_maker()
                            socket_client.send(packetmaker)
                            sleep(0.5)

                            packetfinal = self.changes(2)
                            socket_client.send(packetfinal)
                            sleep(0.5)

                            if uid_part and uid_part.isdigit():
                                iddd = uid_part
                                invitess = self.invite_skwad(iddd)
                                socket_client.send(invitess)

                            if uid:
                                clients.send(
                                    self.GenResponsMsg(
                                        f"""{generate_random_color()}جاري تحويل الفريق الي ثلاثي""",
                                        uid
                                    )
                                )

                            sleep(5)
                            leavee = self.leave_s()
                            socket_client.send(leavee)
                            sleep(1)
                            change_to_solo = self.changes(1)
                            socket_client.send(change_to_solo)
                        except Exception as e:
                            print(f"Error in @3: {e}")
                            
                    if "1200" in data.hex()[0:4] and b"@5" in data:
                        try:
                            data_str = str(data)
                            parts = data_str.split("@5")
                            if len(parts) > 1:
                                uid_part = parts[1].split("(\\x")[0] if "(\\x" in parts[1] else parts[1].split()[0] if parts[1].strip() else ""
                            else:
                                uid_part = ""
                            
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]

                            packetmaker = self.skwad_maker()
                            socket_client.send(packetmaker)
                            sleep(1)

                            packetfinal = self.changes(4)
                            socket_client.send(packetfinal)

                            if uid_part and uid_part.isdigit():
                                iddd = uid_part
                                invitess = self.invite_skwad(iddd)
                                socket_client.send(invitess)

                            if uid:
                                clients.send(
                                    self.GenResponsMsg(
                                        f"""{generate_random_color()}جاري تحويل الفريق الي خماسي""",
                                        uid))

                            sleep(5)
                            leavee = self.leave_s()
                            socket_client.send(leavee)
                            sleep(2)
                            change_to_solo = self.changes(1)
                            socket_client.send(change_to_solo)
                        except Exception as e:
                            print(f"Error in @5: {e}")
                        
                    if "1200" in data.hex()[0:4] and b"@6" in data:
                        try:
                            data_str = str(data)
                            parts = data_str.split("@6")
                            if len(parts) > 1:
                                uid_part = parts[1].split("(\\x")[0] if "(\\x" in parts[1] else parts[1].split()[0] if parts[1].strip() else ""
                            else:
                                uid_part = ""
                            
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]
                            
                            packetmaker = self.skwad_maker()
                            socket_client.send(packetmaker)
                            sleep(0.5)
                            packetfinal = self.changes(5)
                            
                            if uid_part and uid_part.isdigit():
                                iddd = uid_part
                            else:
                                iddd = uid
                            
                            socket_client.send(packetfinal)
                            invitess = self.invite_skwad(iddd)
                            socket_client.send(invitess)
                            
                            if uid:
                                clients.send(
                                    self.GenResponsMsg(
                                        f"""{generate_random_color()}جاري تحويل الفريق الي سداسي""",
                                        uid))

                            sleep(4)
                            leavee = self.leave_s()
                            socket_client.send(leavee)
                            sleep(0.5)
                            change_to_solo = self.changes(1)
                            socket_client.send(change_to_solo)
                        except Exception as e:
                            print(f"Error in @6: {e}")

                    # أمر دعوة لاعب للفريق
                    if "1200" in data.hex()[0:4] and b"@inv" in data:
                        try:
                            data_str = str(data)
                            parts = data_str.split("@inv")
                            if len(parts) > 1:
                                uid_part = parts[1].split("(\\x")[0] if "(\\x" in parts[1] else parts[1].split()[0] if parts[1].strip() else ""
                            else:
                                uid_part = ""
                            
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]
                            
                            if uid_part and uid_part.isdigit():
                                iddd = uid_part
                                packetmaker = self.skwad_maker()
                                socket_client.send(packetmaker)
                                sleep(1)
                                packetfinal = self.changes(4)
                                socket_client.send(packetfinal)
                                
                                invitess = self.invite_skwad(iddd)
                                socket_client.send(invitess)
                                invitessa = self.invite_skwad(uid)
                                socket_client.send(invitessa)
                                
                                clients.send(
                                    self.GenResponsMsg(
                                        f"""{generate_random_color()}جاري عمل فريق وارسال لك!""", uid
                                    )
                                )
                            else:
                                clients.send(
                                    self.GenResponsMsg(
                                        f"""{generate_random_color()}الرجاء إدخال معرف اللاعب!""", uid
                                    )
                                )

                            sleep(5)
                            leavee = self.leave_s()
                            socket_client.send(leavee)
                            sleep(5)
                            change_to_solo = self.changes(1)
                            socket_client.send(change_to_solo)
                            sleep(0.1)
                            clients.send(
                                self.GenResponsMsg(
                                    f"""{generate_random_color()}البوت اصبح سلو الان.""", uid
                                )
                            )
                        except Exception as e:
                            print(f"Error in @inv: {e}")
                                                                          
                    # أمر سبام روم
                    if "1200" in data.hex()[0:4] and b"@room" in data:
                        try:
                            data_str = str(data)
                            parts = data_str.split("@room")
                            if len(parts) > 1:
                                uid_part = parts[1].split("(\\x")[0] if "(\\x" in parts[1] else parts[1].split()[0] if parts[1].strip() else ""
                            else:
                                uid_part = ""
                            
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]
                            
                            if uid_part and uid_part.isdigit():
                                player_id = uid_part
                                if "***" in player_id:
                                    player_id = rrrrrrrrrrrrrr(player_id)
                                packetmaker = self.createpacketinfo(player_id)
                                socket_client.send(packetmaker)
                                sleep(0.5)
                                if "IN ROOM" in tempdata:
                                    room_id = get_idroom_by_idplayer(data22)
                                    packetspam = self.spam_room(room_id, player_id)
                                    clients.send(
                                        self.GenResponsMsg(
                                            f"""{generate_random_color()}جاري العمل علي طلب {fix_num(player_id)} ! """, uid
                                        )
                                    )
                                    for _ in range(99):
                                        threading.Thread(target=socket_client.send, args=(packetspam,)).start()
                                    clients.send(
                                        self.GenResponsMsg(
                                            f"""{generate_random_color()}نجح الطلب""", uid
                                        )
                                    )
                                else:
                                    clients.send(
                                        self.GenResponsMsg(
                                            f"""{generate_random_color()}اللاعب ليس في روم""", uid
                                        )
                                    )
                            else:
                                clients.send(
                                    self.GenResponsMsg(
                                        f"""{generate_random_color()}الرجاء كتابة ايدي اللاعب!""", uid
                                    )
                                )
                        except Exception as e:
                            print(f"Error in @room: {e}")

                    # أمر حالة اللاعب
                    if "1200" in data.hex()[0:4] and b"@status" in data:
                        try:
                            data_str = str(data)
                            parts = data_str.split("@status")
                            if len(parts) > 1:
                                uid_part = parts[1].split("(\\x")[0] if "(\\x" in parts[1] else parts[1].split()[0] if parts[1].strip() else ""
                            else:
                                uid_part = ""
                            
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]
                            
                            if uid_part and uid_part.isdigit():
                                player_id = uid_part
                                packetmaker = self.createpacketinfo(player_id)
                                socket_client.send(packetmaker)
                                statusinfo1 = True
                                while statusinfo1:
                                    if statusinfo == True:
                                        if "IN ROOM" in tempdata:
                                            inforoooom = self.info_room(data22)
                                            socket_client.send(inforoooom)
                                            sleep(0.5)
                                            clients.send(self.GenResponsMsg(f"{tempdata1}", uid))  
                                            tempdata = None
                                            tempdata1 = None
                                            statusinfo = False
                                            statusinfo1 = False
                                        else:
                                            clients.send(self.GenResponsMsg(f"{tempdata}", uid))  
                                            tempdata = None
                                            tempdata1 = None
                                            statusinfo = False
                                            statusinfo1 = False
                            else:
                                clients.send(self.GenResponsMsg(f"{generate_random_color()}الرجاء إدخال معرف اللاعب!", uid))  
                        except Exception as e:
                            print(f"Error in @status command: {e}")
                            clients.send(self.GenResponsMsg(f"{generate_random_color()}ERROR! {str(e)}", uid))

                    # أمر فحص الباند
                    if "1200" in data.hex()[0:4] and b"@check" in data:
                        try:
                            data_str = str(data)
                            parts = data_str.split("@check")
                            if len(parts) > 1:
                                uid_part = parts[1].split("(\\x")[0] if "(\\x" in parts[1] else parts[1].split()[0] if parts[1].strip() else ""
                            else:
                                uid_part = ""
                            
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]
                            
                            if uid_part and uid_part.isdigit():
                                player_id = uid_part
                                clients.send(
                                    self.GenResponsMsg(
                                        f"{generate_random_color()}جاري فحص حالة الباند...", uid
                                    )
                                )
                                result = check_banned_status(player_id)
                                if result["success"]:
                                    ban_status = result["is_banned"]
                                    if "مبند" in ban_status:
                                        status_color = "[FF0000]"
                                    else:
                                        status_color = "[00FF00]"
                                    
                                    player_id_formatted = fix_num(player_id)
                                    response_message = f"""
{generate_random_color()}——————————
{generate_random_color()}🆔 ID: {player_id_formatted}
{generate_random_color()}📊 Status: {status_color}{ban_status}
{generate_random_color()}⏰ Ban Period: {result['ban_period']} days
{generate_random_color()}——————————"""
                                    clients.send(self.GenResponsMsg(response_message, uid))
                                else:
                                    clients.send(self.GenResponsMsg(f"{generate_random_color()}❌ {result['message']}", uid))
                            else:
                                clients.send(self.GenResponsMsg(f"{generate_random_color()}الرجاء إدخال معرف لاعب صحيح!", uid))
                        except Exception as e:
                            print(f"Error in @check: {e}")
                            try:
                                clients.send(self.GenResponsMsg(f"{generate_random_color()}❌ حدث خطأ أثناء فحص الباند: {str(e)}", uid))
                            except:
                                pass

                    # أمر الشبح للفريق
                    if "1200" in data.hex()[0:4] and b"@ghost" in data:
                        handle_code_command(data, clients, socket_client, self.key, self.iv, get_available_room, self.GenResponsMsg)

                    # أمر الانضمام للفريق
                    if "1200" in data.hex()[0:4] and b"@join" in data:
                        try:
                            data_str = str(data)
                            parts = data_str.split("@join")
                            if len(parts) > 1:
                                team_code = parts[1].split("(\\x")[0] if "(\\x" in parts[1] else parts[1].split()[0] if parts[1].strip() else ""
                            else:
                                team_code = ""
                            
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]
                            
                            if team_code:
                                clients.send(
                                    self.GenResponsMsg(
                                        f"{generate_random_color()}جاري الانضمام للفريق {team_code}...", uid
                                    )
                                )
                                try:
                                    join_packet = GenJoinSquadsPacket(team_code, self.key, self.iv)
                                    socket_client.send(join_packet)
                                    time.sleep(1)
                                    clients.send(
                                        self.GenResponsMsg(
                                            f"{generate_random_color()}✅ تم الانضمام للفريق بنجاح!", uid
                                        )
                                    )
                                except Exception as e:
                                    print(f"Error in join: {e}")
                                    clients.send(self.GenResponsMsg(f"{generate_random_color()}❌ فشل في الانضمام للفريق: {str(e)}", uid))
                            else:
                                clients.send(self.GenResponsMsg(f"{generate_random_color()}الرجاء إدخال كود الفريق!", uid))
                        except Exception as e:
                            print(f"Error in @join: {e}")

                    # أمر الخروج من الفريق
                    if "1200" in data.hex()[0:4] and b"@exit" in data:
                        try:
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]

                            leavee = self.leave_s()
                            socket_client.send(leavee)
                            sleep(1)
                            change_to_solo = self.changes(1)
                            socket_client.send(change_to_solo)
                            clients.send(
                                self.GenResponsMsg(
                                    f"{generate_random_color()}تم الخروج من المجموعة.", uid
                                )
                            )
                        except Exception as e:
                            print(f"Error in @exit: {e}")

                    # أمر الرسائل الملونة
                    if "1200" in data.hex()[0:4] and b"@mc" in data:
                        try:
                            data_str = str(data)
                            parts = data_str.split("@mc")
                            if len(parts) > 1:
                                word = parts[1].split("(\\x")[0] if "(\\x" in parts[1] else parts[1].strip()
                            else:
                                word = ""
                            
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]
                            
                            if word:
                                for i in range(1, len(word) + 1):
                                    current_word = word[:i]
                                    clients.send(
                                        self.GenResponsMsg(
                                            f"{generate_random_color()}{current_word}", uid
                                        )
                                    )
                                    time.sleep(0.3)
                                
                                time.sleep(0.5)
                                clients.close()
                                if hasattr(self, 'CliEnts2') and self.CliEnts2:
                                    self.CliEnts2.close()
                                self.connect(self.AutH_ToKen, "anything", self.key, self.iv, self.whisper_ip, self.whisper_port, self.online_ip, self.online_port)
                                continue
                            else:
                                clients.send(
                                    self.GenResponsMsg(
                                        f"{generate_random_color()}❌ خطأ في الاستخدام!\nاستخدم: @mc رسالة", uid
                                    )
                                )
                        except Exception as e:
                            print(f"Error in @mc: {e}")

                    # أمر الرقصات
                    if "1200" in data.hex()[0:4] and b"@emote" in data:
                        try:
                            emote_map = {}
                            try:
                                with open('emotes.json', 'r') as f:
                                    emotes_data = json.load(f)
                                    for emote_entry in emotes_data:
                                        emote_map[emote_entry['Number']] = emote_entry['Id']
                            except FileNotFoundError:
                                logging.error("CRITICAL: emotes.json file not found!")
                                json_result = get_available_room(data.hex()[10:])
                                uid_sender = json.loads(json_result)["5"]["data"]["1"]["data"]
                                clients.send(self.GenResponsMsg(f"{generate_random_color()}❌ خطأ: ملف emotes.json مفقود.", uid_sender))
                                continue

                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid_sender = parsed_data["5"]["data"]["1"]["data"]

                            data_str = str(data)
                            parts = data_str.split('@emote')
                            if len(parts) > 1:
                                command_text = parts[1].split('(')[0].strip() if '(' in parts[1] else parts[1].strip()
                                command_parts = command_text.split()
                            else:
                                command_parts = []
                            
                            if len(command_parts) < 3:
                                clients.send(self.GenResponsMsg(
                                    f"""{generate_random_color()}❌ طريقة الاستخدام: @emote [uid1] [uid2] [uid3] [team_cod] [رقم الرقصة]""", uid_sender
                                ))
                                continue

                            emote_choice = command_parts[-1]
                            team_code = command_parts[-2]
                            target_ids = command_parts[:-2]
                            
                            if emote_choice not in emote_map:
                                max_emote_number = len(emote_map)
                                clients.send(self.GenResponsMsg(
                                    f"""{generate_random_color()}❌ رقم الرقصة غير صحيح! الرجاء استخدام رقم بين 1 و {max_emote_number}""", uid_sender
                                ))
                                continue
                            
                            emote_id_to_send = emote_map[emote_choice]
                            clients.send(self.GenResponsMsg(
                                f"{generate_random_color()}🎭 جاري الانضمام للفريق {team_code} وإرسال الرقصة #{emote_choice} إلى {len(target_ids)} لاعب...", uid_sender
                            ))
                            
                            join_packet = GenJoinSquadsPacket(team_code, self.key, self.iv)
                            socket_client.send(join_packet)
                            time.sleep(2)
                            
                            owner_id = uid_sender
                            clients.send(self.GenResponsMsg(
                                f"{generate_random_color()}✅ تم الانضمام للفريق بنجاح! جاري إرسال الرقصات...", uid_sender
                            ))
                            
                            for i, target_id in enumerate(target_ids, 1):
                                if target_id.isdigit() and emote_id_to_send.isdigit():
                                    emote_packet = self.send_emote(target_id, emote_id_to_send, owner_id)
                                    socket_client.send(emote_packet)
                                    clients.send(self.GenResponsMsg(
                                        f"{generate_random_color()}🔄 إرسال الرقصة #{emote_choice} إلى اللاعب {i} من {len(target_ids)}...", uid_sender
                                    ))
                                    time.sleep(0.5)
                            
                            clients.send(self.GenResponsMsg(
                                f"{generate_random_color()}✅ تم إرسال جميع الرقصات بنجاح! جاري الانتظار...", uid_sender
                            ))
                            
                            time.sleep(3)
                            leave_packet = self.leave_s()
                            socket_client.send(leave_packet)
                            clients.send(self.GenResponsMsg(
                                f"{generate_random_color()}🎉 تم إنهاء أمر الرقص بنجاح!", uid_sender
                            ))
                        except Exception as e:
                            logging.error(f"Error processing @emote command: {e}")

                    # أمر سبام طلبات الانضمام
                    if "1200" in data.hex()[0:4] and b"@sp" in data:  
                        try:  
                            json_result = get_available_room(data.hex()[10:])  
                            parsed_data = json.loads(json_result)  
                            uid = parsed_data["5"]["data"]["1"]["data"]  

                            data_str = str(data)
                            parts = data_str.split('@sp')
                            if len(parts) > 1:
                                uid_part = parts[1].split('(')[0].strip().split()[0] if parts[1].strip() else ""
                            else:
                                uid_part = ""
                              
                            if uid_part and uid_part.isdigit():  
                                player_id_str = uid_part  
                                clients.send(  
                                    self.GenResponsMsg(  
                                        f"{generate_random_color()}جاري إرسال 300 طلب انضمام لللاعب : {fix_num(player_id_str)}...", uid  
                                    )  
                                )  

                                socket_client.send(self.leave_s())  
                                time.sleep(0.5)  
                                socket_client.send(self.changes(1))  
                                time.sleep(0.5)  

                                invskwad_packet = self.request_join_squad(player_id_str)  
                                for _ in range(300):  
                                    socket_client.send(invskwad_packet)  
                                    sleep(0.1)  

                                clients.send(  
                                    self.GenResponsMsg(  
                                        f"{generate_random_color()}تم إرسال 300 طلب انضمام بنجاح!", uid  
                                    )  
                                )  

                                sleep(1)  
                                socket_client.send(self.leave_s())  
                            else:  
                                clients.send(  
                                    self.GenResponsMsg(  
                                        f"{generate_random_color()}❌ صيغة الأمر غير صالحة. الرجاء استخدام: @sp <معرف_اللاعب>", uid  
                                    )  
                                )  
                        except Exception as e:  
                            logging.error(f"Error in @sp command: {e}")

                    # أمر معلومات اللاعب
                    if "1200" in data.hex()[0:4] and b"@info" in data:
                        try:
                            data_str = str(data)
                            parts = data_str.split("@info")
                            if len(parts) > 1:
                                uid_part = parts[1].split("(\\x")[0] if "(\\x" in parts[1] else parts[1].split()[0] if parts[1].strip() else ""
                            else:
                                uid_part = ""
                            
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]
                            
                            if uid_part and uid_part.isdigit():
                                player_id = uid_part
                                clients.send(
                                    self.GenResponsMsg(
                                        f"{generate_random_color()}🔍 جاري جلب معلومات اللاعب...", uid
                                    )
                                )
                                info_message = get_player_info(player_id)
                                clients.send(self.GenResponsMsg(info_message, uid))
                            else:
                                clients.send(
                                    self.GenResponsMsg(
                                        f"{generate_random_color()}❌ الرجاء إدخال معرف لاعب صحيح!\nاستخدم: @info [id]", uid
                                    )
                                )
                        except Exception as e:
                            print(f"Error in @info: {e}")

                    # أمر بايو اللاعب
                    if "1200" in data.hex()[0:4] and b"@bio" in data:
                        try:
                            data_str = str(data)
                            parts = data_str.split("@bio")
                            if len(parts) > 1:
                                uid_part = parts[1].split("(\\x")[0] if "(\\x" in parts[1] else parts[1].split()[0] if parts[1].strip() else ""
                            else:
                                uid_part = ""
                            
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]
                            
                            if uid_part and uid_part.isdigit():
                                player_id = uid_part
                                bio_message = get_player_bio(player_id)
                                clients.send(self.GenResponsMsg(bio_message, uid))
                            else:
                                clients.send(
                                    self.GenResponsMsg(
                                        f"{generate_random_color()}❌ الرجاء إدخال معرف لاعب صحيح!\nاستخدم: @bio [id]", uid
                                    )
                                )
                        except Exception as e:
                            print(f"Error in @bio: {e}")

                    # أمر الإعجابات
                    if "1200" in data.hex()[0:4] and b"@like" in data:
                        try:
                            data_str = str(data)
                            parts = data_str.split("@like")
                            if len(parts) > 1:
                                uid_part = parts[1].split("(\\x")[0] if "(\\x" in parts[1] else parts[1].split()[0] if parts[1].strip() else ""
                            else:
                                uid_part = ""
                            
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]
                            
                            if uid_part and uid_part.isdigit():
                                player_id = uid_part
                                clients.send(
                                    self.GenResponsMsg(
                                        f"{generate_random_color()}❤️ جاري إرسال الإعجابات للاعب {fix_num(player_id)}...", uid
                                    )
                                )
                                like_result = get_player_likes(player_id)
                                like_message = like_result.get("message", "حدث خطأ غير متوقع")
                                clients.send(self.GenResponsMsg(like_message, uid))
                            else:
                                clients.send(
                                    self.GenResponsMsg(
                                        f"{generate_random_color()}❌ الرجاء إدخال معرف لاعب صحيح!\nاستخدم: @like [id]", uid
                                    )
                                )
                        except Exception as e:
                            print(f"Error in @like: {e}")

                    # أمر الزيارات
                    if "1200" in data.hex()[0:4] and b"@visit" in data:
                        try:
                            data_str = str(data)
                            parts = data_str.split("@visit")
                            if len(parts) > 1:
                                uid_part = parts[1].split("(\\x")[0] if "(\\x" in parts[1] else parts[1].split()[0] if parts[1].strip() else ""
                            else:
                                uid_part = ""
                            
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]
                            
                            if uid_part and uid_part.isdigit():
                                player_id = uid_part
                                clients.send(
                                    self.GenResponsMsg(
                                        f"{generate_random_color()}👤 جاري إرسال الزيارات للاعب {fix_num(player_id)}...", uid
                                    )
                                )
                                visit_message = send_visits(player_id)
                                clients.send(self.GenResponsMsg(visit_message, uid))
                            else:
                                clients.send(
                                    self.GenResponsMsg(
                                        f"{generate_random_color()}❌ الرجاء إدخال معرف لاعب صحيح!\nاستخدم: @visit [id]", uid
                                    )
                                )
                        except Exception as e:
                            print(f"Error in @visit: {e}")

            except Exception as e:
                print(f"Error in connect main loop: {e}")
                reconnect_attempt += 1
                if reconnect_attempt <= max_reconnect_attempts:
                    time.sleep(5)
                else:
                    time.sleep(60)
                    reconnect_attempt = 0

# ==================== تشغيل البوت بشكل مستمر ====================
if __name__ == "__main__":
    while True:
        try:
            with open('AlliFF.txt', 'r') as file:
                data = json.load(file)
            ids_passwords = list(data.items())

            all_threads = []

            def run_client(id, password):
                print(f"🚀 تشغيل البوت: ID: {id}")
                try:
                    client = FF_CLIENT(id, password)
                    client.start()
                except Exception as e:
                    print(f"❌ فشل تشغيل الحساب {id}: {e}")
                    time.sleep(5)

            for id, password in ids_passwords:
                thread = threading.Thread(target=lambda: run_client(id, password))
                all_threads.append(thread)
                time.sleep(2)
                thread.start()

            # استمر في التشغيل
            while True:
                time.sleep(60)
                print("✅ البوت يعمل...")

        except FileNotFoundError:
            print("❌ ملف AlliFF.txt غير موجود!")
            time.sleep(5)
        except json.JSONDecodeError as e:
            print(f"❌ خطأ في صيغة JSON: {e}")
            print("تأكد من أن ملف AlliFF.txt يحتوي على JSON صحيح")
            time.sleep(5)
        except Exception as e:
            print(f"⚠️ خطأ: {e}, إعادة المحاولة بعد 5 ثوان...")
            time.sleep(5)