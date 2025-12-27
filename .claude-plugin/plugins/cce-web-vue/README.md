# cce-web-vue

> Vue.js and Nuxt.js development with Composition API, composables, and SSR/SSG patterns

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/nodnarbnitram/claude-code-extensions)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/nodnarbnitram/claude-code-extensions/blob/main/LICENSE)

A specialized Claude Code plugin providing expert Vue.js and Nuxt.js development agents with deep knowledge of Vue 3 Composition API, component architecture, state management, and modern full-stack patterns.

## Features

### Specialized Agents

This plugin includes three specialized Vue.js agents:

#### 1. vue-nuxt-expert
**Full-stack Nuxt.js development with SSR/SSG expertise**

Specializes in:
- Nuxt 3 application architecture
- Server-side rendering (SSR) and static site generation (SSG)
- Nitro server engine and API routes
- File-based routing and layouts
- Data fetching patterns (useFetch, useLazyFetch)
- SEO optimization and meta tags
- Performance optimization
- Deployment strategies

**Triggers on:**
- "nuxt", "nuxtjs", "nuxt 3"
- "ssr", "server-side rendering"
- "ssg", "static site generation"
- "nitro server", "server routes"
- "nuxt config", "nuxt modules"

#### 2. vue-component-architect
**Vue 3 Composition API and component design expert**

Specializes in:
- Vue 3 Composition API patterns
- Component architecture and design
- Reusable composables
- Props, emits, and slots
- Lifecycle hooks and reactivity
- Performance optimization
- TypeScript integration
- Testing strategies

**Triggers on:**
- "vue component", "vue 3"
- "composition api", "script setup"
- "composables", "vue hooks"
- "reactive", "ref", "computed"
- "component architecture"

#### 3. vue-state-manager
**State management patterns and Pinia expertise**

Specializes in:
- Pinia store architecture
- State management patterns
- Vuex 4 migration strategies
- Global vs. local state decisions
- Store composition and reusability
- DevTools integration
- SSR state hydration
- Testing state logic

**Triggers on:**
- "pinia", "pinia store"
- "state management", "global state"
- "vuex", "vuex migration"
- "store", "state composition"

## Installation

### From Marketplace

```bash
# Add the CCE marketplace (if not already added)
/plugin marketplace add https://github.com/nodnarbnitram/claude-code-extensions

# Install the plugin
/plugin install cce-web-vue@cce-marketplace
```

### From Local Path

```bash
# For development/testing
/plugin marketplace add /path/to/claude-code-extensions
/plugin install cce-web-vue@cce-marketplace
```

## Usage

Once installed, the Vue agents are automatically available and will activate based on your development context.

### Example Workflows

#### Building a Nuxt 3 Application

```
> I need to build a product catalog with server-side rendering in Nuxt 3
```

The `vue-nuxt-expert` agent will automatically activate and:
1. Fetch the latest Nuxt.js documentation
2. Analyze your project structure
3. Design optimal SSR/SSG architecture
4. Implement pages, server routes, and data fetching
5. Configure SEO and performance optimizations

#### Creating Vue Components

```
> Create a reusable product card component with Vue 3 Composition API
```

The `vue-component-architect` agent will:
1. Load Ultracite frontend standards
2. Fetch latest Vue.js documentation
3. Design accessible, type-safe components
4. Implement with best practices (props validation, emits, slots)
5. Provide testing recommendations

#### Setting Up State Management

```
> Set up Pinia for managing shopping cart state
```

The `vue-state-manager` agent will:
1. Analyze your current architecture
2. Design Pinia store structure
3. Implement composable state patterns
4. Handle SSR hydration if needed
5. Configure DevTools integration

### Command Namespacing

When installed as a plugin, agents are namespaced but automatically activate:

- **Standalone mode**: Agents trigger automatically based on context
- **Plugin mode**: Agents trigger with `cce-web-vue:` namespace (automatic)

## Agent Capabilities

### vue-nuxt-expert

**Key Capabilities:**
- Complete Nuxt 3 project setup and configuration
- File-based routing with dynamic routes
- Server API routes with validation and auth
- Database integration patterns
- Caching strategies (Redis, in-memory)
- Image and font optimization
- Meta tags and structured data
- Deployment configurations (Docker, serverless)

**Sample Output:**
```
## Nuxt.js Implementation Completed

### Architecture Decisions
- Universal rendering (SSR) for SEO-critical pages
- File-based routing with dynamic product routes
- Server API routes with Zod validation

### Features Implemented
- Pages: /products/[id].vue with SSR data fetching
- Server Routes: /api/products/[id].get.ts with caching
- useFetch with 5-minute cache TTL
- NuxtImg for optimized image delivery

### Performance Optimizations
- Redis caching for product queries
- Code splitting on route level
- Lazy loading for related products

### SEO & Metadata
- useSeoMeta with Open Graph tags
- Structured data for products
- Dynamic meta descriptions

### Files Created/Modified
- pages/products/[id].vue
- server/api/products/[id].get.ts
- composables/useCart.ts
```

### vue-component-architect

**Key Capabilities:**
- Vue 3 `<script setup>` patterns
- TypeScript prop and emit definitions
- Composable design and extraction
- Accessibility-first components
- Performance optimization (virtual scrolling, lazy loading)
- Testing with Vitest
- Integration with Vue Router and Pinia

**Sample Output:**
```
## Vue Implementation Report

### Components / Composables
- ProductCard.vue – Accessible card with lazy image loading
- useInfiniteScroll.ts – Composable for pagination

### Patterns Applied
- Composition API with <script setup>
- TypeScript prop validation
- Provide/Inject for theme context
- defineAsyncComponent for code splitting

### Performance Wins
- Virtual scroller for 1000+ items
- Intersection Observer for lazy images
- Computed memo for expensive filters

### Integration & Impact
- State: Pinia store `useProductStore`
- Router: Programmatic navigation on click
- Emits: 'add-to-cart' event to parent

### Next Steps
- Add Vitest tests for composables
- Consider Suspense for async data
```

### vue-state-manager

**Key Capabilities:**
- Pinia store design patterns
- Composition vs. Options API stores
- Store modularity and composition
- Getters, actions, and subscriptions
- SSR state serialization
- DevTools integration
- Migration from Vuex to Pinia
- Testing store logic

## Integration with Other Plugins

### Works Well With

- **cce-core**: Uses core hooks and commands
- **cce-web-react**: Learn from React patterns, compare approaches
- **cce-cloudflare**: Deploy Nuxt apps to Cloudflare Pages

### Complementary Workflows

1. **Full-Stack Development**:
   - Use `vue-nuxt-expert` for SSR setup
   - Use `vue-component-architect` for UI components
   - Use `vue-state-manager` for global state

2. **Migration Projects**:
   - Use `vue-component-architect` to modernize Options API → Composition API
   - Use `vue-state-manager` for Vuex → Pinia migration

3. **Performance Optimization**:
   - Use `vue-nuxt-expert` for SSR/SSG strategies
   - Use `vue-component-architect` for component-level optimizations

## Best Practices

### Documentation Fetching

All agents are configured to fetch the latest documentation:

1. **Primary**: context7 MCP (`/vuejs/vue`, `/nuxt/nuxt`)
2. **Fallback**: WebFetch from official docs
3. Always verify current version features

### Ultracite Integration

The `vue-component-architect` and `vue-nuxt-expert` agents load Ultracite standards via `/frontend-mode` for:
- Accessibility compliance
- Type safety enforcement
- Code quality rules
- Consistent patterns

### Project-Aware Implementation

All agents:
- Scan existing codebase first
- Detect Vue version and conventions
- Adapt to project-specific patterns
- Integrate seamlessly with existing architecture

## Configuration

### Environment Variables

No environment variables required. Agents use:
- Project detection for Vue/Nuxt version
- Runtime config from `nuxt.config.ts`
- Package.json dependencies

### Customization

The agents respect existing project patterns:
- Naming conventions (PascalCase, kebab-case)
- Folder structure (components/, composables/, pages/)
- State management approach (Pinia, Vuex, or custom)
- Testing framework (Vitest, Jest)

## Development Workflows

### New Nuxt 3 Project

```bash
# 1. Create Nuxt app
npx nuxi@latest init my-app
cd my-app

# 2. Install dependencies
npm install

# 3. Ask Claude with cce-web-vue
> Set up authentication with Nuxt 3 server routes and middleware
```

### Adding Components

```bash
# Claude will create in proper directories
> Create a navigation component with mobile menu
# Result: components/Navigation.vue
```

### State Management Setup

```bash
# Install Pinia
npm install pinia @pinia/nuxt

# Claude configures
> Set up Pinia for user authentication state
# Result: stores/useAuthStore.ts
```

## Testing

### Plugin Validation

```bash
# Validate plugin structure
/plugin validate .

# Check agents load correctly
/plugin install cce-web-vue@cce-marketplace
/agents  # Should show vue-nuxt-expert, vue-component-architect, vue-state-manager
```

### Agent Testing

```bash
# Test vue-nuxt-expert
> Create a Nuxt 3 page with SSR data fetching

# Test vue-component-architect
> Build a reusable Vue 3 button component with TypeScript

# Test vue-state-manager
> Set up Pinia store for shopping cart
```

### Validation Checklist

- [ ] Plugin installs without errors
- [ ] All 3 agents appear in `/agents`
- [ ] Agents trigger on relevant keywords
- [ ] Documentation fetching works (context7/WebFetch)
- [ ] Generated code follows Ultracite standards
- [ ] Components integrate with existing project

## Troubleshooting

### Agents Not Activating

**Problem**: Agents don't trigger automatically

**Solution**:
1. Verify installation: `/plugin list`
2. Check agent descriptions match your query
3. Use explicit keywords: "vue component", "nuxt ssr", "pinia store"

### Documentation Fetch Fails

**Problem**: Cannot fetch latest Vue/Nuxt docs

**Solution**:
1. Ensure context7 MCP is configured
2. Fallback to manual WebFetch
3. Check internet connectivity

### Code Quality Issues

**Problem**: Generated code doesn't match project standards

**Solution**:
1. Ensure `/frontend-mode` runs (loads Ultracite)
2. Check agents scan existing codebase first
3. Provide more context about project conventions

## Version History

### 1.0.0 (2025-12-23)
- Initial release
- 3 specialized Vue agents
- Vue 3 and Nuxt 3 support
- Composition API focus
- Pinia state management
- SSR/SSG expertise

## Contributing

This plugin is part of the [claude-code-extensions](https://github.com/nodnarbnitram/claude-code-extensions) repository.

### Adding Features

1. Fork the repository
2. Modify agents in `.claude/agents/specialized/vue/`
3. Update plugin.json if needed
4. Test thoroughly
5. Submit a pull request

### Reporting Issues

File issues at: https://github.com/nodnarbnitram/claude-code-extensions/issues

Use the label: `plugin:cce-web-vue`

## License

MIT License - see [LICENSE](https://github.com/nodnarbnitram/claude-code-extensions/blob/main/LICENSE)

## Resources

### Official Documentation
- [Vue.js](https://vuejs.org/)
- [Nuxt.js](https://nuxt.com/)
- [Pinia](https://pinia.vuejs.org/)
- [Vite](https://vitejs.dev/)

### Related Plugins
- [cce-core](../cce-core/) - Essential extensions
- [cce-web-react](../cce-web-react/) - React development

### Repository
- [GitHub](https://github.com/nodnarbnitram/claude-code-extensions)
- [Plugin Directory](./)

---

**Built with ❤️ by the Claude Code Extensions community**
