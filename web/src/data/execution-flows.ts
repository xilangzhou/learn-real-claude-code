import type { FlowNode, FlowEdge } from "@/types/agent-data";

export interface FlowDefinition {
  nodes: FlowNode[];
  edges: FlowEdge[];
}

const FLOW_WIDTH = 600;
const COL_CENTER = FLOW_WIDTH / 2;
const COL_LEFT = 140;
const COL_RIGHT = FLOW_WIDTH - 140;

export const EXECUTION_FLOWS: Record<string, FlowDefinition> = {
  s01: {
    nodes: [
      { id: "start", label: "User Input", type: "start", x: COL_CENTER, y: 30 },
      { id: "llm", label: "LLM Call", type: "process", x: COL_CENTER, y: 110 },
      { id: "tool", label: "tool_use?", type: "decision", x: COL_CENTER, y: 190 },
      { id: "bash", label: "Run Bash", type: "subprocess", x: COL_LEFT, y: 280 },
      { id: "append", label: "Append Result", type: "process", x: COL_LEFT, y: 360 },
      { id: "end", label: "Answer User", type: "end", x: COL_RIGHT, y: 280 },
    ],
    edges: [
      { from: "start", to: "llm" },
      { from: "llm", to: "tool" },
      { from: "tool", to: "bash", label: "yes" },
      { from: "tool", to: "end", label: "no" },
      { from: "bash", to: "append" },
      { from: "append", to: "llm" },
    ],
  },
  s02: {
    nodes: [
      { id: "start", label: "User Input", type: "start", x: COL_CENTER, y: 30 },
      { id: "llm", label: "LLM Call", type: "process", x: COL_CENTER, y: 110 },
      { id: "tool", label: "tool_use?", type: "decision", x: COL_CENTER, y: 190 },
      { id: "dispatch", label: "Tool Registry", type: "process", x: COL_LEFT, y: 280 },
      { id: "exec", label: "Read / Write / Edit\nOr Bash", type: "subprocess", x: COL_LEFT, y: 360 },
      { id: "append", label: "Append Result", type: "process", x: COL_LEFT, y: 440 },
      { id: "end", label: "Answer User", type: "end", x: COL_RIGHT, y: 280 },
    ],
    edges: [
      { from: "start", to: "llm" },
      { from: "llm", to: "tool" },
      { from: "tool", to: "dispatch", label: "yes" },
      { from: "tool", to: "end", label: "no" },
      { from: "dispatch", to: "exec" },
      { from: "exec", to: "append" },
      { from: "append", to: "llm" },
    ],
  },
  s03: {
    nodes: [
      { id: "start", label: "User Input", type: "start", x: COL_CENTER, y: 30 },
      { id: "llm", label: "LLM Call", type: "process", x: COL_CENTER, y: 110 },
      { id: "tool", label: "todo_write?", type: "decision", x: COL_CENTER, y: 190 },
      { id: "todo", label: "Update Session\nChecklist", type: "subprocess", x: COL_LEFT, y: 280 },
      { id: "work", label: "Do The Next Step", type: "process", x: COL_LEFT, y: 360 },
      { id: "end", label: "Answer User", type: "end", x: COL_RIGHT, y: 280 },
    ],
    edges: [
      { from: "start", to: "llm" },
      { from: "llm", to: "tool" },
      { from: "tool", to: "todo", label: "yes" },
      { from: "tool", to: "end", label: "no" },
      { from: "todo", to: "work" },
      { from: "work", to: "llm" },
    ],
  },
  s04: {
    nodes: [
      { id: "start", label: "User Input", type: "start", x: COL_CENTER, y: 30 },
      { id: "llm", label: "LLM Call", type: "process", x: COL_CENTER, y: 110 },
      { id: "delegate", label: "delegate?", type: "decision", x: COL_CENTER, y: 190 },
      { id: "fresh", label: "Fresh Worker", type: "subprocess", x: COL_LEFT, y: 280 },
      { id: "fork", label: "Forked Worker", type: "subprocess", x: COL_RIGHT, y: 280 },
      { id: "summary", label: "Return Summary", type: "process", x: COL_CENTER, y: 390 },
    ],
    edges: [
      { from: "start", to: "llm" },
      { from: "llm", to: "delegate" },
      { from: "delegate", to: "fresh", label: "fresh" },
      { from: "delegate", to: "fork", label: "fork" },
      { from: "fresh", to: "summary" },
      { from: "fork", to: "summary" },
      { from: "summary", to: "llm" },
    ],
  },
  s05: {
    nodes: [
      { id: "start", label: "User Input", type: "start", x: COL_CENTER, y: 30 },
      { id: "match", label: "Match Request\nAgainst Metadata", type: "process", x: COL_CENTER, y: 110 },
      { id: "skill", label: "Relevant Skill?", type: "decision", x: COL_CENTER, y: 190 },
      { id: "load", label: "Load Skill\nInstructions", type: "subprocess", x: COL_LEFT, y: 280 },
      { id: "inject", label: "Inject Active\nGuidance", type: "process", x: COL_LEFT, y: 360 },
      { id: "end", label: "Proceed With Task", type: "end", x: COL_RIGHT, y: 280 },
    ],
    edges: [
      { from: "start", to: "match" },
      { from: "match", to: "skill" },
      { from: "skill", to: "load", label: "yes" },
      { from: "skill", to: "end", label: "no" },
      { from: "load", to: "inject" },
      { from: "inject", to: "end" },
    ],
  },
  s06: {
    nodes: [
      { id: "start", label: "Long Session", type: "start", x: COL_CENTER, y: 30 },
      { id: "budget", label: "Trim Large\nResults", type: "process", x: COL_CENTER, y: 110 },
      { id: "summary", label: "Update Rolling\nSummary", type: "process", x: COL_CENTER, y: 190 },
      { id: "manual", label: "Need Manual\nCompact?", type: "decision", x: COL_CENTER, y: 270 },
      { id: "compact", label: "Run Compact", type: "subprocess", x: COL_LEFT, y: 360 },
      { id: "llm", label: "Continue LLM\nLoop", type: "end", x: COL_RIGHT, y: 360 },
    ],
    edges: [
      { from: "start", to: "budget" },
      { from: "budget", to: "summary" },
      { from: "summary", to: "manual" },
      { from: "manual", to: "compact", label: "yes" },
      { from: "manual", to: "llm", label: "no" },
      { from: "compact", to: "llm" },
    ],
  },
  s07: {
    nodes: [
      { id: "start", label: "User Input", type: "start", x: COL_CENTER, y: 30 },
      { id: "llm", label: "LLM Call", type: "process", x: COL_CENTER, y: 110 },
      { id: "task", label: "Task Tool?", type: "decision", x: COL_CENTER, y: 190 },
      { id: "store", label: "Persistent\nTask Store", type: "subprocess", x: COL_LEFT, y: 280 },
      { id: "append", label: "Return Task\nState", type: "process", x: COL_LEFT, y: 360 },
      { id: "end", label: "Answer User", type: "end", x: COL_RIGHT, y: 280 },
    ],
    edges: [
      { from: "start", to: "llm" },
      { from: "llm", to: "task" },
      { from: "task", to: "store", label: "yes" },
      { from: "task", to: "end", label: "no" },
      { from: "store", to: "append" },
      { from: "append", to: "llm" },
    ],
  },
  s08: {
    nodes: [
      { id: "start", label: "User Input", type: "start", x: COL_CENTER, y: 30 },
      { id: "spawn", label: "Spawn Background\nTask", type: "subprocess", x: COL_LEFT, y: 120 },
      { id: "handle", label: "Return Task Id", type: "process", x: COL_LEFT, y: 210 },
      { id: "poll", label: "Poll Or Wait\nFor Notification", type: "decision", x: COL_CENTER, y: 300 },
      { id: "notify", label: "Inject Completion\nEvent", type: "process", x: COL_RIGHT, y: 390 },
      { id: "end", label: "Continue Foreground", type: "end", x: COL_CENTER, y: 480 },
    ],
    edges: [
      { from: "start", to: "spawn" },
      { from: "spawn", to: "handle" },
      { from: "handle", to: "poll" },
      { from: "poll", to: "notify", label: "done" },
      { from: "poll", to: "end", label: "still running" },
      { from: "notify", to: "end" },
    ],
  },
  s09: {
    nodes: [
      { id: "start", label: "Lead Request", type: "start", x: COL_CENTER, y: 30 },
      { id: "spawn", label: "Spawn Named\nWorker", type: "subprocess", x: COL_LEFT, y: 120 },
      { id: "send", label: "Send Mailbox\nMessage", type: "process", x: COL_CENTER, y: 210 },
      { id: "inbox", label: "Worker Reads\nInbox", type: "subprocess", x: COL_RIGHT, y: 300 },
      { id: "reply", label: "Worker Sends\nReply", type: "process", x: COL_CENTER, y: 390 },
      { id: "end", label: "Lead Continues", type: "end", x: COL_CENTER, y: 480 },
    ],
    edges: [
      { from: "start", to: "spawn" },
      { from: "spawn", to: "send" },
      { from: "send", to: "inbox" },
      { from: "inbox", to: "reply" },
      { from: "reply", to: "end" },
    ],
  },
  s10: {
    nodes: [
      { id: "start", label: "Protocol\nRequest", type: "start", x: COL_CENTER, y: 30 },
      { id: "create", label: "Create Request\nWith Id", type: "process", x: COL_CENTER, y: 120 },
      { id: "pending", label: "Pending", type: "decision", x: COL_CENTER, y: 210 },
      { id: "approved", label: "Approved", type: "subprocess", x: COL_LEFT, y: 310 },
      { id: "rejected", label: "Rejected", type: "subprocess", x: COL_RIGHT, y: 310 },
      { id: "end", label: "Runtime Uses\nOutcome", type: "end", x: COL_CENTER, y: 430 },
    ],
    edges: [
      { from: "start", to: "create" },
      { from: "create", to: "pending" },
      { from: "pending", to: "approved", label: "approve" },
      { from: "pending", to: "rejected", label: "reject" },
      { from: "approved", to: "end" },
      { from: "rejected", to: "end" },
    ],
  },
  s11: {
    nodes: [
      { id: "start", label: "Worker Idle", type: "start", x: COL_CENTER, y: 30 },
      { id: "poll", label: "Poll Inbox\nAnd Board", type: "process", x: COL_CENTER, y: 120 },
      { id: "claim", label: "Claimable Task?", type: "decision", x: COL_CENTER, y: 210 },
      { id: "take", label: "Claim Task", type: "subprocess", x: COL_LEFT, y: 310 },
      { id: "message", label: "Send Update", type: "process", x: COL_LEFT, y: 400 },
      { id: "end", label: "Continue Work", type: "end", x: COL_RIGHT, y: 310 },
    ],
    edges: [
      { from: "start", to: "poll" },
      { from: "poll", to: "claim" },
      { from: "claim", to: "take", label: "yes" },
      { from: "claim", to: "end", label: "no" },
      { from: "take", to: "message" },
      { from: "message", to: "end" },
    ],
  },
  s12: {
    nodes: [
      { id: "start", label: "Assigned Task", type: "start", x: COL_CENTER, y: 30 },
      { id: "worktree", label: "Provision\nWorktree", type: "subprocess", x: COL_LEFT, y: 130 },
      { id: "bind", label: "Bind Task To\nWorkspace", type: "process", x: COL_CENTER, y: 220 },
      { id: "log", label: "Write Event\nLog", type: "process", x: COL_RIGHT, y: 310 },
      { id: "end", label: "Isolated Work\nContinues", type: "end", x: COL_CENTER, y: 420 },
    ],
    edges: [
      { from: "start", to: "worktree" },
      { from: "worktree", to: "bind" },
      { from: "bind", to: "log" },
      { from: "log", to: "end" },
    ],
  },
};

export function getFlowForVersion(version: string): FlowDefinition | null {
  return EXECUTION_FLOWS[version] ?? null;
}
