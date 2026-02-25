""" """

import os
import httpx

MUSICBRAINZ_URL = "https://musicbrainz.org/ws/2"

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY", "")

HEADER = f"MusicAgent/1.0 ({os.getenv('EMAIL_HEADER', '')})"

HEADERS = {"User-Agent": HEADER}


async def search_artist(name: str) -> dict:
    """
    Busca un artista en MusicBrainz.
    Retorna info básica + MBID (el ID único del artista).
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{MUSICBRAINZ_URL}/artist",
            params={"query": name, "limit": 1, "fmt": "json"},
            headers=HEADERS,
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


async def get_discography(artist_name: str) -> dict:
    """
    Retorna los álbumes de un artista ordenados por ano de lanzamiento.
    Primero obtiene el MBID via search_artist()
    """
    # Primero necsitamos el MBID del artista
    artist = await search_artist(artist_name)
    if "error" in artist:
        return artist  # Retorna el error si no se encontró el artista

    mbid = artist["mbid"]

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{MUSICBRAINZ_URL}/release-group",
            params={"artist": mbid, "type": "album", "limit": 20, "fmt": "json"},
            headers=HEADERS,
        )
        response.raise_for_status()
        data = response.json()

    EXCLUDED_TYPES = {"Live", "Compilation", "Soundtrack", "Demo", "DJ-mix", "Mixtape"}

    albums = [
        {
            "title": album.get("title"),
            "year": album.get("first-release-date", "")[:4],
        }
        for album in data.get("release-groups", [])
        if not any(t in EXCLUDED_TYPES for t in album.get("secondary-types", []))
    ]

    # Ordenar por año
    albums.sort(key=lambda x: x["year"])

    return {"artist": artist["name"], "albums": albums}

