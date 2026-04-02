# Home Assistant Voice Control

> Configure Assist pipelines, custom intents, wake words, and voice satellites for local voice control.

| | |
|---|---|
| **Status** | Production |
| **Version** | 1.0.0 |
| **Last Updated** | 2025-12-31 |
| **Confidence** | 5/5 |
| **Key Docs** | [Voice Control Docs](https://www.home-assistant.io/voice_control/) |

## What This Skill Does

Provides expert guidance for Home Assistant Assist voice control capabilities, including:
- Assist pipeline configuration (connecting STT, TTS, intents, and conversation agents)
- Custom intent creation with sentence patterns, slots, and lists
- Wake word setup (openWakeWord, Porcupine)
- Speech processing configuration (local Piper TTS + Faster Whisper STT, or cloud alternatives)
- Voice satellite setup for ESPHome devices (ESP32-S3, I2S microphones, speakers)
- Multi-language support and performance tuning
- Integration with OpenAI, Anthropic, and custom conversation agents

### Core Capabilities

- Configure Assist pipelines with custom STT/TTS engines
- Create natural voice commands using sentence patterns, slots, and lists
- Set up local wake words (Alexa, Hey Google, Hey Siri or custom)
- Build voice satellites with ESPHome hardware (INMP441 mic, MAX98357A speaker)
- Configure TTS engine selection (Piper local, Google Cloud, OpenAI)
- Configure STT engine selection (Faster Whisper local, Google Cloud, Whisper API)
- Debug intent matching with Assist Developer Tools
- Optimize performance for single-board computers

## Auto-Trigger Keywords

### Primary Keywords
Exact terms that strongly trigger this skill:
- Assist pipeline
- Voice control
- Wake word
- Custom intent
- Sentence pattern
- STT (speech-to-text)
- TTS (text-to-speech)
- Piper
- Whisper
- Voice satellite

### Secondary Keywords
Related terms that may trigger in combination:
- Voice assistant
- Voice command
- Wake detection
- Speech processing
- Intent recognition
- Conversation agent
- Wyoming protocol
- ESPHome voice
- Audio pipeline
- Voice feedback

### Error-Based Keywords
Common error messages that should trigger this skill:
- "No matching intent"
- "Engine not found"
- "TTS engine not available"
- "STT engine not available"
- "Wake word entity not found"
- "Pipeline configuration error"
- "Sentence pattern syntax error"

## Known Issues Prevention

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| Intent not matching | Sentence pattern too strict or list values incorrect | Use optional groups `[]` and verify list values in Developer Tools |
| "Engine not available" | TTS/STT component not installed or configured | Install component via integrations, verify platform field matches |
| Wake word not triggering | Model sensitivity too high or microphone not connected | Test microphone separately, adjust model selection, check WiFi signal |
| Voice satellite disconnects | WiFi instability or ESPHome OTA conflicts | Move router closer, update ESPHome firmware, disable OTA during testing |
| Slot extraction failing | Slot name mismatch between sentences and lists | Verify `{slot:list}` matches list definition, use Developer Tools to test |

## When to Use

### Use This Skill For
- Setting up or troubleshooting Assist pipelines
- Creating custom voice commands with sentence patterns
- Configuring TTS/STT engines (local or cloud)
- Building ESPHome voice satellites
- Debugging intent recognition issues
- Optimizing voice control performance
- Integrating custom conversation agents

### Don't Use This Skill For
- General Home Assistant installation (use home-assistant-core skill)
- YAML validation for non-voice components
- Cloud service setup (use service-specific documentation)

## Quick Usage

```yaml
# Complete working Assist pipeline example
assist_pipeline:
  pipelines:
    - language: en
      name: Default Pipeline
      stt_engine: faster_whisper
      tts_engine: tts.piper
      conversation_engine: conversation.home_assistant
      wake_word_entity: binary_sensor.wake_word

# Minimal custom intent
custom_sentences/en/custom.yaml:
---
language: en
version: 1

intents:
  TurnOn:
    data:
      - sentences:
          - "turn on {name:list}"
        lists:
          name:
            - "bedroom light"
            - "kitchen light"
```

## Token Efficiency

| Approach | Estimated Tokens | Time |
|----------|-----------------|------|
| Manual documentation reading | 8,000+ | 30+ minutes |
| With This Skill | 2,000-3,000 | 5-10 minutes |
| **Savings** | **60-75%** | **75% faster** |

## File Structure

```
ha-voice/
├── SKILL.md                # Detailed instructions, patterns, troubleshooting
├── README.md              # This file - discovery and quick reference
└── references/            # Supporting documentation
    └── intent-patterns.md # Common intent configuration patterns
```

## Dependencies

No external Python packages required. Skill uses Home Assistant's native components:

| Component | Version | Purpose | Required |
|-----------|---------|---------|----------|
| Home Assistant | 2024.1+ | Core voice control platform | Yes |
| Faster Whisper | 0.5+ | Local speech-to-text | Optional (recommended) |
| Piper TTS | 1.0+ | Local text-to-speech | Optional (recommended) |
| OpenWakeWord | 0.3+ | Local wake word detection | Optional |

## Official Documentation

- [Home Assistant Voice Control](https://www.home-assistant.io/voice_control/)
- [Assist Pipeline Integration](https://www.home-assistant.io/integrations/assist_pipeline/)
- [Intent Recognition Guide](https://developers.home-assistant.io/docs/voice/intent-recognition)
- [Conversation Integration](https://www.home-assistant.io/integrations/conversation/)
- [Piper TTS Documentation](https://github.com/rhasspy/piper)
- [Faster Whisper Documentation](https://github.com/SYSTRAN/faster-whisper)

## Related Skills

- `ha-dashboard` - Configure Lovelace UI for voice control testing
- `ha-automations` - Create automations triggered by voice intents
- `esphome-config-helper` - Configure ESP32 voice satellites

---

**License:** MIT
