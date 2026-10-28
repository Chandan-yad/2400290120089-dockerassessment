# FEST - Docker Container Assessment

## Stage 4: Versioning and Publishing

### Docker Hub Image

- Docker Hub Repository: `chandanyadav15/fest-backend`
- Version Tag: `1.0.0`
- Additional Tag: `1.0`
- Image Size: `98.6MB`

### Image Digest

```text
sha256:b18fc25e6c6b469584d74a1bb176ad0bb1676c129b536a6bb35c0831f83a15a1
```

### Registry Deployment

Backend image was published to Docker Hub and deployed using:

```bash
docker compose pull backend
docker compose up -d
```

### Verification

The backend health endpoint was checked:

```bash
curl http://localhost:169/api/health
```

Verified response:

```json
{
  "database": true,
  "regno": "2400290120089",
  "status": "healthy",
  "version": "1.0.0"
}
```

The frontend was successfully opened at `http://localhost:8080`.

The local backend image tags `fest-backend:0.1` through `fest-backend:0.5` were removed after publishing.