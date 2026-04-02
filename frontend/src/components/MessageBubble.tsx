"use client";
import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { SourceCard } from "./SourceCard";
import { User, Scale, ChevronDown, ChevronUp, BookOpen } from "lucide-react";
import clsx from "clsx";
import { ChatMessage } from "../lib/api";

export function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";
  const [sourcesOpen, setSourcesOpen] = useState(false);
  const sourceCount = message.sources?.length ?? 0;

  return (
    <div className={clsx("flex gap-3 mb-6", isUser && "flex-row-reverse")}>
      {/* Avatar */}
      <div
        className={clsx(
          "w-9 h-9 rounded-full flex items-center justify-center flex-shrink-0 mt-1",
          isUser ? "bg-[var(--red)] text-white" : "bg-[var(--green)] text-white"
        )}
      >
        {isUser ? <User size={16} /> : <ScaleIcon size={16} />}
      </div>

      <div className={clsx("max-w-[75%]", isUser && "items-end flex flex-col")}>
        {/* Bubble */}
        <div
          className={clsx(
            "rounded-2xl px-4 py-3 text-sm leading-relaxed",
            isUser
              ? "bg-[var(--red)] text-white rounded-tr-sm"
              : "bg-[var(--surface)] border border-[var(--border)] text-[var(--text)] rounded-tl-sm"
          )}
        >
          {isUser ? (
            <p className={message.content.match(/[\u0980-\u09FF]/) ? "bangla-text" : ""}>
              {message.content}
            </p>
          ) : (
            <div className="prose-custom">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {message.content}
              </ReactMarkdown>
            </div>
          )}
        </div>

        {/* Sources toggle — only for assistant with sources */}
        {!isUser && sourceCount > 0 && (
          <div className="mt-2 w-full">
            {/* Toggle button */}
            <button
              onClick={() => setSourcesOpen((prev) => !prev)}
              className={clsx(
                "flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all w-full",
                sourcesOpen
                  ? "bg-[var(--green)]/15 border border-[var(--green)]/40 text-[var(--green)]"
                  : "bg-[var(--surface)] border border-[var(--border)] text-[var(--muted)] hover:border-[var(--green)]/40 hover:text-[var(--green)]"
              )}
            >
              <BookOpen size={12} />
              <span>
                {sourcesOpen ? "সূত্র লুকান" : "সূত্র দেখুন"}{" "}
                <span className="opacity-70">/ {sourcesOpen ? "Hide" : "Show"} sources</span>
              </span>
              <span
                className={clsx(
                  "ml-1 px-1.5 py-0.5 rounded-full text-[10px] font-bold",
                  sourcesOpen
                    ? "bg-[var(--green)]/20 text-[var(--green)]"
                    : "bg-[var(--border)] text-[var(--muted)]"
                )}
              >
                {sourceCount}
              </span>
              <span className="ml-auto">
                {sourcesOpen ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
              </span>
            </button>

            {/* Collapsible sources list */}
            <div
              className={clsx(
                "overflow-hidden transition-all duration-300 ease-in-out",
                sourcesOpen ? "max-h-[600px] opacity-100 mt-2" : "max-h-0 opacity-0"
              )}
            >
              <div className="space-y-2">
                {message.sources!.map((src, i) => (
                  <SourceCard key={i} source={src} index={i + 1} />
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// Local Scale icon to avoid lucide version issues
function ScaleIcon({ size }: { size: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M12 2v20" />
      <path d="M2 12h20" />
      <path d="M6 6l12 12" />
      <path d="M18 6L6 18" />
    </svg>
  );
}