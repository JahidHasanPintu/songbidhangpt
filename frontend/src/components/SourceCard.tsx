import { FileText, BookOpen } from "lucide-react";
import { SourceDocument } from "../lib/api";

export function SourceCard({ source }: { source: SourceDocument }) {
  return (
    <div className="rounded-lg border border-[var(--border)] bg-[var(--surface)] p-3 text-sm">
      <div className="flex items-center gap-2 mb-1.5">
        <FileText size={14} className="text-[var(--green)]" />
        <span className="font-medium text-[var(--gold)] text-xs truncate">
          {source.source}
        </span>
        {source.page && (
          <span className="ml-auto text-[var(--muted)] text-xs">
            পৃষ্ঠা {source.page}
          </span>
        )}
      </div>
      {source.article && (
        <div className="flex items-center gap-1 mb-1">
          <BookOpen size={12} className="text-[var(--muted)]" />
          <span className="text-[var(--muted)] text-xs">{source.article}</span>
        </div>
      )}
      <p className="text-[var(--muted)] text-xs leading-relaxed line-clamp-3">
        {source.content}
      </p>
    </div>
  );
}