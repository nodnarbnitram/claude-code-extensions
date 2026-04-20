---
title: Linear GraphQL Reference
---

# Linear GraphQL Reference

The Linear skill now uses `https://api.linear.app/graphql` exclusively.

## Authentication

Linear expects the raw API token in the `Authorization` header.

```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_TOKEN" \
  -d '{"query":"{ viewer { id name } }"}'
```

## Common Resolver Queries

### Resolve a Team by Key or Name

```graphql
query ResolveTeam($value: String!) {
  byKey: teams(filter: { key: { eq: $value } }, first: 2) {
    nodes { id key name }
  }
  byName: teams(filter: { name: { eq: $value } }, first: 2) {
    nodes { id key name }
  }
}
```

### Resolve a Project by Name

```graphql
query ResolveProject($value: String!) {
  projects(filter: { name: { eqIgnoreCase: $value } }, first: 2) {
    nodes { id name url }
  }
}
```

### Resolve a Workflow State by Name

```graphql
query ResolveWorkflowState($value: String!, $teamId: String!) {
  workflowStates(
    filter: {
      name: { eqIgnoreCase: $value }
      team: { id: { eq: $teamId } }
    }
    first: 2
  ) {
    nodes { id name }
  }
}
```

### Resolve a Milestone by Name

```graphql
query FindScopedMilestone($projectId: String!, $name: String!) {
  project(id: $projectId) {
    projectMilestones(filter: { name: { eq: $name } }, first: 10) {
      nodes {
        id
        name
        project { id name }
      }
    }
  }
}
```

## Issue Queries and Mutations

### Read an Issue by Identifier

```graphql
query GetIssueByIdentifier($teamKey: String!, $number: Float!) {
  issues(
    filter: { team: { key: { eq: $teamKey } }, number: { eq: $number } }
    first: 1
  ) {
    nodes {
      id
      identifier
      title
      description
      branchName
      priority
      url
      state { id name }
      team { id key name }
      project { id name }
      projectMilestone { id name targetDate }
      labels { nodes { id name } }
      comments { nodes { id body createdAt updatedAt } }
    }
  }
}
```

### List Issues

```graphql
query ListIssues($first: Int!, $filter: IssueFilter) {
  issues(first: $first, filter: $filter, includeArchived: false) {
    nodes {
      id
      identifier
      title
      url
      state { id name }
      assignee { id name }
      team { id key name }
      project { id name }
      labels { nodes { id name } }
    }
  }
}
```

### Search Issues

```graphql
query SearchIssues($term: String!, $first: Int!, $filter: IssueFilter) {
  searchIssues(
    term: $term
    first: $first
    filter: $filter
    includeArchived: false
  ) {
    nodes {
      id
      identifier
      title
      url
      state { id name }
    }
  }
}
```

### Create an Issue

```graphql
mutation CreateIssue($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    success
    issue {
      id
      identifier
      title
      branchName
      url
      state { id name }
    }
  }
}
```

### Update an Issue

```graphql
mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
  issueUpdate(id: $id, input: $input) {
    success
    issue {
      id
      identifier
      title
      url
      state { id name }
      labels { nodes { id name } }
    }
  }
}
```

### Add a Comment

```graphql
mutation CreateComment($input: CommentCreateInput!) {
  commentCreate(input: $input) {
    success
    comment {
      id
    }
  }
}
```

## Project and Milestone Mutations

### Create a Project

```graphql
mutation CreateProject($input: ProjectCreateInput!) {
  projectCreate(input: $input) {
    success
    project {
      id
      name
      description
      content
      state
      url
    }
  }
}
```

### Update Project Content

```graphql
mutation UpdateProject($id: String!, $input: ProjectUpdateInput!) {
  projectUpdate(id: $id, input: $input) {
    success
  }
}
```

### Create a Milestone

```graphql
mutation CreateProjectMilestone($input: ProjectMilestoneCreateInput!) {
  projectMilestoneCreate(input: $input) {
    success
    projectMilestone {
      id
      name
      description
      targetDate
    }
  }
}
```

## Document Queries and Mutations

### Create a Document

```graphql
mutation CreateDocument($input: DocumentCreateInput!) {
  documentCreate(input: $input) {
    success
    document {
      id
      title
      content
      slugId
      url
      icon
      color
      createdAt
      updatedAt
      trashed
    }
  }
}
```

### List Documents

```graphql
query ListDocuments($first: Int!, $filter: DocumentFilter) {
  documents(first: $first, filter: $filter) {
    nodes {
      id
      title
      slugId
      url
      updatedAt
      trashed
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Read a Document

```graphql
query GetDocument($id: String!) {
  document(id: $id) {
    id
    title
    content
    slugId
    url
    icon
    color
    createdAt
    updatedAt
    trashed
  }
}
```
