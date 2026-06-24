import json
import random
from datetime import datetime, timedelta
from app.database import db_execute


def record_question_view(conn, user_id: int, question_id: int, was_correct: bool | None = None):
    """Record that user saw a question. Called after check or submit."""
    db_execute(
        conn,
        "INSERT INTO user_question_history (user_id, question_id, was_correct) VALUES (%s, %s, %s)",
        (user_id, question_id, 1 if was_correct else 0 if was_correct is not None else None),
    )
    conn.commit()


def get_user_question_stats(conn, user_id: int, question_ids: list[int]) -> dict[int, dict]:
    """
    Return per-question stats for a user:
    {
        question_id: {
            'times_seen': int,
            'last_seen_days_ago': int | None,
            'last_correct': bool | None
        }
    }
    """
    if not question_ids:
        return {}

    placeholders = ",".join(["%s"] * len(question_ids))
    query = f"""
        SELECT
            question_id,
            COUNT(*) as times_seen,
            MAX(seen_at) as last_seen,
            (SELECT was_correct FROM user_question_history
             WHERE user_id = %s AND question_id = h.question_id
             ORDER BY seen_at DESC LIMIT 1) as last_correct
        FROM user_question_history h
        WHERE user_id = %s AND question_id IN ({placeholders})
        GROUP BY question_id
    """

    rows = db_execute(conn, query, (user_id, user_id, *question_ids)).fetchall()

    stats = {}
    now = datetime.now()
    for row in rows:
        qid = row[0] if isinstance(row, tuple) else row["question_id"]
        times_seen = row[1] if isinstance(row, tuple) else row["times_seen"]
        last_seen = row[2] if isinstance(row, tuple) else row["last_seen"]
        last_correct = row[3] if isinstance(row, tuple) else row["last_correct"]

        # Parse last_seen timestamp
        if isinstance(last_seen, str):
            try:
                last_seen_dt = datetime.fromisoformat(last_seen.replace("Z", "+00:00"))
            except:
                last_seen_dt = datetime.strptime(last_seen, "%Y-%m-%d %H:%M:%S")
        elif hasattr(last_seen, 'timestamp'):
            last_seen_dt = last_seen
        else:
            last_seen_dt = None

        days_ago = (now - last_seen_dt).days if last_seen_dt else None

        stats[qid] = {
            "times_seen": times_seen,
            "last_seen_days_ago": days_ago,
            "last_correct": bool(last_correct) if last_correct is not None else None,
        }

    return stats


def get_weighted_question_sample(
    conn,
    user_id: int | None,
    available_questions: list[dict],
    count: int,
    session_exclude: set[int] = None
) -> list[dict]:
    """
    Smart question selection with weighted randomization.

    Weights:
    - Never seen: weight 10
    - Seen 1 time, >7 days ago: weight 5
    - Seen 1 time, 1-7 days ago: weight 2
    - Seen 2 times, >14 days ago: weight 3
    - Seen 2 times, <14 days ago: weight 1
    - Seen 3+ times in last 30 days: weight 0 (skip)
    - In session_exclude set: weight 0 (skip)

    Falls back to uniform random if user_id is None (guest).
    """
    session_exclude = session_exclude or set()

    # Guest mode: uniform random selection
    if user_id is None:
        available = [q for q in available_questions if q["id"] not in session_exclude]
        random.shuffle(available)
        return available[:count]

    # Get stats for all available questions
    question_ids = [q["id"] for q in available_questions]
    stats = get_user_question_stats(conn, user_id, question_ids)

    # Calculate weights
    weighted = []
    for question in available_questions:
        qid = question["id"]

        # Skip if in session exclude
        if qid in session_exclude:
            continue

        stat = stats.get(qid)

        if stat is None:
            # Never seen
            weight = 10
        else:
            times = stat["times_seen"]
            days = stat["last_seen_days_ago"] or 0

            if times >= 3 and days <= 30:
                # Seen 3+ times in last 30 days: skip
                weight = 0
            elif times == 1:
                weight = 5 if days > 7 else 2
            elif times == 2:
                weight = 3 if days > 14 else 1
            else:
                # times >= 3 but > 30 days ago
                weight = 1

        if weight > 0:
            weighted.append((question, weight))

    # If not enough questions with positive weight, include all non-excluded
    if len(weighted) < count:
        for question in available_questions:
            if question["id"] not in session_exclude and not any(q[0]["id"] == question["id"] for q in weighted):
                weighted.append((question, 1))

    # Weighted random selection
    if not weighted:
        return []

    # Use weights to sample
    questions = [item[0] for item in weighted]
    weights = [item[1] for item in weighted]

    # Sample without replacement
    if len(questions) <= count:
        selected = questions
    else:
        selected = []
        available_indices = list(range(len(questions)))
        available_weights = weights[:]

        for _ in range(min(count, len(questions))):
            total_weight = sum(available_weights)
            if total_weight == 0:
                # All remaining have weight 0, just pick randomly
                idx = random.choice(range(len(available_indices)))
            else:
                rand = random.uniform(0, total_weight)
                cumulative = 0
                idx = 0
                for i, w in enumerate(available_weights):
                    cumulative += w
                    if rand <= cumulative:
                        idx = i
                        break

            selected.append(questions[available_indices[idx]])
            available_indices.pop(idx)
            available_weights.pop(idx)

    random.shuffle(selected)
    return selected
