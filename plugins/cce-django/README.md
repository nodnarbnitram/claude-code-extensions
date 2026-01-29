# CCE Django Plugin

Professional Django backend development suite for Claude Code, featuring specialized agents for models, APIs, and ORM optimization.

## Overview

The **cce-django** plugin provides expert Django development capabilities through three specialized agents that understand Django best practices, project-specific patterns, and current framework features. Whether you're building REST APIs with Django REST Framework, implementing GraphQL endpoints, or optimizing complex database queries, this plugin delivers intelligent, project-aware solutions.

## Features

### Comprehensive Django Coverage

- **Backend Development**: Models, views, services, middleware, signals, management commands
- **API Development**: Django REST Framework (DRF) viewsets, serializers, GraphQL with Graphene
- **ORM Optimization**: Query optimization, database design, migrations, performance tuning
- **Security & Testing**: Django security best practices, comprehensive test patterns
- **Async Support**: Django 4.1+ async views, Channels for WebSockets, Celery integration

### Intelligent Project Integration

All agents analyze your existing codebase before implementing features:
- Detect project-specific naming conventions and architecture patterns
- Integrate seamlessly with existing models, serializers, and views
- Respect current authentication methods and permission classes
- Follow established coding standards and Django app structure

### Always Current

Agents fetch the latest Django and DRF documentation before implementing features, ensuring you use current best practices and syntax for your Django version.

## Plugin Components

### Agents

This plugin includes **3 specialized Django agents**:

#### 1. Django Backend Expert (`django-backend-expert`)

**Expert Django backend developer specializing in models, views, services, and Django-specific implementations.**

**Capabilities:**
- Django model design with custom managers and querysets
- Class-based and function-based views
- Service layer pattern implementation
- Django admin customization
- Middleware development
- Signal handlers
- Celery task implementation
- Management commands
- Multi-tenant architectures

**Use Cases:**
- "Create a Product model with category relationships and stock management"
- "Implement a service layer for order processing with transaction safety"
- "Build custom Django admin with inline editing and bulk actions"
- "Add middleware for tenant isolation in multi-tenant app"

#### 2. Django API Developer (`django-api-developer`)

**Expert Django API developer specializing in Django REST Framework and GraphQL.**

**Capabilities:**
- DRF viewsets and generic views
- Serializers with nested relationships
- Custom permissions and authentication (JWT, OAuth2, API keys)
- API versioning strategies
- Pagination, filtering, and throttling
- GraphQL schemas with Graphene-Django
- GraphQL resolvers and mutations
- OpenAPI/Swagger documentation
- Webhook implementation

**Use Cases:**
- "Create a REST API for the Product model with pagination and filtering"
- "Implement JWT authentication with refresh tokens"
- "Build a GraphQL schema for the order management system"
- "Add API versioning and deprecation strategy"

#### 3. Django ORM Expert (`django-orm-expert`)

**Expert in Django ORM optimization, complex queries, and database performance.**

**Capabilities:**
- QuerySet optimization with select_related/prefetch_related
- N+1 query prevention
- Complex aggregations and annotations
- Database indexing strategies
- Migration design and optimization
- Raw SQL when needed
- Database functions and window functions
- Query profiling and analysis
- Multi-database routing
- Read replica configuration

**Use Cases:**
- "Optimize this view that's causing N+1 queries"
- "Add database indexes for the most common query patterns"
- "Implement complex aggregation for sales analytics"
- "Profile and optimize slow product listing queries"

## Installation

### From Marketplace (Recommended)

```bash
# Add the CCE marketplace
/plugin marketplace add https://github.com/nodnarbnitram/claude-code-extensions

# Install the Django plugin
/plugin install cce-django@cce-marketplace
```

### From Local Source

```bash
# Clone the repository
git clone https://github.com/nodnarbnitram/claude-code-extensions.git

# Add as local marketplace
/plugin marketplace add /path/to/claude-code-extensions

# Install the plugin
/plugin install cce-django@cce-marketplace
```

## Usage

### Automatic Agent Delegation

When you request Django-related tasks, Claude Code automatically delegates to the appropriate specialized agent:

```bash
# Automatically uses django-backend-expert
> Create a Django model for blog posts with categories and tags

# Automatically uses django-api-developer
> Build a REST API for the blog with DRF serializers and viewsets

# Automatically uses django-orm-expert
> Optimize the blog post listing query to prevent N+1 issues
```

### Manual Agent Invocation

You can explicitly invoke agents when needed:

```bash
# Use the backend expert
> @django-backend-expert Create a custom User model with email authentication

# Use the API developer
> @django-api-developer Add GraphQL mutations for creating and updating posts

# Use the ORM expert
> @django-orm-expert Add database indexes for the most frequent queries
```

### Example Workflows

#### Building a Complete Feature

```bash
# 1. Backend expert creates models
> Create models for an e-commerce product catalog with categories and inventory

# 2. API developer builds endpoints
> Create a REST API for the product catalog with filtering and pagination

# 3. ORM expert optimizes performance
> Analyze and optimize the product listing queries for 100k+ products
```

#### Migrating from Function-Based to Class-Based Views

```bash
> @django-backend-expert Review the views in myapp/views.py and convert
  function-based views to class-based views following Django best practices
```

#### Adding Advanced Features

```bash
# GraphQL with DataLoader optimization
> @django-api-developer Add a GraphQL API with DataLoader to prevent N+1 queries

# Multi-tenant middleware
> @django-backend-expert Implement tenant isolation middleware using subdomains

# Complex analytics queries
> @django-orm-expert Build an analytics dashboard query that aggregates
  sales by category, month, and region
```

## Agent Coordination

Agents return structured reports that enable seamless coordination:

### Backend Expert Output
```
## Django Backend Implementation Completed

### Components Implemented
- Product model with UUID primary key
- Category model with hierarchical relationships
- ProductManager with custom querysets

### Key Features
- Automatic slug generation
- Stock management with validation
- Timestamped abstract base model

### Next Steps Available
- API Layer: Product and Category endpoints needed
- Database Optimization: Consider indexing slug and category fields
- Frontend Integration: GET /api/products/ and /api/categories/

### Files Modified/Created
- myapp/models.py: Added Product and Category models
- myapp/admin.py: Registered models with custom admin
```

### API Developer Output
```
## Django API Implementation Completed

### API Endpoints Created
- GET/POST /api/v1/products/
- GET/PUT/PATCH/DELETE /api/v1/products/{id}/
- GET /api/v1/categories/

### Authentication & Permissions
- JWT authentication with refresh tokens
- IsAuthenticatedOrReadOnly for products
- IsAdminUser for category management

### Serializers & Data Flow
- ProductSerializer with nested category data
- ProductCreateSerializer for write operations
- Custom validation for stock levels

### Files Created/Modified
- myapp/api/serializers.py: Product and Category serializers
- myapp/api/views.py: ViewSets with custom actions
- myapp/api/urls.py: API routing configuration
```

## Best Practices

### 1. Let Agents Analyze First

Agents examine your existing codebase before implementing features:
- They detect your project structure and conventions
- They match your naming patterns and code style
- They integrate with existing authentication and permissions

### 2. Leverage Latest Documentation

All agents fetch current Django/DRF documentation to ensure:
- You use the latest features for your Django version
- Deprecated patterns are avoided
- Security best practices are followed

### 3. Progressive Enhancement

Build features incrementally:
1. **Backend Expert**: Create models and business logic
2. **API Developer**: Add API endpoints
3. **ORM Expert**: Optimize performance as needed

### 4. Request Structured Output

Ask for structured reports when coordinating complex features:
```bash
> @django-backend-expert Create the order management models and
  return a structured report of components and integration points
```

## Django Patterns Included

### Architecture Patterns
- Clean Architecture in Django
- Service layer pattern
- Repository pattern
- Domain-Driven Design
- Django apps as bounded contexts

### Security Patterns
- OWASP compliance
- Content Security Policy
- Django security best practices
- API authentication strategies
- Permission class hierarchies

### Performance Patterns
- QuerySet optimization
- Database connection pooling
- Caching strategies (Redis, Memcached)
- Async views (Django 4.1+)
- Celery for background tasks

### Testing Patterns
- Model unit tests
- API endpoint tests
- Service layer testing with mocks
- Transaction test cases
- Test fixtures and factories

## Requirements

- **Claude Code**: Latest version
- **Python**: 3.11+ (for Django 4.2+)
- **Django**: Compatible with Django 3.2, 4.0, 4.1, 4.2, 5.0+
- **Optional**: Django REST Framework, Graphene-Django, Celery

## Plugin Commands

This plugin uses namespaced commands:

### In Plugin Mode
```bash
# Commands are namespaced with /cce-django:
# (Currently no commands - agents handle all functionality)
```

### In Standalone Mode
```bash
# Commands use unprefixed names
# (Currently no commands - agents handle all functionality)
```

## Troubleshooting

### Agent Not Activating

If agents don't activate automatically:
1. Check that the plugin is installed: `/plugin list`
2. Verify agents are loaded: `/agents` (should show django agents)
3. Use explicit invocation: `@django-backend-expert <task>`

### Documentation Fetch Issues

If agents can't fetch latest docs:
- Ensure you have internet connectivity
- Check if context7 MCP is configured (optional but recommended)
- Agents will fall back to built-in knowledge if fetch fails

### Performance Issues

For large Django projects:
- Use ORM expert for query optimization early
- Request profiling before implementing optimizations
- Ask for database index recommendations

## Contributing

This plugin is part of the [claude-code-extensions](https://github.com/nodnarbnitram/claude-code-extensions) repository.

To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes to agents in `.claude/agents/specialized/django/`
4. Test with both plugin and standalone modes
5. Submit a pull request

See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for detailed guidelines.

## License

MIT License - see [LICENSE](../../../LICENSE) for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/nodnarbnitram/claude-code-extensions/issues)
- **Discussions**: [GitHub Discussions](https://github.com/nodnarbnitram/claude-code-extensions/discussions)
- **Documentation**: [Repository README](../../../README.md)

## Related Plugins

- **cce-core**: Essential hooks, commands, and universal agents
- **cce-web-react**: React/Next.js frontend development
- **cce-kubernetes**: Kubernetes operations and diagnostics

## Version History

### 1.0.0 (Initial Release)
- Django Backend Expert agent
- Django API Developer agent
- Django ORM Expert agent
- Support for Django 3.2+, DRF, GraphQL
- Comprehensive testing and optimization patterns
