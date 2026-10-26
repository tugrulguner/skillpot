export function groupRows(rows) {
  if (!Array.isArray(rows)) throw new TypeError('Input must be an array of rows.');
  const groups = new Map();
  for (const row of rows) {
    if (!row || typeof row.id !== 'string' || !row.id.trim() || typeof row.item !== 'string' || !row.item.trim()) {
      throw new TypeError('Each row needs a non-empty identifier and item.');
    }
    if (!groups.has(row.id)) groups.set(row.id, []);
    groups.get(row.id).push(row.item);
  }
  return [...groups].map(([id, items]) => ({ id, items }));
}
