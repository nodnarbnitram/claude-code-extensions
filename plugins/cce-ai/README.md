# cce-ai - AI/ML Development Plugin

**Version:** 1.0.0
**Status:** Production Ready
**Category:** AI/ML Development

## Overview

The `cce-ai` plugin provides comprehensive AI/ML development capabilities through specialized agents covering the full spectrum of modern AI development: from LLM architecture and prompt engineering to NLP systems and production ML deployment.

This plugin is designed for teams building AI-powered applications, training and deploying machine learning models, implementing LLM-based systems, or developing natural language processing solutions.

## What's Included

### Agents (5 specialists)

All agents are located in `./.claude/agents/specialized/data-ai/`:

1. **ai-engineer** - Senior AI engineer for comprehensive AI system design
   - AI architecture design and model selection
   - Training pipeline development
   - Production deployment and monitoring
   - Ethical AI and governance frameworks
   - Multi-modal systems integration

2. **llm-architect** - LLM system design and optimization expert
   - Large language model architecture
   - Fine-tuning strategies (LoRA/QLoRA, RLHF)
   - RAG implementation and optimization
   - Serving infrastructure (vLLM, TGI, Triton)
   - Safety mechanisms and cost optimization

3. **machine-learning-engineer** - Production ML deployment specialist
   - Model optimization (quantization, pruning, distillation)
   - Real-time inference infrastructure
   - Batch prediction systems
   - Auto-scaling and monitoring
   - Edge deployment strategies

4. **nlp-engineer** - Natural language processing expert
   - Text preprocessing and tokenization
   - Named entity recognition and classification
   - Machine translation and question answering
   - Sentiment analysis and information extraction
   - Multilingual support (12+ languages)

5. **prompt-engineer** - Prompt design and optimization specialist
   - Prompt architecture and patterns
   - Few-shot learning and chain-of-thought
   - A/B testing and evaluation frameworks
   - Token optimization and cost reduction
   - Production prompt management

## Use Cases

### LLM Applications
- Design and deploy scalable LLM systems
- Implement RAG (Retrieval-Augmented Generation)
- Fine-tune models for specific domains
- Optimize inference performance and costs
- Build conversational AI and chatbots

### Machine Learning Operations
- Deploy models to production with monitoring
- Optimize model size and inference latency
- Implement auto-scaling ML services
- Build batch prediction pipelines
- Deploy models to edge devices

### Natural Language Processing
- Build multilingual NLP systems
- Implement named entity recognition
- Create sentiment analysis pipelines
- Develop question answering systems
- Extract information from text at scale

### Prompt Engineering
- Design effective prompt templates
- Optimize token usage and costs
- Implement chain-of-thought reasoning
- A/B test prompt variations
- Manage production prompt systems

### AI Engineering
- Design end-to-end AI systems
- Select and train models
- Implement ethical AI frameworks
- Build multi-modal AI applications
- Ensure AI governance and compliance

## Agent Collaboration

The agents in this plugin are designed to work together:

```
ai-engineer
    ├── Collaborates with llm-architect on LLM integration
    ├── Supports machine-learning-engineer on deployment
    ├── Works with nlp-engineer on language tasks
    └── Guides prompt-engineer on LLM systems

llm-architect
    ├── Supports prompt-engineer on optimization
    ├── Works with machine-learning-engineer on serving
    └── Guides backend-developer on API design

machine-learning-engineer
    ├── Collaborates with ai-engineer on model selection
    ├── Supports mlops-engineer on infrastructure
    └── Works with data-engineer on pipelines

nlp-engineer
    ├── Collaborates with ai-engineer on model architecture
    ├── Works with machine-learning-engineer on deployment
    └── Assists prompt-engineer on language models

prompt-engineer
    ├── Collaborates with llm-architect on system design
    ├── Supports ai-engineer on LLM integration
    └── Works with data-scientist on evaluation
```

## Installation

### From Marketplace (Recommended)

```bash
# Add the marketplace (if not already added)
/plugin marketplace add https://github.com/nodnarbnitram/claude-code-extensions

# Install the plugin
/plugin install cce-ai@cce-marketplace
```

### From Local Path (Development)

```bash
# Clone the repository
git clone https://github.com/nodnarbnitram/claude-code-extensions.git

# Add local marketplace
/plugin marketplace add /path/to/claude-code-extensions

# Install from local path
/plugin install cce-ai@cce-marketplace
```

## Usage

Once installed, agents will automatically activate based on your tasks:

### Automatic Agent Selection

The agents will automatically engage when you mention AI/ML related tasks:

```
> Help me implement a RAG system for document search
# llm-architect will engage

> Optimize this model for production deployment
# machine-learning-engineer will engage

> Design prompts for better LLM performance
# prompt-engineer will engage

> Build a multilingual sentiment analysis pipeline
# nlp-engineer will engage

> Design an end-to-end AI system for recommendation
# ai-engineer will engage
```

### Manual Agent Invocation

You can also explicitly request specific agents:

```
> @ai-engineer design a training pipeline for image classification

> @llm-architect help me fine-tune this model with LoRA

> @machine-learning-engineer optimize inference latency

> @nlp-engineer implement named entity recognition

> @prompt-engineer create few-shot examples for this task
```

## Agent Capabilities

### ai-engineer
**Color:** Yellow
**Focus:** Comprehensive AI system design and implementation

**Key Capabilities:**
- Model architecture selection and design
- Training pipeline development
- Inference optimization techniques
- Multi-modal systems integration
- Ethical AI and bias detection
- AI governance frameworks
- Edge AI deployment

**Tools:** TensorFlow, PyTorch, JAX, ONNX, TensorRT, Core ML

### llm-architect
**Color:** Blue
**Focus:** Large language model systems and optimization

**Key Capabilities:**
- Fine-tuning strategies (LoRA/QLoRA, RLHF)
- RAG implementation and optimization
- Serving patterns (vLLM, TGI, Triton)
- Model quantization and optimization
- Safety mechanisms and content filtering
- Token optimization and cost control
- Multi-model orchestration

**Tools:** Transformers, LangChain, LlamaIndex, vLLM, Weights & Biases

### machine-learning-engineer
**Color:** Purple
**Focus:** Production ML deployment and operations

**Key Capabilities:**
- Model optimization (quantization, pruning, distillation)
- Real-time inference infrastructure
- Batch prediction systems
- Auto-scaling strategies
- Multi-model serving
- Edge deployment
- Performance monitoring

**Tools:** TensorFlow, PyTorch, ONNX, Triton, BentoML, Ray, vLLM

### nlp-engineer
**Color:** Orange
**Focus:** Natural language processing systems

**Key Capabilities:**
- Text preprocessing pipelines
- Named entity recognition
- Text classification and sentiment analysis
- Machine translation (12+ languages)
- Question answering systems
- Information extraction
- Conversational AI

**Tools:** Transformers, spaCy, NLTK, Hugging Face, Gensim, FastText

### prompt-engineer
**Color:** Pink
**Focus:** Prompt design and optimization

**Key Capabilities:**
- Prompt architecture patterns
- Few-shot learning and chain-of-thought
- A/B testing frameworks
- Token optimization techniques
- Safety mechanisms
- Multi-model strategies
- Production prompt management

**Tools:** OpenAI API, Anthropic API, LangChain, PromptFlow, Jupyter

## Performance Targets

Each agent follows strict performance benchmarks:

| Agent | Metric | Target |
|-------|--------|--------|
| ai-engineer | Model accuracy | > 94% |
| ai-engineer | Inference latency | < 100ms |
| llm-architect | Inference latency | < 200ms |
| llm-architect | Throughput | > 100 tokens/s |
| machine-learning-engineer | Inference latency | < 100ms |
| machine-learning-engineer | Throughput | > 1000 RPS |
| nlp-engineer | F1 score | > 0.85 |
| nlp-engineer | Latency | < 100ms |
| prompt-engineer | Accuracy | > 90% |
| prompt-engineer | Response time | < 2s |

## Best Practices

### When to Use Each Agent

**ai-engineer:** Use for overall AI system design, model selection, and comprehensive AI solutions requiring multiple components.

**llm-architect:** Use for LLM-specific tasks like fine-tuning, RAG implementation, or optimizing LLM serving infrastructure.

**machine-learning-engineer:** Use for deploying models to production, optimizing inference, or building scalable ML services.

**nlp-engineer:** Use for text processing tasks, language understanding, or multilingual NLP applications.

**prompt-engineer:** Use for optimizing LLM prompts, reducing token costs, or implementing prompt testing frameworks.

### Workflow Recommendations

1. **Start with ai-engineer** for high-level system design
2. **Delegate to specialists** for specific implementations
3. **Use llm-architect** for LLM infrastructure decisions
4. **Leverage machine-learning-engineer** for deployment
5. **Consult prompt-engineer** for LLM interaction optimization

## Examples

### Example 1: Building a RAG System

```
> I need to build a RAG system for internal documentation search

# llm-architect engages and provides:
1. Document processing strategy
2. Embedding model selection
3. Vector store recommendation (e.g., Pinecone, Weaviate)
4. Retrieval optimization techniques
5. Context management strategies
6. Serving infrastructure design
```

### Example 2: Optimizing Model Deployment

```
> This model is too slow in production. Latency is 500ms.

# machine-learning-engineer engages and:
1. Profiles model performance
2. Applies quantization (4-bit or 8-bit)
3. Implements model caching
4. Sets up batch processing
5. Configures auto-scaling
6. Reduces latency to < 100ms
```

### Example 3: Prompt Optimization

```
> My prompts are using too many tokens and costing too much

# prompt-engineer engages and:
1. Analyzes current prompts
2. Implements token compression
3. Optimizes context usage
4. Creates A/B testing framework
5. Measures cost reduction (typically 30-50%)
```

### Example 4: Multilingual NLP Pipeline

```
> Build a sentiment analysis system supporting 10 languages

# nlp-engineer engages and:
1. Designs preprocessing pipeline
2. Selects multilingual models
3. Implements language detection
4. Creates sentiment classification
5. Builds real-time API
6. Achieves > 0.85 F1 score across languages
```

## Requirements

### System Requirements
- Python 3.11+ (for AI/ML tools)
- GPU recommended for model training/inference
- 16GB+ RAM for LLM work
- Sufficient disk space for models

### Optional Dependencies
- TensorFlow or PyTorch
- Hugging Face Transformers
- LangChain / LlamaIndex
- CUDA toolkit (for GPU acceleration)
- vLLM or other serving frameworks

## Compatibility

- **Claude Code Version:** 0.1.0+
- **Python:** 3.11+
- **Operating Systems:** Linux, macOS, Windows (WSL2)
- **GPU Support:** NVIDIA CUDA 11.8+

## Troubleshooting

### Agents Not Appearing

```bash
# Verify plugin installation
/plugin list

# Check if agents are loaded
/agents

# Reinstall if needed
/plugin update cce-ai
```

### Agent Not Auto-Engaging

Try explicit invocation with `@agent-name` syntax, or ensure your query includes relevant AI/ML keywords.

### Performance Issues

Ensure you have:
- Adequate RAM (16GB+ for LLM work)
- GPU drivers installed (for GPU acceleration)
- Python 3.11+ with required dependencies

## Contributing

This plugin is part of the Claude Code Extensions project. Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for details.

## License

MIT License - see [LICENSE](../../../LICENSE) for details.

## Support

- **Issues:** https://github.com/nodnarbnitram/claude-code-extensions/issues
- **Discussions:** https://github.com/nodnarbnitram/claude-code-extensions/discussions
- **Documentation:** https://github.com/nodnarbnitram/claude-code-extensions

## Changelog

### v1.0.0 (Initial Release)
- 5 specialized AI/ML agents
- Complete LLM architecture support
- Production ML deployment capabilities
- Multilingual NLP processing
- Prompt engineering and optimization
- Full documentation and examples

## Related Plugins

- **cce-core:** Essential extensions and hooks
- **cce-kubernetes:** Kubernetes operations and health checks
- **cce-cloudflare:** Cloudflare Workers and AI integration
- **cce-esphome:** IoT device configuration and management
- **cce-web-react:** React and frontend development

---

**Built with Claude Code Extensions** | [GitHub](https://github.com/nodnarbnitram/claude-code-extensions)
