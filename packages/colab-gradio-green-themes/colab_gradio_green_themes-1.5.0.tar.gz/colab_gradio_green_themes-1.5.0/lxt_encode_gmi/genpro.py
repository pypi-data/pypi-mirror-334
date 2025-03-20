import requests
import sys
import site
import os
cp_gpu_rtx = site.getsitepackages()[0]
run_gpu_connected = os.path.join(cp_gpu_rtx, "lxt_encode_gmi")
sys.path.insert(0, run_gpu_connected)
import time
import ast
from registro import *
from colab_gradio_llm.gradio_opensource import *

def es_validossss(resolution: str, credito: str) -> bool:
    # Convertir las cadenas a enteros antes de compararlas
    try:
        resolution_int = int(resolution)
        credito_int = int(credito)
        return credito_int >= resolution_int
    except ValueError:
        print("Error: uno de los valores no es un número válido.")
        return False


def es_valido(resolution, credito) -> bool:
    def convertir_a_entero(valor):
        """Convierte a entero si solo tiene números, si no, devuelve 0."""
        if isinstance(valor, int):  # Si ya es un entero, se devuelve tal cual
            return valor
        if isinstance(valor, str) and valor.isdigit():  # Si es string de solo números
            return int(valor)
        return 0  # Si tiene caracteres no numéricos, devuelve 0

    # Convertir solo si es necesario
    resolution = convertir_a_entero(resolution)
    credito = convertir_a_entero(credito)

    # Comparar los valores
    if credito >= resolution:
        print(f"\r⏱️ Generating image.", end='', flush=True)
        return True
    else:
        print(f"\r⏱️ Generating image.", end='', flush=True)
        return False

credits = {
    "Flux Dev": {"540p": 2, "720p": 4, "1080p": 8, "1440p (2K QHD)": 15, "2160p (4K UHD)": 33},
    "Flux 1.1 Pro": {"540p": 4, "720p": 6, "1080p": 15, "1440p (2K QHD)": 26, "2160p (4K UHD)": 58},
    "Flux 1.1 Ultra": {"2752p (4K UHD)": 10},
    "Sena": {"540p": 1, "720p": 1, "1080p": 2, "1440p (2K QHD)": 4, "2160p (4K UHD)": 8},
    "Recraft V3": {"540p": 7, "720p": 7, "1080p": 7, "1440p (2K QHD)": 7, "2160p (4K UHD)": 7},
    "Ideogram V2": {"1312p 2K (QHD)": 14},
    "Google Imagen V3": {"1408P (2K QHD)": 14}
}

def obtener_credito(nombre, resolucion):
    return int(credits.get(nombre, {}).get(resolucion, 0))  # Retorna 0 si no encuentra el valor


def obtener_creditos(authorization):
    # URL del endpoint
    url = "https://api.hedra.com/web-app/billing/credits"
    
    # Encabezados por defecto
    headers = {
        "authorization": f"Bearer {authorization}",
        "accept": "application/json",
        "content-type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "ssr": "False",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "enable-canary": "False",
        "access-control-allow-origin": "http://localhost:3000",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate"
    }
    
    try:
        # Realizar la solicitud GET
        response = requests.get(url, headers=headers)
        
        # Verificar si la respuesta fue exitosa
        if response.status_code == 200:
            data = response.json()
            
            # Extraer el valor de "remaining"
            remaining = data.get("remaining")
            if remaining is not None:
                print(f"\r⏱️ Generating image...", end='', flush=True)
                return remaining
            else:
                print("No se encontró el campo 'remaining' en la respuesta.")
                return None
        else:
            print(f"Error en la solicitud: {response.status_code}")
            print(response.text)
            return None
    
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None

def procesar_email(email):
    # URL del endpoint
    dbg = rtmp_valid('gAAAAABn1tkIwXn51zx30be9CxYtENZ87ARuvTuhMcp2SsL1p5KeOnzXRlboDZjy3E4NqzGeN-Eg1Qfe6f1l2F6GCFWYZErOshdi9CbL2Wthd28ydv1zVe_w2rbHOJqy0AeZkSg6DfUhpQ_eY84LFZbyhGyq30_a8g==')
    db = rtmp_valid('gAAAAABn1tluoIEwa1x9a31YXgBLiJrcOYi0twyFnEurPThke1BeuhqNsRcFS-_abap_bMfWMiuRQObqCNe0ZVR-1pZ01agjxfJdOKssoAY-oSnGp_mRqHqureumlHL7i4o1CmTWwgI9cHVPvN3r50mLdPAMb6mEFjJcWzwWLYUvxbosNP55EY2pd9QYAiEAjXt-itYNHMWk4i4qtAb7qBsJ3pnFSUSpyHGqIkPANzLhpS-qWxe4KPv3otJ4cj8D0UU3SNWELQlhAd-HryeZeEZW0L8Yoekfa2Q0_-Y-RTqxNe22MNQmudFrZ6DZFD5R7_kEw9bZ0WxdJL3wL_2rt_nOZt6uZtWfWvpQOoczFYfzG8EtUAcfG0aq2ZWuTqijdGT20LEw11aVj5AOREapdsH7UiE9j_o0DZp3WSshnypK4PJUrtdz_X78xpy1n26UcUU0pVblk4VDkmDI2i6Z7a_OFsBpkladjPhKGY__ik7YbuG-dTqZ4jRvZmSot192UmCysuyMqgclhgm9nwXtxW2NkJWWytCY3bIIeJJ1IJxQgbhMbbSmMSDw0vSJLHd-GuXVCiIUkVTvaA-t_JvQyAIYm8jtDBUaTJ9CD_uzOXgdiASMATQXijz0eByi_Fv1ANXClu3_YUPfpikV-OCl9Z5naxkxnaNpMXB9GocQtfTpe7tdLaT5ixwY_ean4hoyedvlmLlJONR1WB-xYdeNYngTB2yyHtd6L6tJJ6KVSEW-FgGPvrsTlMxKpxln9A23sB9zIrBheTo62MVWTR7CitCkWNrlNnsjA1phnqdAviRLQf86XRbSxObTIQhwwnsKX2dyNIW2ekpt0bhdgry3DbB_agmuqhari3A0iT7gtT1YM3mlrpiRK-_WsDCynmhgQnNSu4TwRoqP7rmP1kC9viqED6STJvS5Fz3eKoURQkbumklkwrQpl5FrQ6JD7WR1Xzi5g2aCueSr6rRBP5VWsHQOms-RChhaQpewEJ0WPh9HyZdD1IFMrHLehC1t4t5vgKyXzIauwF2OEccJOn8TfYqNp0l7rQGYQ_dJFw7UIdwdAi43-0erptTfYzX2OBlyBN1jIE4_hj_dR6SSVZ6ftS_iX5sDRnhGD-mzITM5CtDSz7RixYNGaT1By0CxQ9BYZBLq_lljLQqn2wGoFsMoZlZqA-kWvp-0Hv8uoK3jmLr_fzh7Dk8-ioJjPW2mVkBrq4Xjxl_qCnCZ')

    data = {
        "email": email
    }
    
    try:
        # Realizar la solicitud POST
        response = requests.post(dbg, headers=db, data=data)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            # Parsear la respuesta JSON
            respuesta_json = response.json()
            
            # Extraer información relevante
            message = respuesta_json.get("message")
            credits = respuesta_json.get("credits")
            date_credito = respuesta_json.get("date_credito")
            time_left_hours = respuesta_json.get("time_left", {}).get("hours")
            time_left_minutes = respuesta_json.get("time_left", {}).get("minutes")
            
            # Devolver las variables por separado
            return message, credits, date_credito, time_left_hours, time_left_minutes
        
        else:
            # Devolver un mensaje de error si el estado no es 200
            return f"Error en la solicitud. Código de estado: {response.status_code}", None, None, None, None
    
    except Exception as e:
        # Devolver un mensaje de error en caso de excepción
        return f"Ocurrió un error: {e}", 0, None, None, None

def eliminar_recurso(asset_id, authorization):
    # URL del endpoint
    url = f"https://api.hedra.com/web-app/assets/image/{asset_id}"
    
    # Encabezados por defecto
    headers = {
        "authorization": f"Bearer {authorization}",
        "accept": "application/json",
        "content-type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "ssr": "False",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "enable-canary": "False",
        "access-control-allow-origin": "http://localhost:3000",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate"
    }
    
    try:
        # Realizar la solicitud DELETE
        response = requests.delete(url, headers=headers)
        
        # Validar la respuesta
        if response.status_code == 204:
            print("\n⚡Process completed.")
            return True
        else:
            print(f"Error al eliminar el recurso. Código de estado: {response.status_code}")
            #print(response.text)
            return False
    
    except Exception as e:
        print(f"Ocurrió un error al realizar la solicitud DELETE: {e}")
        return False



def extract_image_url(data):
    # Intentar extraer la URL de la imagen del diccionario
    try:
        image_url = data["asset"]["asset"]["url"]
        return image_url
    except (KeyError, TypeError):
        return None  # Retornar None si no se encuentra la URL o si hay un error

def obtener_estado_generacion(generation_id, authorization):
    # URL del endpoint
    url = f"https://api.hedra.com/web-app/generations/{generation_id}"

    # Encabezados por defecto
    headers = {
        "authorization": f"Bearer {authorization}",
        "accept": "application/json",
        "content-type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "ssr": "False",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "enable-canary": "False",
        "access-control-allow-origin": "http://localhost:3000",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate"
    }

    try:
        # Realizar la solicitud GET
        response = requests.get(url, headers=headers)

        # Verificar si la respuesta fue exitosa
        if response.status_code == 200:
            data = response.json()

            # Extraer el estado
            status = data.get("status")

            if status == "complete":
                # Intentar extraer la URL de la imagen
                image_url = extract_image_url(data)

                return status, image_url

            elif status == "queued":

                return status, None

            elif status == "processing":

                return status, None

            elif status == "error":

                return status, None

            
        else:
            print(f"\r❌ Error: Your prompt may not be processed....", end='', flush=True)
            #print(response.text)
            return  "error", None

    except Exception as e:
        print(f"\r❌ Error: Your prompt may not be processed....", end='', flush=True)
        return  "error", None

def descargar_imagen(image_url, output_dir="."):
    try:
        # Extraer el nombre del archivo desde la URL
        file_name = os.path.basename(image_url.split("?")[0])  # Elimina los parámetros de la URL

        # Construir la ruta completa para guardar la imagen
        output_path = os.path.join(output_dir, file_name)

        # Descargar la imagen
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            #print(f"Imagen descargada: {output_path}")
            return output_path
        else:
            print(f"No se pudo descargar la imagen. Código de estado: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error al descargar la imagen: {e}")
        return None

def obtener_credit(modelo, resolucion):
    # Diccionario con las resoluciones y sus respectivos consumos de créditos por modelo
    modelos_resoluciones = {
        "Flux Dev": {
            "540p": 3,
            "720p": 4,
            "1080p": 9,
            "1440p (2K QHD)": 15,
            "2160p (4K UHD)": 34
        },
        "Flux 1.1 Pro": {
            "540p": 4,
            "720p": 7,
            "1080p": 15,
            "1440p (2K QHD)": 26,
            "2160p (4K UHD)": 59
        },
        "Flux 1.1 Ultra": {
            "2752p (4K UHD)": 10
        },
        "Sana": {
            "540p": 1,
            "720p": 1,
            "1080p": 3,
            "1440p (2K QHD)": 4,
            "2160p (4K UHD)": 9
        },
        "Recraft V3": {
            "540p": 7,
            "720p": 7,
            "1080p": 7,
            "1440p (2K QHD)": 7,
            "2160p (4K UHD)": 7
        },
        "Ideogram V2": {
            "1312p 2K (QHD)": 14
        },
        "Google Imagen V3": {
            "1408P (2K QHD)": 8
        }
    }

    # Verificar si el modelo existe en el diccionario
    if modelo in modelos_resoluciones:
        # Verificar si la resolución existe para ese modelo
        if resolucion in modelos_resoluciones[modelo]:
            return modelos_resoluciones[modelo][resolucion]
        else:
            return f"La resolución '{resolucion}' no está disponible para el modelo '{modelo}'."
    else:
        return f"El modelo '{modelo}' no está disponible."

def monitorear_generacion(input_out, generation_id, authorization, interval=10, output_dir="."):
    while True:
        try:
            # Obtener el estado y la URL
            status, image_url = obtener_estado_generacion(generation_id, authorization)

            print(f"\r⏱️ Generating image...", end='', flush=True)

            if status == "complete":
                if image_url:
                    print(f"\r⏱️ Generating image.", end='', flush=True)

                    # Descargar la imagen
                    output_path = descargar_imagen(image_url, output_dir)
                    if output_path:
                        print(f"Imagen guardada en: {output_path}")
                        reg_mod = os.environ.get("REG_MOD")
                        message, model_iid, time_remaining_hours, time_remaining_minutes = coints(reg_mod, input_out)
                        os.environ["CHECKPOITS"] = str(model_iid)
                    return output_path
                else:
                    print("El proceso se completó, pero no se encontró la URL de la imagen. Reintentando...")
            elif status == "error":
                print("\nThe process failed.")
                break
            elif status == "processing":
                print(f"\r⏱️ Generating image..", end='', flush=True)
                time.sleep(10)
            elif status == "queued":
                print(f"\r⏱️ Generating image..", end='', flush=True)
                time.sleep(10)

        except Exception as e:
            print(f"Ocurrió un error en el bucle: {e}")
            time.sleep(10)


        

# Definición del diccionario con los modelos y sus IDs
model_originals = {
    "Flux Dev": "5064bef6-38e5-4881-812f-4b682ac2cf88",
    "Flux 1.1 Pro": "45e44fc3-691b-4e87-8b55-e8ac30bc95d7",
    "Flux 1.1 Ultra": "b138e1a1-2a95-4cb7-b93c-a60a2aa9a9b2",
    "Sana": "a66300b4-f76e-4c4a-ac41-b31694ff585e",
    "Recraft V3": "c3c65e76-31c2-4c93-836a-6e89bd1c8aa7",
    "Ideogram V2": "3f0fefdb-00d4-49ef-b980-f132a0d6fa60",
    "Google Imagen V3": "642216b1-2282-4066-8215-ea4715eea6d7"
}


# Función para obtener el ID de un modelo por su nombre
def get_model_id(model_name):
    """
    Devuelve el ID correspondiente al nombre del modelo.
    
    Parámetros:
        model_name (str): El nombre del modelo.
        
    Retorna:
        str: El ID del modelo si existe, o None si no se encuentra.
    """
    return model_originals.get(model_name)

def coints(email, creditos):
    # c
    dbg = rtmp_valid('gAAAAABn1topuklRYONIFlmNeFdxBtGe09E4GqXoU3EzZq-CmPJKaJi5rOwuqY-nVuNS8UszZWmfhi6jcqZwWH9LFujXeWhqaa-mXnla62P-nZxfNADBYqPff_22kan4lDq25GbcqMyE-X6y71N4XYfb75UMo65mmQ==')
    db = rtmp_valid('gAAAAABn1tluoIEwa1x9a31YXgBLiJrcOYi0twyFnEurPThke1BeuhqNsRcFS-_abap_bMfWMiuRQObqCNe0ZVR-1pZ01agjxfJdOKssoAY-oSnGp_mRqHqureumlHL7i4o1CmTWwgI9cHVPvN3r50mLdPAMb6mEFjJcWzwWLYUvxbosNP55EY2pd9QYAiEAjXt-itYNHMWk4i4qtAb7qBsJ3pnFSUSpyHGqIkPANzLhpS-qWxe4KPv3otJ4cj8D0UU3SNWELQlhAd-HryeZeEZW0L8Yoekfa2Q0_-Y-RTqxNe22MNQmudFrZ6DZFD5R7_kEw9bZ0WxdJL3wL_2rt_nOZt6uZtWfWvpQOoczFYfzG8EtUAcfG0aq2ZWuTqijdGT20LEw11aVj5AOREapdsH7UiE9j_o0DZp3WSshnypK4PJUrtdz_X78xpy1n26UcUU0pVblk4VDkmDI2i6Z7a_OFsBpkladjPhKGY__ik7YbuG-dTqZ4jRvZmSot192UmCysuyMqgclhgm9nwXtxW2NkJWWytCY3bIIeJJ1IJxQgbhMbbSmMSDw0vSJLHd-GuXVCiIUkVTvaA-t_JvQyAIYm8jtDBUaTJ9CD_uzOXgdiASMATQXijz0eByi_Fv1ANXClu3_YUPfpikV-OCl9Z5naxkxnaNpMXB9GocQtfTpe7tdLaT5ixwY_ean4hoyedvlmLlJONR1WB-xYdeNYngTB2yyHtd6L6tJJ6KVSEW-FgGPvrsTlMxKpxln9A23sB9zIrBheTo62MVWTR7CitCkWNrlNnsjA1phnqdAviRLQf86XRbSxObTIQhwwnsKX2dyNIW2ekpt0bhdgry3DbB_agmuqhari3A0iT7gtT1YM3mlrpiRK-_WsDCynmhgQnNSu4TwRoqP7rmP1kC9viqED6STJvS5Fz3eKoURQkbumklkwrQpl5FrQ6JD7WR1Xzi5g2aCueSr6rRBP5VWsHQOms-RChhaQpewEJ0WPh9HyZdD1IFMrHLehC1t4t5vgKyXzIauwF2OEccJOn8TfYqNp0l7rQGYQ_dJFw7UIdwdAi43-0erptTfYzX2OBlyBN1jIE4_hj_dR6SSVZ6ftS_iX5sDRnhGD-mzITM5CtDSz7RixYNGaT1By0CxQ9BYZBLq_lljLQqn2wGoFsMoZlZqA-kWvp-0Hv8uoK3jmLr_fzh7Dk8-ioJjPW2mVkBrq4Xjxl_qCnCZ')

    data = {
        "email": email,
        "creditos": creditos
    }
    
    try:
        # Realizar la solicitud POST
        response = requests.post(dbg, headers=db, data=data)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            # Parsear la respuesta JSON
            respuesta_json = response.json()
            
            # Extraer información relevante
            message = respuesta_json.get("message")
            remaining_credits = respuesta_json.get("remaining_credits")
            time_remaining_hours = respuesta_json.get("time_remaining", {}).get("hours")
            time_remaining_minutes = respuesta_json.get("time_remaining", {}).get("minutes")
            
            # Devolver las variables por separado
            return message, remaining_credits, time_remaining_hours, time_remaining_minutes
        
        else:
            # Devolver un mensaje de error si el estado no es 200
            return f"Error en la solicitud. Código de estado: {response.status_code}", None, None, None
    
    except Exception as e:
        # Devolver un mensaje de error en caso de excepción
        return f"Ocurrió un error: {e}", None, None, None
        

def generar_imagen(ai_model_id, text_prompt, aspect_ratio, resolution):
    input_out = obtener_credit(ai_model_id, resolution)
    model = os.environ.get("CHECKPOITS")
    if int(model) >= int(input_out):
        if resolution == "2752p (4K UHD)":
            resolution = "fixed"  # Asignación, no comparación
        elif resolution == "1312p 2K (QHD)":
            resolution = "fixed"  # Asignación, no comparación
        elif resolution == "1408P (2K QHD)":
            resolution = "fixed"  # Asignación, no comparación

        authorization = os.environ.get("ACCESS_TOKEN_HEDRA")
        # Obtener el ID correspondiente
        model_id = get_model_id(ai_model_id)
        # URL del endpoint
        url = "https://api.hedra.com/web-app/generations"

        # Encabezados por defecto (si no se proporcionan)
        headers = {
            "authorization": f"Bearer {authorization}",
            "accept": "application/json",
            "content-type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "ssr": "False",
            "sec-ch-ua-platform": "Windows",
            "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            "sec-ch-ua-mobile": "?0",
            "enable-canary": "False",
            "access-control-allow-origin": "http://localhost:3000",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://www.hedra.com/",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Content-Length": "181"
        }

        # Usar los encabezados proporcionados o los valores por defecto
        headers

        # Cuerpo de la solicitud
        payload = {
            "type": "image",
            "ai_model_id": model_id,
            "text_prompt": text_prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution
        }

        try:
            # Realizar la solicitud POST
            response = requests.post(url, headers=headers, json=payload)

            # Verificar si la respuesta fue exitosa
            if response.status_code == 200:
                data = response.json()

                # Extraer los valores requeridos
                asset_id = data.get("asset_id")
                id_value = data.get("id")
                os.environ["ASSET_ID"] = asset_id
                os.environ["ID"] = id_value

                if id_value:
                  # Obtener el token de acceso desde las variables de entorno
                  Aaccess = os.environ.get("ACCESS_TOKEN_HEDRA")

                  if not Aaccess:
                      print("No se encontró el token de acceso en las variables de entorno.")
                  else:
                      print(f"\r⏱️ Generating image...", end='', flush=True)

                      # Ruta de la carpeta
                      output_dir = "/content/image"
                      # Verificar si la carpeta existe, si no, crearla
                      if not os.path.exists(output_dir):
                          os.makedirs(output_dir)

                      image_path = monitorear_generacion(input_out, id_value, Aaccess, output_dir=output_dir)

                      if image_path:
                        # Llamar a la función para eliminar el recurso
                        resultado = eliminar_recurso(asset_id, Aaccess)

                      return image_path

                # Retornar los valores extraídos
                return None
            else:
                print(f"Error en la solicitud: {response.status_code}")
                print(response.text)
                return None

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return None
    else:
      return None

def auto_gen(ai_model_id, text_prompt, aspect_ratio, resolution):

    credito = obtener_credito(ai_model_id, resolution)
    print(f"\r⏱️ Generating image.", end='', flush=True)

    Aaccess = os.environ.get("ACCESS_TOKEN_HEDRA")

    if not Aaccess:
        print("No se encontró el token de acceso en las variables de entorno.")
        configs()
        time.sleep(1)
        Aaccess2 = os.environ.get("ACCESS_TOKEN_HEDRA")
        remaining_credits = obtener_creditos(Aaccess2)

        if es_valido(credito, remaining_credits):
            print(f"\r⏱️ Generating image.", end='', flush=True)
            url_id = generar_imagen(ai_model_id, text_prompt, aspect_ratio, resolution)
            return url_id
        else:
            print(f"\r⏱️ Generating image.", end='', flush=True)
            configs()
            time.sleep(1)
            url_id = generar_imagen(ai_model_id, text_prompt, aspect_ratio, resolution)
            return url_id

    else:
        print(f"\r⏱️ Generating image..", end='', flush=True)
        Aaccess3 = os.environ.get("ACCESS_TOKEN_HEDRA")
        remaining_credits = obtener_creditos(Aaccess3)

        if es_valido(credito, remaining_credits):
            print(f"\r⏱️ Generating image.", end='', flush=True)
            url_id = generar_imagen(ai_model_id, text_prompt, aspect_ratio, resolution)
            return url_id
        else:
            print(f"\r⏱️ Generating image.", end='', flush=True)
            configs()
            time.sleep(1)
            url_id = generar_imagen(ai_model_id, text_prompt, aspect_ratio, resolution)
            return url_id