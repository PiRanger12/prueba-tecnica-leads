"""
Módulo de Procesamiento y Limpieza de Leads
Completa las funciones indicadas para limpiar, validar y generar métricas del dataset.
"""
import os
import pandas as pd
import requests

DATA_IN = os.path.join(os.path.dirname(__file__), "..", "data", "leads.csv")
DATA_OUT = os.path.join(os.path.dirname(__file__), "..", "data", "leads_limpios.csv")

API_URL = "http://127.0.0.1:8000/api/leads"
API_TOKEN = "atlas-token-2026"

# Mapeo de posibles variantes de estatus a los valores canónicos
ESTATUS_CANONICOS = {
    "NUEVO": "NUEVO",
    "NEW": "NUEVO",
    "CONTACTADO": "CONTACTADO",
    "CONTACTED": "CONTACTADO",
    "EN_SEGUIMIENTO": "EN_SEGUIMIENTO",
    "EN SEGUIMIENTO": "EN_SEGUIMIENTO",
    "SEGUIMIENTO": "EN_SEGUIMIENTO",
    "FOLLOW_UP": "EN_SEGUIMIENTO",
    "FOLLOWUP": "EN_SEGUIMIENTO",
    "CONVERTIDO": "CONVERTIDO",
    "CONVERTED": "CONVERTIDO",
    "GANADO": "CONVERTIDO",
    "PERDIDO": "PERDIDO",
    "LOST": "PERDIDO",
    "CANCELADO": "PERDIDO",
}


def cargar_datos() -> pd.DataFrame:
    """1. Cargar el dataset crudo."""
    df = pd.read_csv(DATA_IN)
    print(f"Total registros cargados: {len(df)}")
    return df


def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    2. Limpieza de datos:
       - Eliminar registros duplicados considerando el campo email.
       - Descartar registros con email vacío.
       - Normalizar los valores de estatus a: NUEVO, CONTACTADO, EN_SEGUIMIENTO, CONVERTIDO, PERDIDO.
       - Rellenar valores nulos en la columna presupuesto con 0 o el valor promedio.
    """
    df_limpio = df.copy()

    # Normaliza email (quita espacios, pasa a minúsculas) para detectar
    # duplicados/vacíos de forma consistente antes de decidir qué conservar
    df_limpio["email"] = df_limpio["email"].astype(str).str.strip()

    # Descarta registros con email vacío, nulo o literal "nan"
    df_limpio = df_limpio[
        df_limpio["email"].notna()
        & (df_limpio["email"] != "")
        & (df_limpio["email"].str.lower() != "nan")
    ]

    # Elimina duplicados por email, conservando la primera aparición
    df_limpio = df_limpio.drop_duplicates(subset="email", keep="first")

    # Normaliza estatus: mayúsculas, sin espacios extra, y mapeo a valor canónico
    df_limpio["estatus"] = (
        df_limpio["estatus"]
        .astype(str)
        .str.strip()
        .str.upper()
        .map(ESTATUS_CANONICOS)
        .fillna("NUEVO")  # cualquier valor no reconocido se trata como NUEVO
    )

    # Rellena presupuesto nulo con el promedio de los presupuestos válidos
    df_limpio["presupuesto"] = pd.to_numeric(df_limpio["presupuesto"], errors="coerce")
    presupuesto_promedio = df_limpio["presupuesto"].mean()
    df_limpio["presupuesto"] = df_limpio["presupuesto"].fillna(round(presupuesto_promedio, 2))

    df_limpio = df_limpio.reset_index(drop=True)
    return df_limpio


def generar_resumen(df: pd.DataFrame):
    """
    3. Imprimir métricas en consola:
       - Total de prospectos limpios.
       - Cantidad de prospectos por origen.
       - Cantidad de prospectos por estatus normalizado.
    """
    print("\n--- RESUMEN DE LEADS ---")
    print(f"Total de prospectos limpios: {len(df)}")

    print("\nProspectos por origen:")
    print(df["origen"].value_counts().to_string())

    print("\nProspectos por estatus:")
    print(df["estatus"].value_counts().to_string())


def exportar_datos(df: pd.DataFrame):
    """4. Guardar dataset limpio listo para base de datos."""
    df.to_csv(DATA_OUT, index=False)
    print(f"\nDataset limpio guardado en: {DATA_OUT}")


def enviar_muestra_api(df: pd.DataFrame, limite: int = 5):
    """
    5. Consumo de API:
       - Tomar una muestra de los primeros `limite` prospectos.
       - Enviar una petición POST a la API (http://127.0.0.1:8000/api/leads)
         utilizando el encabezado 'Authorization: Bearer atlas-token-2026'.
    """
    muestra = df.head(limite)
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    print(f"\n--- ENVIANDO MUESTRA DE {len(muestra)} LEADS A LA API ---")

    for _, row in muestra.iterrows():
        payload = {
            "id": int(row["id"]),
            "nombre": row["nombre"],
            "email": row["email"],
            "telefono": str(row["telefono"]),
            "origen": row["origen"],
            "fecha_registro": str(row["fecha_registro"]),
            "estatus": row["estatus"],
            "presupuesto": float(row["presupuesto"]) if pd.notna(row["presupuesto"]) else None,
            "desarrollo_id": int(row["desarrollo_id"]),
            "comentarios": row.get("comentarios") if pd.notna(row.get("comentarios")) else None,
        }

        try:
            response = requests.post(API_URL, json=payload, headers=headers, timeout=5)

            if response.status_code == 200 or response.status_code == 201:
                print(f"Lead {payload['id']} sincronizado correctamente.")
            elif response.status_code == 401:
                # Token vencido/inválido: no reintentar con el mismo token.
                # En producción, esto se resolvería refrescando el token
                # (p. ej. vía OAuth2 refresh_token) o notificando para
                # regenerar credenciales, y solo entonces reintentar la petición.
                print(f"Lead {payload['id']}: 401 Unauthorized -> {response.json().get('detail')}")
            elif response.status_code == 429:
                # Rate limit alcanzado: en producción se implementaría backoff
                # exponencial (esperar y reintentar con tiempos crecientes) o
                # respetar un header Retry-After si la API lo expone, en vez
                # de seguir disparando peticiones.
                print(f"Lead {payload['id']}: 429 Too Many Requests -> {response.json().get('detail')}")
            else:
                print(f"Lead {payload['id']}: respuesta inesperada ({response.status_code}) -> {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"Lead {payload['id']}: error de conexión -> {e}")


if __name__ == "__main__":
    df = cargar_datos()
    df_limpio = limpiar_datos(df)
    generar_resumen(df_limpio)
    exportar_datos(df_limpio)
    enviar_muestra_api(df_limpio)