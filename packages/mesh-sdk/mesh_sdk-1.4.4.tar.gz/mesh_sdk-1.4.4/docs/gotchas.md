# Mesh SDK Gotchas and Edge Cases

## Package Naming

- The SDK is published on PyPI as `mesh-sdk` (not `mesh`)
- All imports still use `import mesh` despite the package being named `mesh-sdk`
- Installation is done via `pip install mesh-sdk`

## Authentication

- The backend validation endpoint `/auth/validate` may return 404 on some server configurations
- The SDK automatically falls back to local validation when backend validation fails
- Direct token authentication via `auth_token` property is deprecated and will be removed in a future version

## Network Issues

- All API requests include a configurable timeout parameter (default: 60 seconds)
- When backend validation endpoints are unavailable, local validation is used as a fallback
- If authentication server is unreachable during initial login, the browser-based flow may hang

## Installation Issues

- Post-install authentication may fail in CI/CD environments
- The `mesh-auth` command-line tool can be used to authenticate manually when needed
- Python environments with strict external management settings may require using `--break-system-packages` or virtual environments

## Import Concerns

- Top-level functions (e.g., `mesh.chat()`) will automatically trigger authentication when needed
- The module structure maintains backward compatibility despite the package name change
- Environment variables are still used the same way regardless of package name
