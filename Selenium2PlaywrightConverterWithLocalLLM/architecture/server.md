# Server SOP

## Endpoints

### `POST /api/convert`
- **Input**: `{ sourceCode: string, options: { usePageObjectModel: boolean } }`
- **Output**: `{ files: [{ fileName, fileType, content }], logs: [] }`

## Running
- `node server/index.js`
- Port: 3001
