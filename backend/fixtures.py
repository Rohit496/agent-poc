"""Swap this file with real DB/API calls when moving to production."""

ASSETS: dict[str, list[dict]] = {
    "P-10042": [
        {"id": "A-001", "party_number": "P-10042", "asset_type": "server", "name": "PROD-WEB-01", "status": "active", "location": "DC-East-Rack-12", "manufacturer": "Dell", "model": "PowerEdge R750", "serial_number": "SN-DEL-001", "purchase_date": "2022-03-15", "metadata": {"cpu_cores": 32, "ram_gb": 256, "storage_tb": 4}},
        {"id": "A-002", "party_number": "P-10042", "asset_type": "server", "name": "PROD-DB-01", "status": "active", "location": "DC-East-Rack-14", "manufacturer": "HP", "model": "ProLiant DL380", "serial_number": "SN-HP-002", "purchase_date": "2021-11-08", "metadata": {"cpu_cores": 64, "ram_gb": 512, "storage_tb": 8}},
        {"id": "A-003", "party_number": "P-10042", "asset_type": "server", "name": "DEV-APP-01", "status": "maintenance", "location": "DC-West-Rack-03", "manufacturer": "Dell", "model": "PowerEdge R640", "serial_number": "SN-DEL-003", "purchase_date": "2020-07-22", "metadata": {"cpu_cores": 16, "ram_gb": 128, "storage_tb": 2}},
        {"id": "A-004", "party_number": "P-10042", "asset_type": "hardware", "name": "CISCO-SW-01", "status": "active", "location": "DC-East-Rack-12", "manufacturer": "Cisco", "model": "Catalyst 9300", "serial_number": "SN-CSC-004", "purchase_date": "2023-01-10", "metadata": {"ports": 48, "speed_gbps": 10}},
    ],
    "P-20017": [
        {"id": "B-001", "party_number": "P-20017", "asset_type": "server", "name": "PROD-API-01", "status": "active", "location": "DC-North-Rack-07", "manufacturer": "Lenovo", "model": "ThinkSystem SR650", "serial_number": "SN-LNV-001", "purchase_date": "2023-05-20", "metadata": {"cpu_cores": 48, "ram_gb": 384, "storage_tb": 6}},
        {"id": "B-002", "party_number": "P-20017", "asset_type": "server", "name": "STAGE-WEB-01", "status": "inactive", "location": "DC-North-Rack-09", "manufacturer": "Dell", "model": "PowerEdge R540", "serial_number": "SN-DEL-005", "purchase_date": "2019-09-14", "metadata": {"cpu_cores": 12, "ram_gb": 64, "storage_tb": 1}},
        {"id": "B-003", "party_number": "P-20017", "asset_type": "hardware", "name": "ARUBA-AP-01", "status": "active", "location": "Office-Floor-2", "manufacturer": "Aruba", "model": "AP-515", "serial_number": "SN-ARB-001", "purchase_date": "2022-08-30", "metadata": {"wifi_standard": "WiFi 6"}},
        {"id": "B-004", "party_number": "P-20017", "asset_type": "hardware", "name": "UPS-MAIN-01", "status": "active", "location": "DC-North-PowerRoom", "manufacturer": "APC", "model": "Smart-UPS 3000", "serial_number": "SN-APC-001", "purchase_date": "2021-02-11", "metadata": {"capacity_kva": 3}},
        {"id": "B-005", "party_number": "P-20017", "asset_type": "hardware", "name": "SAN-STORAGE-01", "status": "active", "location": "DC-North-Rack-11", "manufacturer": "NetApp", "model": "AFF A400", "serial_number": "SN-NTP-001", "purchase_date": "2022-12-01", "metadata": {"capacity_tb": 96}},
    ],
    "P-30099": [
        {"id": "C-001", "party_number": "P-30099", "asset_type": "server", "name": "PROD-K8S-01", "status": "active", "location": "DC-South-Rack-01", "manufacturer": "HP", "model": "ProLiant DL360", "serial_number": "SN-HP-010", "purchase_date": "2023-03-08", "metadata": {"cpu_cores": 32, "ram_gb": 256}},
        {"id": "C-002", "party_number": "P-30099", "asset_type": "server", "name": "PROD-K8S-02", "status": "active", "location": "DC-South-Rack-01", "manufacturer": "HP", "model": "ProLiant DL360", "serial_number": "SN-HP-011", "purchase_date": "2023-03-08", "metadata": {"cpu_cores": 32, "ram_gb": 256}},
        {"id": "C-003", "party_number": "P-30099", "asset_type": "server", "name": "PROD-K8S-03", "status": "active", "location": "DC-South-Rack-02", "manufacturer": "Dell", "model": "PowerEdge R750", "serial_number": "SN-DEL-020", "purchase_date": "2023-06-15", "metadata": {"cpu_cores": 32, "ram_gb": 256}},
        {"id": "C-004", "party_number": "P-30099", "asset_type": "server", "name": "BACKUP-SRV-01", "status": "maintenance", "location": "DC-South-Rack-05", "manufacturer": "Lenovo", "model": "ThinkSystem SR530", "serial_number": "SN-LNV-030", "purchase_date": "2020-04-19", "metadata": {"storage_tb": 12}},
        {"id": "C-005", "party_number": "P-30099", "asset_type": "hardware", "name": "JUNIPER-FW-01", "status": "active", "location": "DC-South-Edge", "manufacturer": "Juniper", "model": "SRX345", "serial_number": "SN-JNP-001", "purchase_date": "2022-01-25", "metadata": {"throughput_gbps": 5}},
        {"id": "C-006", "party_number": "P-30099", "asset_type": "hardware", "name": "PDU-RACK-01", "status": "active", "location": "DC-South-Rack-01", "manufacturer": "Vertiv", "model": "Geist rPDU", "serial_number": "SN-VTV-001", "purchase_date": "2021-07-30", "metadata": {"outlets": 24}},
    ],
}
