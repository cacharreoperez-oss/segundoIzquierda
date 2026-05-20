import http.server
import os
import datetime

class ArtemisHandler(http.server.SimpleHTTPRequestHandler):
    # Esta función se ejecuta cada vez que tú haces un POST desde nivel4.sh
    def do_POST(self):
        # 1. Leer cuántos bytes envías
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        
        # 2. Obtener metadatos (fecha, hora, IP)
        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip_cliente = self.client_address[0]
        
        # 3. Intentar extraer el nombre del agente del reporte para el log
        agente = "Agente Desconocido"
        try:
            lineas = body.decode('utf-8', errors='ignore').split('\n')
            for linea in lineas:
                if "REPORTE DE AGENTE:" in linea:
                    agente = linea.split(":")[1].strip()
                    break
        except:
            pass

        # 4. Guardar el contenido en el archivo único (~/nivel5/reporte.log)
        ruta_log = os.path.expanduser('~/nivel5/reporte.log')
        os.makedirs(os.path.dirname(ruta_log), exist_ok=True)
        with open(ruta_log, 'ab') as f:
            # Escribimos un encabezado con la información solicitada
            encabezado = f"\n[NUEVO REPORTE]\nFECHA/HORA: {fecha_hora}\nORIGEN (IP): {ip_cliente}\nUSUARIO: {agente}\n"
            f.write(encabezado.encode())
            f.write(b"-"*20 + b"\n")
            f.write(body)
            # Añadimos un separador final
            f.write(b"\n" + b"="*40 + b"\n")
            
        print(f"\n[!] ¡ALERTA! Reporte recibido de {agente} ({ip_cliente})")
        # 4. Responder al cliente (a ti) que todo ha ido bien
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"RECIBIDO")

    # Sobrescribimos log_message para registrar cada petición en reporte.log
    def log_message(self, format, *args):
        log_line = "%s - - [%s] %s\n" % (
            self.address_string(),
            self.log_date_time_string(),
            format % args
        )
        ruta_log = os.path.expanduser('~/nivel5/reporte.log')
        try:
            with open(ruta_log, 'ab') as f:
                f.write(log_line.encode('utf-8'))
        except:
            pass
        # Muestra también en la consola del servidor
        super().log_message(format, *args)

# Aseguramos que la carpeta y el archivo de log existan al arrancar el servidor
ruta_log_inicio = os.path.expanduser('~/nivel5/reporte.log')
os.makedirs(os.path.dirname(ruta_log_inicio), exist_ok=True)

# Recopilamos información del servidor para el reporte de arranque
fecha_arranque = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
hostname_srv = os.popen('hostname').read().strip()
ip_srv = os.popen("hostname -I | awk '{print $1}'").read().strip()
cpu_uptime = os.popen('uptime -p').read().strip()
disco_libre = os.popen("df -h / | awk 'NR==2 {print $4}'").read().strip()
ram_libre = os.popen("free -h | awk '/^Mem:/ {print $7}'").read().strip()

reporte_inicio = f"""
==================================================
🖥️  INICIO DE SERVIDOR ARTEMIS (GROUND CONTROL)
==================================================
FECHA DE ARRANQUE : {fecha_arranque}
HOSTNAME          : {hostname_srv}
IP SERVIDOR       : {ip_srv}
UPTIME            : {cpu_uptime}
DISCO DISPONIBLE  : {disco_libre}
RAM DISPONIBLE    : {ram_libre}
==================================================
\n"""

with open(ruta_log_inicio, 'ab') as f:
    f.write(reporte_inicio.encode('utf-8'))

# Iniciamos el servidor en todas las interfaces (0.0.0.0) y puerto 8000
print("=== GROUND CONTROL: ESCUCHANDO EN EL PUERTO 8000 ===")
print(f"[i] Reporte de inicio guardado en: {ruta_log_inicio}")
http.server.HTTPServer(('0.0.0.0', 8000), ArtemisHandler).serve_forever()