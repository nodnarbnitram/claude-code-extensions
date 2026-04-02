# Grafana Plugin Troubleshooting Guide

Common issues and solutions for Grafana plugin development (v12.x+).

## Plugin Not Appearing

### Symptoms
- Plugin doesn't show in Grafana's plugin list
- "Plugin not found" errors

### Solutions

1. **Check plugin.json**
   ```bash
   # Verify plugin.json is valid JSON
   cat dist/plugin.json | jq .

   # Check required fields
   jq '.id, .type, .name' dist/plugin.json
   ```

2. **Verify dist folder structure**
   ```bash
   ls -la dist/
   # Should contain:
   # - plugin.json
   # - module.js
   # - img/ folder (optional)
   ```

3. **Check unsigned plugin setting**
   ```ini
   # grafana.ini or GF_PLUGINS_ALLOW_LOADING_UNSIGNED_PLUGINS env var
   [plugins]
   allow_loading_unsigned_plugins = your-plugin-id
   ```

4. **Restart Grafana**
   ```bash
   docker compose restart grafana
   # or
   systemctl restart grafana-server
   ```

5. **Check Grafana logs**
   ```bash
   docker compose logs grafana | grep -i plugin
   ```

## Build Errors

### TypeScript Errors

```bash
# Check TypeScript version compatibility
npm ls typescript

# Update @grafana packages to matching versions
npm update @grafana/data @grafana/ui @grafana/runtime
```

### Webpack Errors

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear build cache
rm -rf dist .cache
npm run build
```

### Go Backend Build Errors

```bash
# Update Go SDK
go get -u github.com/grafana/grafana-plugin-sdk-go
go mod tidy

# Check Go version (1.21+ required)
go version

# Build with verbose output
mage -v build:linux
```

## Backend Plugin Not Working

### Symptoms
- "Plugin failed to load" in Grafana
- Backend health check fails
- No data returned from queries

### Solutions

1. **Check binary exists**
   ```bash
   ls -la dist/gpx_*
   # Should have executable binaries for target platforms
   ```

2. **Verify plugin.json backend settings**
   ```json
   {
     "backend": true,
     "executable": "gpx_yourplugin"
   }
   ```

3. **Check binary permissions**
   ```bash
   chmod +x dist/gpx_*
   ```

4. **Check Grafana logs for backend errors**
   ```bash
   docker compose logs grafana 2>&1 | grep -i "yourplugin"
   ```

5. **Test health check manually**
   ```bash
   curl -X POST http://admin:admin@localhost:3000/api/ds/query \
     -H "Content-Type: application/json" \
     -d '{"queries":[{"datasource":{"type":"your-datasource","uid":"xxx"}}]}'
   ```

## Data Source Connection Issues

### Authentication Errors

1. **Check secureJsonData storage**
   - API keys should use `secureJsonData`, not `jsonData`
   - Verify onReset handler clears the field

2. **CORS issues**
   ```json
   // In plugin.json routes
   {
     "routes": [{
       "path": "api",
       "url": "https://api.example.com",
       "headers": [
         {"name": "Authorization", "content": "Bearer {{.SecureJsonData.apiKey}}"}
       ]
     }]
   }
   ```

3. **Backend proxy not configured**
   - For frontend data sources, use `getBackendSrv().fetch()`
   - Configure routes in plugin.json for proxy

### No Data Returned

1. **Check time range handling**
   ```typescript
   // Ensure time range is passed to API
   const from = options.range.from.valueOf();
   const to = options.range.to.valueOf();
   ```

2. **Verify data frame format**
   ```typescript
   // Time field must be first or explicitly typed
   const frame = new MutableDataFrame({
     fields: [
       { name: 'Time', type: FieldType.time, values: [...] },
       { name: 'Value', type: FieldType.number, values: [...] },
     ],
   });
   ```

3. **Check console for errors**
   - Open browser DevTools → Console
   - Look for network errors in Network tab

## Docker Development Issues

### Volume Mount Problems

```bash
# Verify mount is correct
docker compose exec grafana ls -la /var/lib/grafana/plugins/

# Check compose file volume syntax
volumes:
  - ./dist:/var/lib/grafana/plugins/your-plugin-id
```

### Container Won't Start

```bash
# Check for port conflicts
lsof -i :3000

# Remove orphan containers
docker compose down --remove-orphans
docker compose up -d
```

### Changes Not Reflecting

```bash
# Ensure dev mode is running
npm run dev

# Hard refresh browser
# Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows/Linux)

# Restart Grafana to reload plugin
docker compose restart grafana
```

## Panel Plugin Issues

### Panel Shows "No Data"

1. **Check data link in panel settings**
   - Ensure data source is selected
   - Run a test query

2. **Handle empty data gracefully**
   ```typescript
   if (!data.series || data.series.length === 0) {
     return <div>No data available</div>;
   }
   ```

### Options Not Saving

1. **Check option path names**
   - Paths must match TypeScript interface
   - Use dot notation for nested: `nested.option`

2. **Verify default values**
   ```typescript
   .addTextInput({
     path: 'text',
     defaultValue: 'default', // Must be valid for the type
   })
   ```

### Visualization Not Updating

1. **Check React dependencies**
   ```typescript
   // Use useEffect with proper dependencies
   useEffect(() => {
     // Update visualization
   }, [data, options, width, height]);
   ```

2. **Avoid mutating props**
   - Create new objects when transforming data
   - Use spread operators or Object.assign

## Signing and Publishing

### Signing Errors

```bash
# Check plugin ID format
# Must be: <org>-<name>-<type>
# Example: myorg-mypanel-panel

# Verify Grafana Cloud credentials
export GRAFANA_ACCESS_POLICY_TOKEN=your-token
npx @grafana/sign-plugin@latest
```

### Catalog Submission Issues

1. **Ensure all required files exist**
   - README.md
   - LICENSE
   - CHANGELOG.md
   - Screenshots in img/

2. **Validate plugin.json**
   - All info fields populated
   - Valid semver version
   - Correct grafanaDependency

## Performance Issues

### Slow Panel Rendering

1. **Memoize expensive calculations**
   ```typescript
   const processedData = useMemo(() => {
     return transformData(data);
   }, [data]);
   ```

2. **Use virtualization for large datasets**
   - Consider react-window or react-virtualized

3. **Debounce option changes**
   ```typescript
   const debouncedOnChange = useDebouncedCallback(onChange, 300);
   ```

### Memory Leaks

1. **Clean up subscriptions**
   ```typescript
   useEffect(() => {
     const subscription = observable.subscribe();
     return () => subscription.unsubscribe();
   }, []);
   ```

2. **Cancel pending requests**
   ```typescript
   useEffect(() => {
     const controller = new AbortController();
     fetch(url, { signal: controller.signal });
     return () => controller.abort();
   }, [url]);
   ```

## Getting Help

1. **Check official documentation**: https://grafana.com/developers/plugin-tools/
2. **Grafana Community Forums**: https://community.grafana.com/
3. **GitHub Issues**: https://github.com/grafana/plugin-tools/issues
4. **Ask the grafana-plugin-expert agent** for SDK-specific guidance
