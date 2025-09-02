| ฟีเจอร์                                   |             Central             | OCPP Client | สิ่งที่ยังขาด                                            |
| ----------------------------------------- | :-----------------------------: | :---------: | -------------------------------------------------------- |
| BootNotification & Heartbeat              |                ✅                |      ❌      | ยังไม่มีการส่ง BootNotification/Heartbeat จากฝั่ง client |
| Authorize                                 |                ✅                |      ❌      | Client ยังไม่ส่ง `Authorize` ก่อนเริ่มธุรกรรม            |
| MeterValues                               |           ✅ (แค่ log)           |      ❌      | ยังไม่ส่งค่ากระแส/แรงดัน/SoC ฯลฯ                         |
| DataTransfer                              |                ✅                |      ❌      | Client ไม่รองรับการส่ง/รับ DataTransfer                  |
| Session data ขยายเก็บ sensor              |                ❌                |      ❌      | โครงสร้าง session ยังเก็บเฉพาะ meterStart/stop           |
| RemoteStart/RemoteStop                    |                ✅                |      ❌      | Client ไม่รองรับคำสั่งระยะไกล                            |
| StatusNotification                        |                ✅                |      ❌      | Client ไม่ส่งสถานะ Available/Charging/Finishing          |
| Change/Get Configuration & TriggerMessage | ✅ (ยังไม่รองรับ TriggerMessage) |      ❌      | Client ไม่รองรับ และ TriggerMessage ยังขาด               |
| UpdateFirmware                            |                ❌                |      ❌      | ยังไม่มีการจัดการอัปเดตเฟิร์มแวร์                        |
| Reset (Hard/Soft)                         |                ❌                |      ❌      | ยังไม่รองรับคำสั่งรีเซ็ต                                 |
