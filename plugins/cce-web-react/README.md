# CCE Web React Plugin

React, Next.js, and TanStack Start development for modern web applications.

## Overview

The **cce-web-react** plugin provides expert React development capabilities across the entire React ecosystem, from component architecture to full-stack applications with Next.js and TanStack Start.

## Features

- **Modern React**: React 18+ with Hooks, Suspense, Server Components (Next.js)
- **Component Architecture**: Composition patterns, custom hooks, context management
- **Next.js**: SSR, SSG, ISR, App Router, API routes, Middleware
- **TanStack Start**: Full-stack React with TanStack Router and Server Functions
- **State Management**: Context, useState, useReducer, external libraries
- **Performance**: Code splitting, lazy loading, memoization
- **Type Safety**: TypeScript integration patterns

## Plugin Components

### Agents (3)

- **react-component-architect**: React component design and modern patterns
  - Composition API and hooks
  - Component architecture
  - State management patterns
  - Performance optimization

- **react-nextjs-expert**: Next.js framework specialist
  - SSR, SSG, ISR strategies
  - App Router and Pages Router
  - Server Components and Actions
  - API routes and middleware
  - Image optimization

- **tanstack-start-expert**: TanStack Start full-stack development
  - TanStack Router integration
  - Server functions
  - Type-safe development
  - File-based routing

## Installation

### From Marketplace (Recommended)

```bash
# Add the CCE marketplace
/plugin marketplace add github:nodnarbnitram/claude-code-extensions

# Install React plugin
/plugin install cce-web-react@cce-marketplace
```

### From Local Source

```bash
git clone https://github.com/nodnarbnitram/claude-code-extensions.git
/plugin marketplace add /path/to/claude-code-extensions
/plugin install cce-web-react@cce-marketplace
```

## Usage

### Agents (Automatic Activation)

```bash
> Create a reusable Button component with TypeScript
# Uses react-component-architect

> Build a Next.js page with SSR for product listings
# Uses react-nextjs-expert

> Implement a TanStack Start route with server functions
# Uses tanstack-start-expert

> Add custom hook for data fetching with loading states
# Uses react-component-architect

> Set up Next.js middleware for authentication
# Uses react-nextjs-expert
```

### Example Workflows

**Component Development:**
```bash
> Create a Card component with hover effects and TypeScript props
# Generates reusable component with proper typing
```

**Next.js Application:**
```bash
> Set up Next.js App Router with dynamic routes for blog posts
# Implements file-based routing with [slug] pattern
```

**TanStack Start App:**
```bash
> Create a TanStack Start app with type-safe server functions
# Sets up full-stack React with TanStack Router
```

**Performance Optimization:**
```bash
> Optimize this component to prevent unnecessary re-renders
# Uses React.memo, useMemo, useCallback patterns
```

## Requirements

- **Claude Code**: Latest version
- **Node.js**: 18+ (for Next.js 14+)
- **React**: 18+
- **TypeScript**: 5+ (recommended)
- **Framework**: Next.js 14+ or TanStack Start

## Key Capabilities

**Component Patterns:**
- Functional components with hooks
- Compound components
- Render props and HOCs
- Custom hook composition

**Next.js Features:**
- Server and Client Components
- Streaming and Suspense
- Parallel and Intercepting Routes
- Server Actions
- Image and Font optimization
- Metadata API

**TanStack Start:**
- Type-safe routing
- Server functions
- Data loading strategies
- Code splitting

**State Management:**
- Context API patterns
- useReducer for complex state
- External libraries (Zustand, Jotai, Redux)

**Styling:**
- CSS Modules
- Tailwind CSS (use with cce-core:tailwind-frontend-expert)
- CSS-in-JS (styled-components, Emotion)
- Sass/SCSS

## Best Practices

- **Server vs Client**: Use Server Components by default in Next.js
- **Data Fetching**: Fetch on server when possible (SSR/SSG)
- **Performance**: Lazy load non-critical components
- **Type Safety**: Use TypeScript for props and state
- **Testing**: Component testing with React Testing Library

## License

MIT License - see [LICENSE](../../../LICENSE) for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/nodnarbnitram/claude-code-extensions/issues)
- **Documentation**: [Repository README](../../../README.md)
- **React Docs**: [react.dev](https://react.dev)
- **Next.js Docs**: [nextjs.org](https://nextjs.org)
