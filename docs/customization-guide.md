# Customization Guide

Every agent and sub-agent in this collection is designed to be used out of the box — but the real power comes from adapting them to your specific workflow, voice, and context. This guide walks you through the most common customization scenarios.

---

## The Golden Rule of Customization

**Change only what you need.** The agents in this collection have been written and tested to work well as-is. The more you change, the more you should test. Start with small adjustments and verify the agent's behavior before making bigger changes.

---

## Frontmatter Customizations

These changes are safe, low-risk, and almost always worth doing.

### Set Your Preferred Communication Channels

```yaml
comms_channels: [telegram, discord]

```

Update this to match the channels you actually use. If you only use Telegram, remove the others to keep things clean.

### Adjust Memory Profile

```yaml
memory_profile: "deep"

```

Options:

- `minimal` — Use when privacy matters or you want a fresh experience each session
- `standard` — Good default for most personal agents
- `deep` — Best for professional agents that need to remember contacts and commitments

### Configure Sub-Agents

```yaml
sub_agents: [email-manager, web-researcher]

```

Only list sub-agents you have installed. Listing a sub-agent that isn't installed will cause delegation failures.

### Set Model Preferences

```yaml
model_recommendations:
  primary: "gpt-4o"
  fallback: "claude-3-haiku"

```

Use the model that gives the best results for your use case. Code review agents often benefit from larger context models. Briefing agents can use faster, smaller models.

---

## Persona Customization

The `## Persona` section defines who the agent is. You can adapt it to match your style.

### Rename the Agent

Simply change the name in both the frontmatter and the Persona section:

```yaml
name: "Alex"

```

```markdown
## Persona

You are Alex, a warm and efficient personal assistant...

```

### Adjust the Tone

Find the tone description in `## Communication Style` and modify it:

**Before:**

```text
Warm, concise, and practical.

```

**After:**

```text
Formal and efficient. Use professional language at all times.
Avoid casual phrasing. Address the user as "you" not by first name.

```

### Add Domain Expertise

In the Persona section, add context about your industry or role:

```markdown
You are aware that the user works in the healthcare industry
and is familiar with HIPAA compliance requirements.
When handling patient-adjacent topics, always flag
privacy considerations.

```

---

## Behavior Customization

### Add a Core Behavior

Simply add a new bullet to `## Core Behaviors`:

```markdown

- Always respond in Spanish unless the user writes in another language
- Never suggest scheduling meetings before 9:00 AM or after 6:00 PM
- When the user says "EOM" at the end of a message, that means no reply is needed

```

### Remove a Behavior

Delete the bullet that describes the behavior you want to remove. Be careful not to remove behaviors that are referenced in other sections.

### Adjust Heartbeat Timing

For heartbeat-enabled agents, find the time reference in `## Heartbeat Behavior` and update it:

```markdown
Aria's heartbeat fires every morning at 6:30 AM local time (changed from 7:00 AM default).

```

Then update your OpenClaw heartbeat configuration to match.

---

## Adding Capabilities

If you want to extend what an agent can do:

1. Add the new capability to `## Capabilities`
2. If it requires a new skill, add the skill name to `skills_required` in the frontmatter
3. If appropriate, add a new `## Core Behaviors` bullet describing how the agent should use this capability
4. Add an example interaction demonstrating the new capability

---

## Customizing for a Team

When deploying agents for a whole team (especially Velocity for scrum teams), consider:

### Prime the Agent's Memory

On first use, give the agent context about your team:

> "Velocity, our team is: Alice (frontend lead), Bob (backend), Carol (QA). We run 2-week sprints. Our current sprint started March 25 and ends April 7. Our standup is at 9:30 AM Pacific in #team-standup."

### Set Standing Preferences

Tell the agent your preferences so it remembers them:

> "Maxwell, my working hours are 8 AM to 5 PM Pacific. Don't schedule meetings before 8 AM or after 4 PM. I prefer meetings clustered in the morning."

### Create a Team Brand Voice for Lyra

Paste your brand guidelines and tell Lyra to remember them:

> "Lyra, please remember this as our brand voice guide: [paste guidelines]. Use this for all content you write for us."

---

## Version Control Your Customizations

If you make significant changes to an agent, bump the version number in the frontmatter:

```yaml
version: "1.1.0"  # was 1.0.0

```

This helps you track what changed and makes it easier to see which agents have been customized vs. running the original.

---

## Contributing Your Customization Back

If you create a meaningfully improved or specialized version of an agent, consider contributing it back to the community as a new agent. See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines. A well-crafted "healthcare executive assistant" or "game developer code reviewer" could be valuable to others!
