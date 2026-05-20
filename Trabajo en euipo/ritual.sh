#!/bin/bash

# ─── Nivel 5: Ritual Matutino ───────────────────────────────────────
# Proyecto final: Consulta de información diaria en el servidor Artemis.
# ─── Configuración ──────────────────────────────────────────────────
# Dirección del servidor de tu compañero adaptada a su IP del aula
SERVER_URL="10.0.140.35:8000"

# Colores para la interfaz
VERDE='\033[0;32m'
CIAN='\033[0;36m'
AMARILLO='\033[1;33m'
RESET='\033[0m'

# ─── Inicio del Ritual ─────────────────────────────────────────────
clear
echo -e "${AMARILLO}🌅 BIENVENIDO A TU RITUAL MATUTINO${RESET}"
echo "------------------------------------------------"

# Pedimos el nombre para buscar su agenda específica
read -p "Introduce tu nombre de usuario para el sistema: " usuario
echo -e "------------------------------------------------\n"

# 1. Obtención del Clima (Petición GET)
echo -e "${CIAN}[🌤️ ESTADO DEL TIEMPO]${RESET}"
clima=$(curl -s -f "$SERVER_URL/tiempo.txt")
if [ $? -eq 0 ]; then
    echo -e "$clima"
else
    echo "Información meteorológica no disponible actualmente."
fi
echo ""

# 2. Obtención de Noticias (Petición GET)
echo -e "${CIAN}[📰 ÚLTIMA HORA]${RESET}"
noticias=$(curl -s -f "$SERVER_URL/noticias.txt")
if [ $? -eq 0 ]; then
    echo -e "$noticias"
else
    echo "No hay noticias nuevas en el boletín."
fi
echo ""

# 3. Obtención de Agenda Personalizada (Petición GET)
echo -e "${CIAN}[📅 TU AGENDA: $usuario]${RESET}"

# Primero comprobamos si el archivo existe mirando el código HTTP (200=OK)
http_code=$(curl -s -o /dev/null -w "%{http_code}" "$SERVER_URL/agendas/$usuario.txt")

if [ "$http_code" -eq 200 ]; then
    # Si existe, lo descargamos y lo mostramos
    curl -s "$SERVER_URL/agendas/$usuario.txt"
else
    # Si da 404 u otro error, indicamos que no hay agenda
    echo -e "${AMARILLO}Aviso: No se ha encontrado ninguna agenda para el usuario '$usuario'.${RESET}"
fi

echo -e "\n------------------------------------------------"
echo -e "${VERDE}Se acabó el trabajo, ¡Que tengas un excelente día, $usuario!${RESET}"
echo ""
