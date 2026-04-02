# Grafana Plugin SDK Patterns (v12.x+)

Common patterns for Grafana plugin development using the official SDKs.

## Frontend SDK Patterns

### Panel Plugin Component

```typescript
import React from 'react';
import { PanelProps } from '@grafana/data';
import { useTheme2 } from '@grafana/ui';
import { SimpleOptions } from './types';

interface Props extends PanelProps<SimpleOptions> {}

export const SimplePanel: React.FC<Props> = ({ options, data, width, height, fieldConfig, replaceVariables }) => {
  const theme = useTheme2();

  // Access data frames
  const frame = data.series[0];
  if (!frame) {
    return <div>No data</div>;
  }

  // Access field values
  const timeField = frame.fields.find(f => f.type === 'time');
  const valueField = frame.fields.find(f => f.type === 'number');

  return (
    <div style={{ width, height, padding: theme.spacing(1) }}>
      {/* Your visualization */}
    </div>
  );
};
```

### Panel Options Configuration

```typescript
import { PanelPlugin } from '@grafana/data';
import { SimplePanel } from './SimplePanel';
import { SimpleOptions } from './types';

export const plugin = new PanelPlugin<SimpleOptions>(SimplePanel)
  .setPanelOptions(builder => {
    builder
      .addTextInput({
        path: 'text',
        name: 'Display text',
        description: 'Text to display',
        defaultValue: 'Hello',
      })
      .addBooleanSwitch({
        path: 'showLabels',
        name: 'Show labels',
        defaultValue: true,
      })
      .addSelect({
        path: 'displayMode',
        name: 'Display mode',
        defaultValue: 'default',
        settings: {
          options: [
            { value: 'default', label: 'Default' },
            { value: 'compact', label: 'Compact' },
            { value: 'expanded', label: 'Expanded' },
          ],
        },
      })
      .addColorPicker({
        path: 'color',
        name: 'Color',
        defaultValue: 'green',
      });
  });
```

### Data Source Class

```typescript
import {
  DataSourceApi,
  DataSourceInstanceSettings,
  DataQueryRequest,
  DataQueryResponse,
  MutableDataFrame,
  FieldType,
} from '@grafana/data';
import { getBackendSrv } from '@grafana/runtime';
import { MyQuery, MyDataSourceOptions } from './types';

export class DataSource extends DataSourceApi<MyQuery, MyDataSourceOptions> {
  baseUrl: string;

  constructor(instanceSettings: DataSourceInstanceSettings<MyDataSourceOptions>) {
    super(instanceSettings);
    this.baseUrl = instanceSettings.url || '';
  }

  async query(options: DataQueryRequest<MyQuery>): Promise<DataQueryResponse> {
    const { range } = options;
    const from = range!.from.valueOf();
    const to = range!.to.valueOf();

    const promises = options.targets.map(async target => {
      const response = await getBackendSrv().fetch({
        url: `${this.baseUrl}/api/data`,
        method: 'POST',
        data: {
          query: target.queryText,
          from,
          to,
        },
      }).toPromise();

      return new MutableDataFrame({
        refId: target.refId,
        fields: [
          { name: 'Time', type: FieldType.time, values: response.data.times },
          { name: 'Value', type: FieldType.number, values: response.data.values },
        ],
      });
    });

    return { data: await Promise.all(promises) };
  }

  async testDatasource(): Promise<{ status: string; message: string }> {
    try {
      await getBackendSrv().fetch({
        url: `${this.baseUrl}/api/health`,
        method: 'GET',
      }).toPromise();

      return { status: 'success', message: 'Data source is working' };
    } catch (error) {
      return { status: 'error', message: `Connection failed: ${error}` };
    }
  }
}
```

### Config Editor

```typescript
import React, { ChangeEvent } from 'react';
import { InlineField, Input, SecretInput } from '@grafana/ui';
import { DataSourcePluginOptionsEditorProps } from '@grafana/data';
import { MyDataSourceOptions, MySecureJsonData } from './types';

interface Props extends DataSourcePluginOptionsEditorProps<MyDataSourceOptions, MySecureJsonData> {}

export const ConfigEditor: React.FC<Props> = ({ options, onOptionsChange }) => {
  const { jsonData, secureJsonFields, secureJsonData } = options;

  const onPathChange = (event: ChangeEvent<HTMLInputElement>) => {
    onOptionsChange({
      ...options,
      jsonData: { ...jsonData, path: event.target.value },
    });
  };

  const onAPIKeyChange = (event: ChangeEvent<HTMLInputElement>) => {
    onOptionsChange({
      ...options,
      secureJsonData: { ...secureJsonData, apiKey: event.target.value },
    });
  };

  const onResetAPIKey = () => {
    onOptionsChange({
      ...options,
      secureJsonFields: { ...secureJsonFields, apiKey: false },
      secureJsonData: { ...secureJsonData, apiKey: '' },
    });
  };

  return (
    <>
      <InlineField label="Path" labelWidth={12}>
        <Input
          value={jsonData.path || ''}
          placeholder="/api/v1"
          width={40}
          onChange={onPathChange}
        />
      </InlineField>
      <InlineField label="API Key" labelWidth={12}>
        <SecretInput
          isConfigured={secureJsonFields.apiKey}
          value={secureJsonData?.apiKey || ''}
          placeholder="Your API key"
          width={40}
          onChange={onAPIKeyChange}
          onReset={onResetAPIKey}
        />
      </InlineField>
    </>
  );
};
```

### Query Editor

```typescript
import React, { ChangeEvent } from 'react';
import { InlineField, Input, Select } from '@grafana/ui';
import { QueryEditorProps, SelectableValue } from '@grafana/data';
import { DataSource } from './datasource';
import { MyDataSourceOptions, MyQuery } from './types';

type Props = QueryEditorProps<DataSource, MyQuery, MyDataSourceOptions>;

export const QueryEditor: React.FC<Props> = ({ query, onChange, onRunQuery }) => {
  const onQueryTextChange = (event: ChangeEvent<HTMLInputElement>) => {
    onChange({ ...query, queryText: event.target.value });
  };

  const onConstantChange = (event: ChangeEvent<HTMLInputElement>) => {
    onChange({ ...query, constant: parseFloat(event.target.value) });
    onRunQuery();
  };

  return (
    <>
      <InlineField label="Query Text" labelWidth={16} grow>
        <Input
          value={query.queryText || ''}
          onChange={onQueryTextChange}
          onBlur={onRunQuery}
        />
      </InlineField>
      <InlineField label="Constant" labelWidth={16}>
        <Input
          type="number"
          value={query.constant}
          onChange={onConstantChange}
          width={8}
        />
      </InlineField>
    </>
  );
};
```

## Backend SDK Patterns (Go)

### Data Source Implementation

```go
package plugin

import (
    "context"
    "encoding/json"
    "fmt"
    "net/http"

    "github.com/grafana/grafana-plugin-sdk-go/backend"
    "github.com/grafana/grafana-plugin-sdk-go/backend/instancemgmt"
    "github.com/grafana/grafana-plugin-sdk-go/backend/httpclient"
    "github.com/grafana/grafana-plugin-sdk-go/data"
)

type Datasource struct {
    settings   backend.DataSourceInstanceSettings
    httpClient *http.Client
}

func NewDatasource(ctx context.Context, settings backend.DataSourceInstanceSettings) (instancemgmt.Instance, error) {
    opts, err := settings.HTTPClientOptions(ctx)
    if err != nil {
        return nil, fmt.Errorf("http client options: %w", err)
    }

    cl, err := httpclient.New(opts)
    if err != nil {
        return nil, fmt.Errorf("httpclient new: %w", err)
    }

    return &Datasource{
        settings:   settings,
        httpClient: cl,
    }, nil
}

func (d *Datasource) Dispose() {
    // Cleanup resources
}

func (d *Datasource) QueryData(ctx context.Context, req *backend.QueryDataRequest) (*backend.QueryDataResponse, error) {
    response := backend.NewQueryDataResponse()

    for _, q := range req.Queries {
        res := d.query(ctx, req.PluginContext, q)
        response.Responses[q.RefID] = res
    }

    return response, nil
}

func (d *Datasource) query(ctx context.Context, pCtx backend.PluginContext, query backend.DataQuery) backend.DataResponse {
    var qm QueryModel
    if err := json.Unmarshal(query.JSON, &qm); err != nil {
        return backend.ErrDataResponse(backend.StatusBadRequest, fmt.Sprintf("json unmarshal: %v", err))
    }

    // Create data frame
    frame := data.NewFrame("response")
    frame.Fields = append(frame.Fields,
        data.NewField("time", nil, []time.Time{}),
        data.NewField("values", nil, []float64{}),
    )

    // Fetch and populate data...

    return backend.DataResponse{
        Frames: data.Frames{frame},
    }
}

func (d *Datasource) CheckHealth(ctx context.Context, req *backend.CheckHealthRequest) (*backend.CheckHealthResult, error) {
    resp, err := d.httpClient.Get(d.settings.URL + "/health")
    if err != nil {
        return &backend.CheckHealthResult{
            Status:  backend.HealthStatusError,
            Message: fmt.Sprintf("request error: %v", err),
        }, nil
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        return &backend.CheckHealthResult{
            Status:  backend.HealthStatusError,
            Message: fmt.Sprintf("got status code %d", resp.StatusCode),
        }, nil
    }

    return &backend.CheckHealthResult{
        Status:  backend.HealthStatusOk,
        Message: "Data source is working",
    }, nil
}
```

### Streaming Data

```go
func (d *Datasource) SubscribeStream(ctx context.Context, req *backend.SubscribeStreamRequest) (*backend.SubscribeStreamResponse, error) {
    return &backend.SubscribeStreamResponse{
        Status: backend.SubscribeStreamStatusOK,
    }, nil
}

func (d *Datasource) RunStream(ctx context.Context, req *backend.RunStreamRequest, sender *backend.StreamSender) error {
    ticker := time.NewTicker(time.Second)
    defer ticker.Stop()

    for {
        select {
        case <-ctx.Done():
            return ctx.Err()
        case t := <-ticker.C:
            frame := data.NewFrame("stream")
            frame.Fields = append(frame.Fields,
                data.NewField("time", nil, []time.Time{t}),
                data.NewField("value", nil, []float64{rand.Float64()}),
            )

            if err := sender.SendFrame(frame, data.IncludeAll); err != nil {
                return err
            }
        }
    }
}
```

### Resource Handler (Custom API)

```go
func (d *Datasource) CallResource(ctx context.Context, req *backend.CallResourceRequest, sender backend.CallResourceResponseSender) error {
    switch req.Path {
    case "namespaces":
        return d.handleNamespaces(ctx, req, sender)
    case "metrics":
        return d.handleMetrics(ctx, req, sender)
    default:
        return sender.Send(&backend.CallResourceResponse{
            Status: http.StatusNotFound,
        })
    }
}

func (d *Datasource) handleNamespaces(ctx context.Context, req *backend.CallResourceRequest, sender backend.CallResourceResponseSender) error {
    namespaces := []string{"ns-1", "ns-2", "ns-3"}
    body, _ := json.Marshal(map[string]interface{}{"namespaces": namespaces})

    return sender.Send(&backend.CallResourceResponse{
        Status: http.StatusOK,
        Headers: map[string][]string{
            "Content-Type": {"application/json"},
        },
        Body: body,
    })
}
```

## Theming

```typescript
import { useTheme2 } from '@grafana/ui';
import { GrafanaTheme2 } from '@grafana/data';

// In component
const theme = useTheme2();

// Access colors
const backgroundColor = theme.colors.background.primary;
const textColor = theme.colors.text.primary;
const successColor = theme.colors.success.main;

// Visualization colors
const seriesColor = theme.visualization.getColorByName('green');

// Spacing
const padding = theme.spacing(2); // 16px

// Typography
const fontSize = theme.typography.fontSize;
```

## Variable Support

```typescript
import { getTemplateSrv } from '@grafana/runtime';

// Replace variables in query
const templateSrv = getTemplateSrv();
const resolvedQuery = templateSrv.replace(query.queryText, options.scopedVars);

// In panel
const { replaceVariables } = props;
const resolvedText = replaceVariables(options.text);
```
