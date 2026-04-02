"use client";
import { useState, useRef, useEffect } from "react";
import { MessageBubble } from "./MessageBubble";
import { Send, Loader2, Globe } from "lucide-react";
import clsx from "clsx";
import { ChatMessage, sendMessage } from "../lib/api";

const SUGGESTED = [
  "বাংলাদেশের সংবিধানের মৌলিক অধিকারগুলো কী কী?",
  "What are the fundamental principles of state policy?",
  "রাষ্ট্রের মূলনীতি কী?",
  "How is the President elected in Bangladesh?",
];

export function ChatWindow() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState<"auto" | "bn" | "en">("auto");
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (text?: string) => {
    const question = (text || input).trim();
    if (!question || loading) return;

    const userMsg: ChatMessage = { role: "user", content: question };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const history = messages.slice(-6).map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const res = await sendMessage({ question, language, chat_history: history });

      const assistantMsg: ChatMessage = {
        role: "assistant",
        content: res.answer,
        sources: res.sources,
        language: res.language_detected,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "⚠️ দুঃখিত, একটি সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।\n\nSorry, an error occurred. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between px-6 py-4 border-b border-[var(--border)] bg-[var(--surface)]">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-[var(--green)] flex items-center justify-center text-lg">
            ⚖️
          </div>
          <div>
            <h1 className="font-bold text-lg text-white bangla-text">সংবিধান GPT</h1>
            <p className="text-xs text-[var(--muted)]">Bangladesh Constitution AI</p>
          </div>
        </div>

        {/* Language Toggle */}
        <div className="flex items-center gap-1 bg-[var(--bg)] rounded-lg p-1 border border-[var(--border)]">
          <Globe size={14} className="text-[var(--muted)] ml-1" />
          {(["auto", "bn", "en"] as const).map((lang) => (
            <button
              key={lang}
              onClick={() => setLanguage(lang)}
              className={clsx(
                "px-3 py-1 rounded-md text-xs font-medium transition-all",
                language === lang
                  ? "bg-[var(--green)] text-white"
                  : "text-[var(--muted)] hover:text-white"
              )}
            >
              {lang === "auto" ? "Auto" : lang === "bn" ? "বাংলা" : "EN"}
            </button>
          ))}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-4">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full gap-8">
            <div className="text-center">
              <div className="text-6xl mb-4">🇧🇩</div>
              <h2 className="text-2xl font-bold text-white bangla-text mb-2">
                সংবিধান সম্পর্কে জিজ্ঞেস করুন
              </h2>
              <p className="text-[var(--muted)] text-sm">
                Ask anything about the Constitution of Bangladesh
              </p>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-2xl">
              {SUGGESTED.map((q, i) => (
                <button
                  key={i}
                  onClick={() => handleSend(q)}
                  className="text-left p-3 rounded-xl border border-[var(--border)] bg-[var(--surface)] hover:border-[var(--green)] hover:bg-[var(--green)]/10 transition-all text-sm text-[var(--muted)] hover:text-white"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}

        {loading && (
          <div className="flex gap-3 mb-6">
            <div className="w-9 h-9 rounded-full bg-[var(--green)] flex items-center justify-center flex-shrink-0">
              <Scale size={16} className="text-white" />
            </div>
            <div className="bg-[var(--surface)] border border-[var(--border)] rounded-2xl rounded-tl-sm px-4 py-3 flex items-center gap-2">
              <Loader2 size={16} className="animate-spin text-[var(--green)]" />
              <span className="text-[var(--muted)] text-sm">উত্তর তৈরি হচ্ছে...</span>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="px-6 py-4 border-t border-[var(--border)] bg-[var(--surface)]">
        <div className="flex gap-3 items-end">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="সংবিধান সম্পর্কে যেকোনো প্রশ্ন করুন... / Ask anything about the Constitution..."
            rows={1}
            className="flex-1 bg-[var(--bg)] border border-[var(--border)] rounded-xl px-4 py-3 text-sm text-white placeholder:text-[var(--muted)] resize-none focus:outline-none focus:border-[var(--green)] transition-colors max-h-32"
            style={{ minHeight: "48px" }}
            onInput={(e) => {
              const t = e.target as HTMLTextAreaElement;
              t.style.height = "auto";
              t.style.height = Math.min(t.scrollHeight, 128) + "px";
            }}
          />
          <button
            onClick={() => handleSend()}
            disabled={!input.trim() || loading}
            className="w-12 h-12 rounded-xl bg-[var(--green)] hover:bg-[var(--green)]/80 disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center transition-all flex-shrink-0"
          >
            <Send size={18} className="text-white" />
          </button>
        </div>
        <p className="text-center text-xs text-[var(--muted)] mt-2">
          SongbidhanGPT — Open Source · Developed by <a href="">Pintu</a>
        </p>
      </div>
    </div>
  );
}

function Scale(props: any) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} {...props}>
      <path d="M12 2v20M2 7h20M5 7l7-5 7 5M5 17l7 5 7-5" />
    </svg>
  );
}