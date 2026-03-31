export const VERSION_ORDER = [
  "s01", "s02", "s03", "s04", "s05", "s06", "s07", "s08", "s09", "s10", "s11", "s12"
] as const;

export const LEARNING_PATH = VERSION_ORDER;

export type VersionId = typeof LEARNING_PATH[number];

export const VERSION_META: Record<string, {
  title: string;
  subtitle: string;
  coreAddition: string;
  keyInsight: string;
  layer: "tools" | "planning" | "memory" | "concurrency" | "collaboration";
  prevVersion: string | null;
}> = {
  s01: { title: "The Agent Loop", subtitle: "Minimal Harness Core", coreAddition: "Single-loop execution with one tool", keyInsight: "The coding agent starts as a loop, not a workflow graph", layer: "tools", prevVersion: null },
  s02: { title: "Tool Protocol", subtitle: "Capabilities Without Loop Changes", coreAddition: "Schema-backed tool registry", keyInsight: "New capability should change the tool pool, not the loop shape", layer: "tools", prevVersion: "s01" },
  s03: { title: "Session State", subtitle: "Short-Lived Guidance", coreAddition: "Todo-style checklist for the active turn", keyInsight: "Session guidance and durable task state are not the same thing", layer: "planning", prevVersion: "s02" },
  s04: { title: "Delegation Modes", subtitle: "Fresh vs Forked Workers", coreAddition: "Two distinct worker context models", keyInsight: "Some subagents start clean; others inherit scoped context", layer: "planning", prevVersion: "s03" },
  s05: { title: "Skill Discovery", subtitle: "Activate Then Load", coreAddition: "Active and conditional skill loading", keyInsight: "Knowledge is cheaper when the harness discovers and activates it late", layer: "planning", prevVersion: "s04" },
  s06: { title: "Context Management Stack", subtitle: "Budget, Summaries, Compact", coreAddition: "Layered history control", keyInsight: "Context management is a stack of interventions, not one compact button", layer: "memory", prevVersion: "s05" },
  s07: { title: "Persistent Task Runtime", subtitle: "Control Plane Outside the Transcript", coreAddition: "Durable file-backed tasks", keyInsight: "Tasks matter because they survive context resets", layer: "planning", prevVersion: "s06" },
  s08: { title: "Background Runtime", subtitle: "Foreground Loop, Background Work", coreAddition: "Runtime-owned background tasks", keyInsight: "Slow operations belong to the runtime, not the foreground reasoning thread", layer: "concurrency", prevVersion: "s07" },
  s09: { title: "Team Mailboxes", subtitle: "Shared Collaboration State", coreAddition: "Roster + inbox + team identity", keyInsight: "Multi-agent work needs explicit shared state, not just extra prompts", layer: "collaboration", prevVersion: "s08" },
  s10: { title: "Team Protocols", subtitle: "Request IDs and Approval Flows", coreAddition: "Structured request-response coordination", keyInsight: "Safety improves when coordination is protocolized", layer: "collaboration", prevVersion: "s09" },
  s11: { title: "Self-Organizing Workers", subtitle: "Poll, Claim, Resume", coreAddition: "Idle loop over inbox and task board", keyInsight: "Autonomy appears when the harness lets agents find work between turns", layer: "collaboration", prevVersion: "s10" },
  s12: { title: "Worktree Isolation", subtitle: "Execution Lanes Bound to Tasks", coreAddition: "Task-linked isolation records", keyInsight: "Task state is the control plane; worktrees isolate execution", layer: "collaboration", prevVersion: "s11" },
};

export const LAYERS = [
  { id: "tools" as const, label: "Tools & Execution", color: "#3B82F6", versions: ["s01", "s02"] },
  { id: "planning" as const, label: "Planning & Coordination", color: "#10B981", versions: ["s03", "s04", "s05", "s07"] },
  { id: "memory" as const, label: "Memory Management", color: "#8B5CF6", versions: ["s06"] },
  { id: "concurrency" as const, label: "Concurrency", color: "#F59E0B", versions: ["s08"] },
  { id: "collaboration" as const, label: "Collaboration", color: "#EF4444", versions: ["s09", "s10", "s11", "s12"] },
] as const;
