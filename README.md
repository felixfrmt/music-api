# Music API — Flask + PostgreSQL

## Structure du projet

```
music_api/
├── app/
│   ├── __init__.py          # Application factory (create_app)
│   ├── extensions.py        # Instance SQLAlchemy partagée
│   ├── models/
│   │   ├── __init__.py
│   │   ├── artist.py
│   │   ├── album.py
│   │   └── track.py
│   └── routes/
│       ├── __init__.py      # Enregistrement des blueprints
│       ├── artists.py
│       ├── albums.py
│       └── tracks.py
├── run.py                   # Point d'entrée
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

---

## Lancer avec Docker (recommandé)

```bash
# 1. Copier et configurer les variables d'environnement
cp .env.example .env

# 2. Démarrer l'API + la base de données
docker compose up --build

# L'API est disponible sur http://localhost:5000
```

Pour arrêter :
```bash
docker compose down           # conserve les données
docker compose down -v        # supprime aussi le volume postgres
```

---

## Lancer en local (sans Docker)

```bash
pip install -r requirements.txt

export DATABASE_URL=postgresql://user:password@localhost:5432/music_db

python run.py
# Les tables sont créées automatiquement au démarrage
```

---

## Schéma

```
artist      ──< album        (un artiste → plusieurs albums)
artist      ──< track        (owner_id : un artiste est propriétaire de la track)
album       ──< track        (un album → plusieurs tracks, album_id nullable = standalone)
track >──── track_artists ────< artist   (artistes en featuring, many-to-many)
```

---

## Routes

### Artists

| Méthode | Route | Description |
|--------|-------|-------------|
| POST | `/artists` | Créer un artiste |
| GET  | `/artists` | Lister tous les artistes |
| GET  | `/artists/<id>` | Détail artiste + albums + tracks |

```json
POST /artists
{ "name": "Daft Punk", "bio": "Duo français de musique électronique." }
```

### Albums

| Méthode | Route | Description |
|--------|-------|-------------|
| POST | `/albums` | Créer un album |
| GET  | `/albums` | Lister tous les albums |
| GET  | `/albums/<id>` | Détail album + tracks |

```json
POST /albums
{
  "title": "Random Access Memories",
  "artist_id": 1,
  "release_date": "2013-05-17",
  "cover_url": "https://example.com/cover.jpg"
}
```

### Tracks

| Méthode | Route | Description |
|--------|-------|-------------|
| POST | `/tracks` | Créer une musique |
| GET  | `/tracks` | Lister toutes les musiques |
| GET  | `/tracks/<id>` | Détail d'une musique |

```json
// Track dans un album avec featuring
POST /tracks
{
  "title": "Get Lucky",
  "owner_id": 1,
  "album_id": 1,
  "duration_seconds": 248,
  "featured_artist_ids": [2, 3]
}

// Track standalone (sans album)
POST /tracks
{ "title": "Da Funk", "owner_id": 1, "duration_seconds": 320 }
```