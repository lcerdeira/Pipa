# Contributing

## Development Setup

1. Fork and clone the repository
2. Install backend: `cd back-end && pip install -r requirements.txt`
3. Install frontend: `cd UI/DesktopPIPA && yarn install`
4. Run backend: `flask run --host 0.0.0.0 --port 5000`
5. Run frontend: `npx quasar dev`

## Running Tests

```bash
cd back-end
pip install pytest
python -m pytest tests/ -v
```

## Project Structure

```
Pipa/
  back-end/
    app.py                  # Flask entry point
    blueprints/
      api.py                # REST API endpoints
      view.py               # Legacy HTML routes
    extensions/
      services.py           # Pipeline orchestrator
      services1/            # Individual service modules
        Service_Trimage.py  # Trimming
        Service_Assembly.py # Assembly
        Service_Predict.py  # Annotation tools
        Service_Report.py   # Report generation
    tests/                  # API tests
  UI/DesktopPIPA/
    src/
      components/tabs/      # Vue components (About, Software, Results)
      store/pipa/           # Vuex state management
      boot/axios.js         # HTTP client setup
    src-electron/           # Electron main process
  docs/                     # This documentation
  environment.yml           # Conda environment
  Dockerfile               # Container build
  docker-compose.yml       # Container orchestration
```

## Adding a New Annotation Tool

1. Add the tool command to `Service_Predict.py` with a `self._should_run("toolkey")` guard
2. Add the tool key to `ALL_TOOLS` list in `PredictService`
3. Add a card for it in `Software.vue` `defaultAnnotationTools` array
4. Add the tool to `environment.yml` (Bioconda package name)
5. Document it in `docs/user-guide/tools.md`
