python -m py_compile central.py ocpp_client.py

python -m py_compile ocpp_client.py central.py

python -m py_compile ocpp_client.py

python -m py_compile ocpp_client.py central.py

สาธิตการทำงาน

เปิดเทอร์มินัล A รัน python central.py

เปิดเทอร์มินัล B รัน python ocpp_client.py

ผลลัพธ์ที่คาดหวังจาก central.py

หลัง ocpp_client.py เชื่อมต่อ จะมี log ลักษณะ
BootNotification received: status=Accepted interval=60

ทุก ๆ interval (ตัวอย่าง 60 วินาที) จะมี log
Heartbeat received at 2024-xx-xx HH:MM:SS

ผลลัพธ์ที่คาดหวังจาก ocpp_client.py

หลังเชื่อมต่อจะส่ง BootNotification ทันที แล้วขึ้นข้อความ (หรือ log) ยืนยันว่าได้รับ interval

จะมีการส่ง Heartbeat โดย background task และแจ้งใน log ว่ากำลังส่งอยู่


| ฟีเจอร์                                   |             Central             | OCPP Client | สิ่งที่ยังขาด                                   |
| ----------------------------------------- | :-----------------------------: | :---------: | ----------------------------------------------- |
| BootNotification & Heartbeat              |                ✅                |      ✅      | —                                               |
| Authorize                                 |                ✅                |      ❌      | Client ยังไม่ส่ง `Authorize` ก่อนเริ่มธุรกรรม   |
| MeterValues                               |           ✅ (แค่ log)           |      ❌      | ยังไม่ส่งค่ากระแส/แรงดัน/SoC ฯลฯ                |
| DataTransfer                              |                ✅                |      ❌      | Client ไม่รองรับการส่ง/รับ DataTransfer         |
| Session data ขยายเก็บ sensor              |                ❌                |      ❌      | โครงสร้าง session ยังเก็บเฉพาะ meterStart/stop  |
| RemoteStart/RemoteStop                    |                ✅                |      ❌      | Client ไม่รองรับคำสั่งระยะไกล                   |
| StatusNotification                        |                ✅                |      ❌      | Client ไม่ส่งสถานะ Available/Charging/Finishing |
| Change/Get Configuration & TriggerMessage | ✅ (ยังไม่รองรับ TriggerMessage) |      ❌      | Client ไม่รองรับ และ TriggerMessage ยังขาด      |
| UpdateFirmware                            |                ❌                |      ❌      | ยังไม่มีการจัดการอัปเดตเฟิร์มแวร์               |
| Reset (Hard/Soft)                         |                ❌                |      ❌      | ยังไม่รองรับคำสั่งรีเซ็ต                        |
