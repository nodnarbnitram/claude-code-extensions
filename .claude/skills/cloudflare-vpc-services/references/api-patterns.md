# VPC Service API Patterns

Comprehensive fetch() patterns for Workers VPC service bindings.

## Service Binding API

```typescript
const response = await env.VPC_SERVICE_BINDING.fetch(resource, options);
```

### Parameters

- `resource` (string | URL | Request): Absolute URL with protocol, host, path
- `options` (optional RequestInit): Standard fetch options

### Important Routing Behavior

The VPC Service configuration determines actual connectivity—not the fetch() URL:
- Host in fetch() → HTTP "Host" header and SNI value only
- Port in fetch() → **IGNORED** (uses configured service port)
- Actual connection → Service's configured hostname/IP and port

## Basic Patterns

### GET Request

```javascript
export default {
  async fetch(request, env) {
    const response = await env.VPC_SERVICE.fetch(
      "https://internal-api.company.local/users"
    );
    const users = await response.json();
    return new Response(JSON.stringify(users), {
      headers: { "Content-Type": "application/json" }
    });
  }
};
```

### POST with JSON Body

```javascript
const response = await env.VPC_SERVICE.fetch(
  "https://internal-api.company.local/users",
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${env.API_TOKEN}`
    },
    body: JSON.stringify({
      name: "John Doe",
      email: "john@example.com"
    })
  }
);
```

### PUT/PATCH Updates

```javascript
const response = await env.VPC_SERVICE.fetch(
  `https://internal-api.company.local/users/${userId}`,
  {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status: "active" })
  }
);
```

### DELETE Request

```javascript
const response = await env.VPC_SERVICE.fetch(
  `https://internal-api.company.local/users/${userId}`,
  { method: "DELETE" }
);
```

## Advanced Patterns

### HTTPS with IP Address

```javascript
// When service is configured with IP, use any hostname in URL
// The Host header will be set from the URL
const response = await env.VPC_SERVICE.fetch("https://10.0.1.50/api/data");
```

### API Gateway with Path Routing

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname.startsWith('/api/users')) {
      return env.USER_SERVICE.fetch(
        `https://user-api.internal${url.pathname}${url.search}`
      );
    } else if (url.pathname.startsWith('/api/orders')) {
      return env.ORDER_SERVICE.fetch(
        `https://orders-api.internal${url.pathname}${url.search}`
      );
    }

    return new Response('Not Found', { status: 404 });
  }
};
```

### Request Forwarding with Headers

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Forward the request with original headers
    const response = await env.VPC_SERVICE.fetch(
      `https://internal-api.local${url.pathname}`,
      {
        method: request.method,
        headers: request.headers,
        body: request.body
      }
    );

    return response;
  }
};
```

### Error Handling

```javascript
export default {
  async fetch(request, env) {
    try {
      const response = await env.VPC_SERVICE.fetch(
        "https://internal-api.local/data"
      );

      if (!response.ok) {
        return new Response(`Internal API error: ${response.status}`, {
          status: 502
        });
      }

      return response;
    } catch (error) {
      // Handle tunnel/connectivity errors
      return new Response(`VPC connection failed: ${error.message}`, {
        status: 503
      });
    }
  }
};
```

### Timeout with AbortController

```javascript
export default {
  async fetch(request, env) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);

    try {
      const response = await env.VPC_SERVICE.fetch(
        "https://internal-api.local/slow-endpoint",
        { signal: controller.signal }
      );
      clearTimeout(timeoutId);
      return response;
    } catch (error) {
      if (error.name === 'AbortError') {
        return new Response('Request timeout', { status: 504 });
      }
      throw error;
    }
  }
};
```

### Multiple Services

```javascript
export default {
  async fetch(request, env) {
    // Call multiple internal services
    const [users, orders] = await Promise.all([
      env.USER_SERVICE.fetch("https://user-api.internal/users"),
      env.ORDER_SERVICE.fetch("https://orders-api.internal/orders")
    ]);

    const userData = await users.json();
    const orderData = await orders.json();

    return new Response(JSON.stringify({
      users: userData,
      orders: orderData
    }), {
      headers: { "Content-Type": "application/json" }
    });
  }
};
```

## TypeScript Types

```typescript
interface Env {
  VPC_SERVICE: Fetcher;
  USER_SERVICE: Fetcher;
  ORDER_SERVICE: Fetcher;
  API_TOKEN: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const response = await env.VPC_SERVICE.fetch(
      "https://internal-api.local/data"
    );
    return response;
  }
};
```
