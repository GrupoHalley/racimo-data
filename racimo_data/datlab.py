import requests
import pandas as pd
import io
from datetime import datetime

# URL de búsqueda en Dataverse (RedCLARA)
SEARCH_URL = "https://dataverse.redclara.net/api/search?q=datos_consolidados*&type=file"


def ultimo_dataset() -> pd.DataFrame:
    """
    Descarga y retorna el dataset más reciente de DatLab (RedCLARA)
    correspondiente a 'datos_consolidados*' del proyecto RACIMO Orquídeas.

    Returns
    -------
    pandas.DataFrame
        DataFrame con los datos consolidados más recientes.

    Raises
    ------
    RuntimeError
        Si no se puede consultar la API, no hay archivos disponibles
        o falla la descarga/procesamiento del CSV.
    """

    # 1. Consultar API de búsqueda
    try:
        response = requests.get(SEARCH_URL, timeout=20)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        raise RuntimeError(
            "No se pudo consultar la API de DatLab (RedCLARA)."
        ) from e

    items = data.get("data", {}).get("items", [])

    if not items:
        raise RuntimeError(
            "No se encontraron archivos con el patrón 'datos_consolidados*'."
        )

    # 2. Encontrar el archivo más reciente
    latest_file = None
    latest_date = datetime.min

    for item in items:
        pub_date_str = item.get("published_at")

        if not pub_date_str:
            continue

        try:
            pub_date = datetime.strptime(
                pub_date_str, "%Y-%m-%dT%H:%M:%SZ"
            )
        except ValueError:
            continue

        if pub_date > latest_date:
            latest_date = pub_date
            latest_file = item

    if not latest_file:
        raise RuntimeError(
            "No se pudo determinar el archivo más reciente."
        )

    # 3. Descargar el archivo CSV
    base_url = latest_file["url"]
    download_url = f"{base_url}?format=original"

    try:
        file_response = requests.get(download_url, timeout=30)
        file_response.raise_for_status()
        df = pd.read_csv(io.StringIO(file_response.text))
    except Exception as e:
        raise RuntimeError(
            "Error al descargar o procesar el dataset CSV."
        ) from e

    return df
