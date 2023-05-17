import os
import subprocess

# Hangi hetke töökaust
current_directory = os.getcwd()

# Käsk töökausta muutmiseks
change_directory_cmd = f'cd /d {current_directory}'

# Käivita töökausta muutmise käsk
subprocess.run(change_directory_cmd, shell=True)

exiftool_cmd = ['exiftool', '-E', '-p', 'kml.fmt', 'Images']
# Käsk KML-faili loomiseks Exiftooli abil
with open('main.kml', 'w', encoding='utf-8') as kml_file:
    subprocess.run(exiftool_cmd, stdout=kml_file)

# Käsk GPS-koordinaatide väljavõtmiseks Exiftooli abil
extract_coordinates_cmd = ['exiftool', '-T', '-c', '%.6f', '-filepath', '-GPSLatitude', '-GPSLongitude', '-GPSAltitude', 'Images']

# Käivita käsk GPS-koordinaatide väljavõtmiseks ja salvestamiseks tekstifaili
result = subprocess.run(extract_coordinates_cmd, capture_output=True, text=True)

# Salvesta vastus tekstifaili
coordinates_file = 'coordinates.txt'
with open(coordinates_file, 'w', encoding='utf-8') as file:
    file.write('File\'i teekond;Laiuskraad;Pikkuskraad;Kõrgus:\n')

    # Formaatige ja salvesta koordinaadid
    for line in result.stdout.strip().split('\n'):
        parts = line.split('\t')
        if len(parts) >= 4:
            filepath = parts[0].strip('"')
            latitude_str = parts[1].strip(' N"')
            longitude_str = parts[2].strip(' E"')
            altitude = parts[3].strip(' m Above Sea Level" E')

            if latitude_str == '-' or longitude_str == '-':
                latitude = longitude = "N/A"
            else:
                latitude = float(latitude_str)
                longitude = float(longitude_str)

            formatted_line = f"{filepath};{latitude if latitude != 'N/A' else '-'};{longitude if longitude != 'N/A' else '-'};{altitude}"
            file.write(formatted_line + '\n')
