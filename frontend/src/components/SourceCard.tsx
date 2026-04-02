import { FileText, BookOpen } from "lucide-react";
import { SourceDocument } from "../lib/api";

export function SourceCard({ source, index }: { source: SourceDocument; index?: number }) {
  return (
    <div className="rounded-lg border border-[var(--border)] bg-[var(--bg)] p-3 text-sm animate-fade-in">
      <div className="flex items-center gap-2 mb-1.5">
        {index !== undefined && (
          <span className="w-5 h-5 rounded-full bg-[var(--green)]/20 text-[var(--green)] text-[10px] font-bold flex items-center justify-center flex-shrink-0">
            {index}
          </span>
        )}
        <FileText size={12} className="text-[var(--green)] flex-shrink-0" />
        <span className="font-medium text-[var(--gold)] text-xs truncate">
          {source.source}
        </span>
        {source.page && (
          <span className="ml-auto text-[var(--muted)] text-[10px] flex-shrink-0">
            পৃষ্ঠা {source.page}
          </span>
        )}
      </div>
      {source.article && (
        <div className="flex items-center gap-1 mb-1.5">
          <BookOpen size={11} className="text-[var(--muted)]" />
          <span className="text-[var(--green)] text-[10px] font-medium">{source.article}</span>
        </div>
      )}
      <p className="text-[var(--muted)] text-xs leading-relaxed line-clamp-3">
        {source.content}
      </p>
    </div>
  );
}