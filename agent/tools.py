"""

"""
import os
import httpx

MUSICBRAINZ_URL = "https://musicbrainz.org/ws/2"

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY", "")

HEADER = f"MusicAgent/1.0 ({os.getenv('EMAIL_HEADER', '')})"

HEADERS = {
    "User-Agent": HEADER
}


async def search_artist(name: str) -> dict:
    """
    Busca un artista en MusicBrainz.
    Retorna info básica + MBID (el ID único del artista).
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{MUSICBRAINZ_URL}/artist",
            params={
                "query": name,
                "limit": 1,
                "fmt": "json"
            },
            headers=HEADERS
        )
        response.raise_for_status()
        data = response.json()

    artists = data.get("artists", [])
    if not artists:
        return {"error": f"No se encontró el artista: {name}"}

    artist = artists[0]
    return {
        "name": artist.get("name"),
        "mbid": artist.get("id"),
        "country": artist.get("country"),
        "disambiguation": artist.get("disambiguation", ""),
    }