#!/bin/bash

programas_python=("createDatabase.py" "createUserService.py" "insertNewsService.py" "loginUserService.py" "logoutService.py" "qualifyNewsService.py" "searchNewsService.py" "userConsultService.py" "viewAnalistService.py" "viewNewsService.py")

# Función para ejecutar programas en segundo plano
ejecutar_programas() {
    for programa in "${programas_python[@]}"; do
        # Verificar si el archivo existe
        if [ -e "$programa" ]; then
            echo "Ejecutando $programa en segundo plano..."
            python "$programa" &
            sleep 1  # Opcional: Esperar un segundo antes de ejecutar el siguiente script
        else
            echo "El archivo $programa no existe."
            break
        fi
    done

    # Esperar a que todos los programas finalicen
    wait
}

# Ejecutar programas en segundo plano
ejecutar_programas

# Bucle infinito para evitar que el script principal termine
while true; do
    echo "Presiona Ctrl+C para detener los programas y salir."
    sleep 1
done
