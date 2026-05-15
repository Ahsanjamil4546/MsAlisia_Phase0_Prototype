import type { SummaryResponse } from '../types';

interface Props {
  summary?: SummaryResponse;
  onRefresh: () => void;
  disabled: boolean;
}

export function ParentSummary({ summary, onRefresh, disabled }: Props) {
  return (
    <section className="panel">
      <div className="section-heading compact">
        <p className="eyebrow">Step 3</p>
        <h2>Parent learning summary</h2>
        <p>A simple view for non-technical parents to understand what happened.</p>
      </div>

      <button className="secondary-button" onClick={onRefresh} disabled={disabled}>
        Refresh summary
      </button>

      {summary ? (
        <div className="summary-card">
          <div>
            <span>Total student turns</span>
            <strong>{summary.total_turns}</strong>
          </div>
          <div>
            <span>Latest focus</span>
            <strong>{summary.latest_topic}</strong>
          </div>
          <div>
            <span>Strengths</span>
            <ul>{summary.strengths.map((item) => <li key={item}>{item}</li>)}</ul>
          </div>
          <div>
            <span>Needs support</span>
            <ul>{summary.needs_support.map((item) => <li key={item}>{item}</li>)}</ul>
          </div>
          <div>
            <span>Next step</span>
            <strong>{summary.recommended_next_step}</strong>
          </div>
        </div>
      ) : (
        <p className="muted-box">Start a learning conversation, then refresh this summary.</p>
      )}
    </section>
  );
}
