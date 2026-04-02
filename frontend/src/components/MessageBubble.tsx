"use client";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { SourceCard } from "./SourceCard";
import { Scale, User } from "lucide-react";
import clsx from "clsx";
import { ChatMessage } from "../lib/api";

export function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";

  return (
    <div className={clsx("flex gap-3 mb-6", isUser && "flex-row-reverse")}>
      {/* Avatar */}
      <div
        className={clsx(
          "w-9 h-9 rounded-full flex items-center justify-center flex-shrink-0 mt-1",
          isUser
            ? "bg-[var(--red)] text-white"
            : "bg-[var(--green)] text-white"
        )}
      >
        {isUser ? <User size={16} /> : <Scale size={16} />}
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

        {/* Sources */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="mt-2 w-full space-y-2">
            <p className="text-xs text-[var(--muted)] px-1">📚 সূত্র / Sources:</p>
            {message.sources.map((src, i) => (
              <SourceCard key={i} source={src} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}