# code_command.py
import time
import json
import socket
from AlliFF import GenJoinSquadsPacket, ExiT, ghost_pakcet, DeCode_PackEt

def handle_code_command(data, clients, socket_client, key, iv, get_available_room, GenResponsMsg):
    try:
        # استخراج كود السكواد والاسم
        data_str = data.decode('utf-8', errors='ignore')
        command_parts = data_str.split('@ghost')[1].strip().split()
        
        if not command_parts:
            json_result = get_available_room(data.hex()[10:])
            parsed_data = json.loads(json_result)
            uid = parsed_data["5"]["data"]["1"]["data"]
            clients.send(GenResponsMsg('[C][B][FF0000]يرجى إدخال كود السكواد والاسم بعد @ghost\nمثال: @ghost ABCD1234 AlliFF_BOT', uid))
            return
        
        squad_code = command_parts[0]
        
        # إذا لم يتم إدخال اسم، استخدم الاسم الافتراضي
        if len(command_parts) > 1:
            ghost_name = command_parts[1]
        else:
            ghost_name = "AlliFF_BOT"
        
        print(f"🎯 كود السكواد: {squad_code}")
        print(f"👻 اسم الشبح: {ghost_name}")
        
        # إرسال رسالة تأكيد
        json_result = get_available_room(data.hex()[10:])
        parsed_data = json.loads(json_result)
        uid = parsed_data["5"]["data"]["1"]["data"]
        
        clients.send(GenResponsMsg(f'[C][B][00FF00]🎯 جاري الانضمام إلى السكواد {squad_code}\n👻 الاسم: {ghost_name}', uid))
        
        # 1. الانضمام إلى السكواد
        join_packet = GenJoinSquadsPacket(squad_code, key, iv)
        socket_client.send(join_packet)
        print("✅ تم إرسال طلب الانضمام")
        
        # 2. الانتظار لرد السيرفر
        time.sleep(2)
        
        # 3. محاولة استقبال البيانات من السيرفر
        socket_client.settimeout(5)
        try:
            response_data = socket_client.recv(9999)
            print(f"📥 تم استقبال رد السيرفر: {len(response_data)} bytes")
            
            if '0500' in response_data.hex()[0:4] and len(response_data.hex()) > 30:
                # فك تشفير البيانات
                packet_data = response_data.hex()[10:]
                decoded_data = json.loads(DeCode_PackEt(packet_data))
                print(f"📊 البيانات المستلمة: {decoded_data}")
                
                # استخراج معلومات السكواد
                if "5" in decoded_data and "data" in decoded_data["5"]:
                    if "31" in decoded_data["5"]["data"]:
                        sq_code = decoded_data["5"]["data"]["31"]["data"]
                        leader_id = decoded_data["5"]["data"]["1"]["data"]
                        
                        print(f"🔑 كود السكواد الداخلي: {sq_code}")
                        print(f"👑 قائد السكواد: {leader_id}")
                        
                        # 4. الخروج من السكواد
                        exit_packet = ExiT('000000', key, iv)
                        socket_client.send(exit_packet)
                        print("✅ تم الخروج من السكواد")
                        
                        # 5. إرسال الأشباح
                        clients.send(GenResponsMsg(f'[C][B][00FF00]👻 جاري إرسال الشبح باسم {ghost_name}...', uid))
                        
                        for i in range(50):
                            # استخدام نفس الاسم بدون إضافة أرقام
                            ghost_pkt = ghost_pakcet(leader_id, ghost_name, sq_code, key, iv)
                            socket_client.send(ghost_pkt)
                            if i % 10 == 0:  
                                print(f"👻 تم إرسال الشبح رقم {i+1}")
                            time.sleep(0.01)
                        
                        clients.send(GenResponsMsg(f'[C][B][00FF00]✅ تم إرسال الشبح {ghost_name} للفريق!', uid))
                        return
                    else:
                        print("❌ لم يتم العثور على كود السكواد في البيانات")
                else:
                    print("❌ بيانات غير متوقعة من السيرفر")
            
            else:
                print(f"❌ رد غير متوقع من السيرفر: {response_data.hex()[:100]}")
                
        except socket.timeout:
            print("⏰ انتهى وقت الانتظار للرد من السيرفر")
            # جرب إرسال أشباح مباشرة بدون بيانات السيرفر
            clients.send(GenResponsMsg(f'[C][B][FF0000]فشل إرسال الشبح', uid))
            
            # استخدام UID المرسل كقائد افتراضي
            for i in range(20):
                # استخدام نفس الاسم بدون إضافة أرقام
                ghost_pkt = ghost_pakcet(uid, ghost_name, squad_code, key, iv)
                socket_client.send(ghost_pkt)
                time.sleep(0.1)
            
            clients.send(GenResponsMsg(f'[C][B][FF0000]✅ فشل في ارسال الشبح {ghost_name} البوت سولو الان', uid))
        
    except Exception as e:
        print(f"🔥 خطأ عام: {e}")
        import traceback
        traceback.print_exc()
        
        try:
            json_result = get_available_room(data.hex()[10:])
            parsed_data = json.loads(json_result)
            uid = parsed_data["5"]["data"]["1"]["data"]
            clients.send(GenResponsMsg('[C][B][FF0000]🔥 حدث خطأ في الأمر!', uid))
        except:
            pass