# Grafana Plugin E2E Testing Guide

End-to-end testing for Grafana plugins using `@grafana/plugin-e2e` and Playwright.

## Overview

The `@grafana/plugin-e2e` package provides:
- Playwright-based testing framework
- Pre-built fixtures for Grafana UI (panels, data sources, dashboards)
- Version-aware selectors (work across Grafana versions)
- Authentication handling
- CI/CD workflow templates

## Setup

### Install Dependencies

```bash
# Install Playwright and plugin-e2e
npm install -D @grafana/plugin-e2e @playwright/test

# Install Playwright browsers
npx playwright install --with-deps chromium
```

### Playwright Configuration

Create `playwright.config.ts`:

```typescript
import { dirname } from 'path';
import { defineConfig, devices } from '@playwright/test';
import type { PluginOptions } from '@grafana/plugin-e2e';

const pluginE2eAuth = `${dirname(require.resolve('@grafana/plugin-e2e'))}/auth`;

export default defineConfig<PluginOptions>({
  testDir: './tests',
  reporter: 'html',
  use: {
    baseURL: process.env.GRAFANA_URL || 'http://localhost:3000',
  },
  projects: [
    // Authentication setup (runs first)
    {
      name: 'auth',
      testDir: pluginE2eAuth,
      testMatch: [/.*\.js/],
    },
    // Main tests (depends on auth)
    {
      name: 'run-tests',
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'playwright/.auth/admin.json',
      },
      dependencies: ['auth'],
    },
  ],
});
```

### Directory Structure

```
my-plugin/
├── tests/
│   ├── panel.spec.ts        # Panel plugin tests
│   ├── datasource.spec.ts   # Data source tests
│   └── fixtures.ts          # Custom fixtures
├── provisioning/
│   ├── datasources/
│   │   └── datasources.yml  # Test data sources
│   └── dashboards/
│       └── dashboard.json   # Test dashboards
├── playwright.config.ts
└── package.json
```

## Available Fixtures

### Page Fixtures

| Fixture | Description |
|---------|-------------|
| `panelEditPage` | Edit a new panel in a dashboard |
| `dashboardPage` | Navigate dashboards |
| `explorePage` | Grafana Explore view |
| `variableEditPage` | Dashboard variable editor |
| `annotationEditPage` | Annotation editor |

### Data Source Fixtures

| Fixture | Description |
|---------|-------------|
| `createDataSourceConfigPage` | Create new data source config |
| `readProvisionedDataSource` | Read provisioned data source |

### App Plugin Fixtures

| Fixture | Description |
|---------|-------------|
| `gotoAppPage` | Navigate to app page |
| `appConfigPage` | App configuration page |

### Utility Fixtures

| Fixture | Description |
|---------|-------------|
| `selectors` | Version-aware Grafana selectors |
| `readProvisionedDashboard` | Read provisioned dashboard |
| `gotoDashboardPage` | Navigate to dashboard |
| `gotoPanelEditPage` | Navigate to panel edit |

## Test Patterns

### Panel Plugin Tests

```typescript
import { test, expect } from '@grafana/plugin-e2e';

test('panel should render data correctly', async ({ panelEditPage }) => {
  // Set data source
  await panelEditPage.datasource.set('gdev-testdata');

  // Set visualization type
  await panelEditPage.setVisualization('Table');

  // Refresh and assert
  await expect(panelEditPage.refreshPanel()).toBeOK();
  await expect(panelEditPage.panel.data).toContainText(['value1', 'value2']);
});

test('panel should handle no data', async ({ panelEditPage, page }) => {
  await panelEditPage.datasource.set('gdev-testdata');
  await panelEditPage.setVisualization('Table');

  // Select "No Data" scenario
  await page.getByLabel('Scenario').last().click();
  await page.getByText('No Data Points').click();

  await panelEditPage.refreshPanel();
  await expect(panelEditPage.panel.locator).toContainText('No data');
});
```

### Data Source Plugin Tests

**Configuration Editor:**

```typescript
import { test, expect } from '@grafana/plugin-e2e';

test('save & test should succeed with valid config', async ({
  createDataSourceConfigPage,
  readProvisionedDataSource,
  page,
}) => {
  const ds = await readProvisionedDataSource({ fileName: 'datasources.yml' });
  const configPage = await createDataSourceConfigPage({ type: ds.type });

  // Fill configuration
  await page.getByLabel('URL').fill('https://api.example.com');
  await page.getByLabel('API Key').fill('test-api-key');

  // Save and test
  await expect(configPage.saveAndTest()).toBeOK();
  await expect(configPage).toHaveAlert('success');
});

test('save & test should fail with invalid config', async ({
  createDataSourceConfigPage,
  page,
}) => {
  const configPage = await createDataSourceConfigPage({ type: 'my-datasource' });

  // Leave required fields empty
  await expect(configPage.saveAndTest()).not.toBeOK();
  await expect(configPage).toHaveAlert('error');
});
```

**Query Editor:**

```typescript
import { test, expect } from '@grafana/plugin-e2e';

test('query editor should render', async ({ panelEditPage, readProvisionedDataSource }) => {
  const ds = await readProvisionedDataSource({ fileName: 'datasources.yml' });
  await panelEditPage.datasource.set(ds.name);

  await expect(
    panelEditPage.getQueryEditorRow('A').getByRole('textbox', { name: 'Query' })
  ).toBeVisible();
});

test('query should return expected data', async ({ panelEditPage, readProvisionedDataSource }) => {
  const ds = await readProvisionedDataSource({ fileName: 'datasources.yml' });
  await panelEditPage.datasource.set(ds.name);
  await panelEditPage.setVisualization('Table');

  await expect(panelEditPage.refreshPanel()).toBeOK();
  await expect(panelEditPage.panel.fieldNames).toContainText(['time', 'value']);
  await expect(panelEditPage.panel.data).toContainText(['10', '20']);
});
```

### App Plugin Tests

**Custom Fixtures:**

```typescript
// tests/fixtures.ts
import { AppPage, test as base } from '@grafana/plugin-e2e';
import pluginJson from '../src/plugin.json';

type AppTestFixture = {
  gotoPage: (path?: string) => Promise<AppPage>;
};

export const test = base.extend<AppTestFixture>({
  gotoPage: async ({ gotoAppPage }, use) => {
    await use((path) =>
      gotoAppPage({
        path,
        pluginId: pluginJson.id,
      })
    );
  },
});

export { expect } from '@grafana/plugin-e2e';
```

**App Page Tests:**

```typescript
import { test, expect } from './fixtures';

test('home page should render', async ({ gotoPage }) => {
  const appPage = await gotoPage('/');
  await expect(appPage.getByRole('heading', { name: 'Welcome' })).toBeVisible();
});

test('config should save successfully', async ({ appConfigPage, page }) => {
  await page.getByRole('textbox', { name: 'API Key' }).fill('secret-key');
  await page.getByRole('textbox', { name: 'API URL' }).fill('https://api.example.com');

  const saveResponse = appConfigPage.waitForSettingsResponse();
  await page.getByRole('button', { name: /Save & test/i }).click();

  await expect(saveResponse).toBeOK();
});
```

## Provisioning Test Resources

### Data Sources (`provisioning/datasources/datasources.yml`)

```yaml
apiVersion: 1

datasources:
  - name: Test Data Source
    type: myorg-mydatasource-datasource
    access: proxy
    isDefault: true
    jsonData:
      path: /api/v1
    secureJsonData:
      apiKey: test-api-key
```

### Dashboards (`provisioning/dashboards/dashboard.json`)

```json
{
  "annotations": { "list": [] },
  "editable": true,
  "panels": [
    {
      "id": 1,
      "type": "myorg-mypanel-panel",
      "title": "Test Panel",
      "datasource": { "type": "myorg-mydatasource-datasource" },
      "gridPos": { "h": 8, "w": 12, "x": 0, "y": 0 }
    }
  ],
  "title": "E2E Test Dashboard",
  "uid": "e2e-test-dashboard"
}
```

### Using Provisioned Resources

```typescript
test('provisioned dashboard panel should work', async ({
  readProvisionedDashboard,
  gotoPanelEditPage,
}) => {
  const dashboard = await readProvisionedDashboard({ fileName: 'dashboard.json' });
  const panelEditPage = await gotoPanelEditPage({ dashboard, id: '1' });

  await expect(panelEditPage.refreshPanel()).toBeOK();
});
```

## Running Tests

```bash
# Run all tests
npx playwright test

# Run with UI mode (debugging)
npx playwright test --ui

# Run specific test file
npx playwright test tests/panel.spec.ts

# Run with specific Grafana version
GRAFANA_VERSION=12.0.0 docker compose up -d
npx playwright test
```

## CI/CD with GitHub Actions

```yaml
name: E2E Tests

on:
  pull_request:
  schedule:
    - cron: '0 11 * * *'  # Daily at 11 UTC

permissions:
  contents: read
  id-token: write

jobs:
  resolve-versions:
    name: Resolve Grafana images
    runs-on: ubuntu-latest
    timeout-minutes: 3
    outputs:
      matrix: ${{ steps.resolve-versions.outputs.matrix }}
    steps:
      - uses: actions/checkout@v4
      - name: Resolve Grafana E2E versions
        id: resolve-versions
        uses: grafana/plugin-actions/e2e-version@main

  playwright-tests:
    needs: resolve-versions
    timeout-minutes: 60
    strategy:
      fail-fast: false
      matrix:
        GRAFANA_IMAGE: ${{ fromJson(needs.resolve-versions.outputs.matrix) }}
    name: e2e ${{ matrix.GRAFANA_IMAGE.name }}@${{ matrix.GRAFANA_IMAGE.VERSION }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version-file: .nvmrc

      - name: Install dependencies
        run: npm ci

      - name: Build plugin
        run: npm run build

      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium

      - name: Start Grafana
        run: |
          docker compose pull
          GRAFANA_VERSION=${{ matrix.GRAFANA_IMAGE.VERSION }} \
          GRAFANA_IMAGE=${{ matrix.GRAFANA_IMAGE.NAME }} \
          docker compose up -d

      - name: Wait for Grafana
        uses: grafana/plugin-actions/wait-for-grafana@main

      - name: Run Playwright tests
        run: npx playwright test

      - name: Upload report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report-${{ matrix.GRAFANA_IMAGE.VERSION }}
          path: playwright-report/
          retention-days: 7
```

## Common Assertions

```typescript
// Response status
await expect(panelEditPage.refreshPanel()).toBeOK();
await expect(configPage.saveAndTest()).not.toBeOK();

// Alert presence
await expect(configPage).toHaveAlert('success');
await expect(configPage).toHaveAlert('error');

// Panel data
await expect(panelEditPage.panel.data).toContainText(['value1', 'value2']);
await expect(panelEditPage.panel.fieldNames).toContainText(['time', 'value']);

// Element visibility
await expect(page.getByRole('button', { name: 'Save' })).toBeVisible();
await expect(page.getByLabel('Query')).toBeEditable();
```

## Best Practices

1. **Use provisioned resources** - Avoid manual setup in tests
2. **Test across Grafana versions** - Use version matrix in CI
3. **Use version-aware selectors** - The `selectors` fixture handles version differences
4. **Mock external APIs** - Use Playwright's `page.route()` for reliability
5. **Keep tests focused** - One assertion per test when possible
6. **Use custom fixtures** - Reduce boilerplate with reusable fixtures

## Resources

- **Official docs**: https://grafana.com/developers/plugin-tools/e2e-test-a-plugin
- **Package**: https://www.npmjs.com/package/@grafana/plugin-e2e
- **Examples**: https://github.com/grafana/grafana-plugin-examples
